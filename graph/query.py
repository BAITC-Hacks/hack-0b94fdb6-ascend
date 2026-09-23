"""Read-only, bounded tools over a frozen backend snapshot."""
from collections import Counter, deque
from copy import deepcopy
import re
import networkx as nx

NODE_FIELDS = ('gid', 'depth', 'is_seed', 'is_boundary', 'is_isolated', 'external_inflow',
               'role', 'base_role', 'role_score', 'priority_score', 'priority_rank', 'cluster_id',
               'component_id', 'in_deg', 'out_deg', 'in_tx', 'out_tx', 'in_kzt', 'out_kzt',
               'pass_through', 'seed_in', 'seed_reach', 'betweenness', 'pagerank',
               'n_nbr_clusters', 'up_hubs', 'down_hubs', 'evidence', 'temporal', 'x', 'y')


class ToolError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def integer(value, lo, hi):
    if type(value) is not int or not lo <= value <= hi:
        raise ToolError('invalid_param', f'Ожидается целое число от {lo} до {hi}')
    return value


class SnapshotTools:
    def __init__(self, snapshot):
        # Detached from mutable backend dictionaries and any future reload.
        snap = deepcopy(snapshot)
        self.nodes = {n['gid']: n for n in snap['nodes']}
        if any(not isinstance(gid, str) or not re.fullmatch(r'[0-9]{1,19}', gid) for gid in self.nodes):
            raise ValueError('Снимок должен содержать gid строками')
        self.clusters = {c['cluster_id']: c for c in snap['clusters']}
        self.g = nx.DiGraph()
        self.g.add_nodes_from(self.nodes)
        for e in snap['edges']:
            if e['src'] not in self.nodes or e['dst'] not in self.nodes:
                raise ValueError('Ребро ссылается на неизвестный gid')
            if e['src'] != e['dst']:
                self.g.add_edge(e['src'], e['dst'], **e)

    def gid(self, gid):
        if not isinstance(gid, str) or not re.fullmatch(r'[0-9]{1,19}', gid):
            raise ToolError('invalid_gid', 'gid должен содержать 1–19 цифр')
        if gid not in self.nodes:
            raise ToolError('not_found', 'Узел не найден')
        return gid

    def node(self, gid):
        n = self.nodes[gid]
        return {k: n[k] for k in NODE_FIELDS if k in n}

    def ordered(self, gids):
        return sorted(gids, key=lambda g: (-self.nodes[g]['priority_score'], int(g)))

    def get_node(self, gid):
        gid = self.gid(gid)
        node = self.nodes[gid]
        detail = node.get('evidence_detail', {k: node[k] for k in ('rule_id', 'rule_text', 'thresholds', 'values', 'strength', 'alternatives', 'limitations', 'priority_contributions', 'why') if k in node})
        return {'node': self.node(gid), 'evidence_detail': deepcopy(detail),
                'neighbors': self.get_neighbors(gid, 'both', 10)}

    def get_neighbors(self, gid, direction, limit):
        gid = self.gid(gid)
        integer(limit, 1, 20)
        if direction not in ('in', 'out', 'both'):
            raise ToolError('invalid_param', 'direction: in, out или both')
        pairs = set()
        if direction in ('in', 'both'):
            pairs.update(self.g.in_edges(gid))
        if direction in ('out', 'both'):
            pairs.update(self.g.out_edges(gid))
        ordered = sorted(pairs, key=lambda p: (-self.g.edges[p]['sum_kzt'], int(p[0]), int(p[1])))
        return {'items': [{'edge': dict(self.g.edges[a, b]), 'node': self.node(b if a == gid else a)} for a, b in ordered[:limit]],
                'total': len(ordered), 'truncated': len(ordered) > limit}

    def common(self, gids, max_depth, reverse=False):
        if not isinstance(gids, list) or not 1 <= len(gids) <= 10 or any(not isinstance(g, str) for g in gids) or len(set(gids)) != len(gids):
            raise ToolError('invalid_param', 'Нужны 1–10 разных gid')
        gids = [self.gid(x) for x in gids]
        integer(max_depth, 1, 4)
        graph = self.g.reverse(copy=False) if reverse else self.g
        hits = Counter()
        for gid in gids:
            hits.update(set(nx.single_source_shortest_path_length(graph, gid, cutoff=max_depth)) - {gid})
        common = [g for g, count in hits.items() if count == len(gids)]
        exact = bool(common)
        candidates = common if exact else list(hits)
        ordered = sorted(candidates, key=lambda g: (-hits[g], -self.nodes[g]['priority_score'], int(g)))
        return {'items': [{'node': self.node(g), 'matched_sources': hits[g]} for g in ordered[:20]],
                'total': len(ordered), 'truncated': len(ordered) > 20, 'exact_intersection': exact,
                'requested_sources': len(gids), 'max_depth': max_depth,
                'limitation': 'Достижимость по наблюдаемым рёбрам; не доказательство движения одних и тех же средств.'}

    def common_downstream(self, gids, max_depth):
        return self.common(gids, max_depth)

    def common_upstream(self, gids, max_depth):
        return self.common(gids, max_depth, reverse=True)

    def find_paths(self, src, dst, max_len, limit):
        src, dst = self.gid(src), self.gid(dst)
        integer(max_len, 1, 6)
        integer(limit, 1, 5)
        distances = nx.single_source_shortest_path_length(self.g.reverse(copy=False), dst, cutoff=max_len)
        queue, paths, expansions = deque([(src,)]), [], 0
        # Both expansions and queue size are bounded, including adversarial dense graphs.
        budget = 10000
        while queue and len(paths) <= limit and expansions < budget:
            path = queue.popleft()
            expansions += 1
            if path[-1] == dst:
                paths.append(path)
                continue
            if len(path)-1 >= max_len:
                continue
            for v in sorted(self.g.successors(path[-1]), key=int):
                if v not in path and len(path) + distances.get(v, max_len+1) <= max_len:
                    if len(queue) + expansions >= budget:
                        return self.path_result(paths, limit, True)
                    queue.append(path + (v,))
        return self.path_result(paths, limit, bool(queue) or len(paths) > limit)

    def path_result(self, paths, limit, truncated):
        return {'paths': [{'gids': list(path), 'edges': [dict(self.g.edges[a, b]) for a, b in zip(path, path[1:])]} for path in paths[:limit]],
                'truncated': truncated,
                'limitation': 'Структурные пути по агрегатам; порядок отдельных переводов не установлен.'}

    def get_top(self, n, role=None, cluster_id=None):
        integer(n, 1, 20)
        if role is not None and role not in ('consolidator', 'distributor', 'transit', 'terminal', 'coordinator', 'peripheral'):
            raise ToolError('invalid_param', 'Неизвестная роль')
        if cluster_id is not None:
            integer(cluster_id, 0, max(self.clusters, default=0))
        ids = [g for g, x in self.nodes.items() if (role is None or x['role'] == role) and (cluster_id is None or x['cluster_id'] == cluster_id)]
        return {'items': [self.node(g) for g in self.ordered(ids)[:n]], 'total': len(ids), 'truncated': len(ids) > n}

    def get_cluster(self, cluster_id):
        if type(cluster_id) is not int or cluster_id not in self.clusters:
            raise ToolError('not_found', 'Кластер не найден')
        cluster = self.clusters[cluster_id]
        return {'cluster': deepcopy(cluster), 'nodes': [self.node(g) for g in cluster['top_gids']],
                'truncated': cluster['n_nodes'] > len(cluster['top_gids'])}

    def dispatch(self, name, args):
        if name not in {t['name'] for t in TOOL_SCHEMAS} or not isinstance(args, dict):
            raise ToolError('invalid_param', 'Неизвестный инструмент или аргументы')
        schema = next(t['parameters'] for t in TOOL_SCHEMAS if t['name'] == name)
        if set(args) != set(schema['required']):
            raise ToolError('invalid_param', 'Неверные имена аргументов инструмента')
        try:
            return getattr(self, name)(**args)
        except (TypeError, ValueError) as exc:
            if isinstance(exc, ToolError):
                raise
            raise ToolError('invalid_param', 'Неверный тип аргументов') from exc


def tool(name, description, properties):
    return {'type': 'function', 'name': name, 'description': description, 'strict': True,
            'parameters': {'type': 'object', 'properties': properties, 'required': list(properties), 'additionalProperties': False}}

GID = {'type': 'string', 'pattern': '^[0-9]{1,19}$'}
def bound(lo, hi):
    return {'type': 'integer', 'minimum': lo, 'maximum': hi}

TOOL_SCHEMAS = [
    tool('get_node', 'Карточка узла, правило роли и до 10 соседей', {'gid': GID}),
    tool('get_neighbors', 'Наблюдаемые связи узла', {'gid': GID, 'direction': {'type': 'string', 'enum': ['in', 'out', 'both']}, 'limit': bound(1, 20)}),
    *[tool(name, desc, {'gids': {'type': 'array', 'items': GID, 'minItems': 1, 'maxItems': 10}, 'max_depth': bound(1, 4)}) for name, desc in [('common_downstream', 'Общие получатели по направлению денег'), ('common_upstream', 'Общие источники против направления денег')]],
    tool('find_paths', 'Ограниченный поиск направленных структурных путей', {'src': GID, 'dst': GID, 'max_len': bound(1, 6), 'limit': bound(1, 5)}),
    tool('get_top', 'Готовый приоритет, без пересчёта', {'n': bound(1, 20), 'role': {'type': ['string', 'null']}, 'cluster_id': {'type': ['integer', 'null']}}),
    tool('get_cluster', 'Гипотеза и ключевые узлы кластера', {'cluster_id': {'type': 'integer', 'minimum': 0}})]
