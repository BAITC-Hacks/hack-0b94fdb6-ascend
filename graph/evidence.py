LIMITATIONS = {'boundary': 'исходящие не прослежены (колено 4)',
               'seed_inflow_incomplete': 'seed: входящие неполные',
               'external_inflow': 'отдаёт больше наблюдаемого входа — вероятны внешние поступления',
               'isolated': 'переводов в выгрузке нет — данных недостаточно'}
LABELS = {'in_kzt': 'наблюдаемый вход', 'betweenness': 'посредничество',
          'n_nbr_clusters': 'другие кластеры', 'seed_reach': 'достижимость от seed', 'role': 'роль'}


def money(value):
    if value >= 1_000_000:
        return f'{value / 1_000_000:.1f}'.replace('.', ',') + ' млн ₸'
    if value >= 1000:
        return f'{value / 1000:.1f}'.replace('.', ',') + ' тыс ₸'
    return f'{value:.2f}'.replace('.', ',') + ' ₸'


def explain(frame, c):
    evidences = []
    for row in frame.to_dict('records'):
        role, detail = row['role'], row['evidence_detail']
        a, b = row['in_deg'], row['out_deg']
        texts = {
            'consolidator': f"Признаки консолидации: {a} отправителей (порог {c['cons_min_in_deg']})",
            'distributor': f"Веерное распределение: {b} получателей (порог {c['dist_min_out_deg']})",
            'transit': f"Признаки транзита: дальше {100 * (row['pass_through'] or 0):.0f}% входа (коридор {100*c['transit_low']:.0f}–{100*c['transit_high']:.0f}%)",
            'terminal': f"Гипотеза конечного получателя: вход {money(row['in_kzt'])}, выход 0; колено {row['depth']}",
            'coordinator': f"Связующий узел: посредничество ≥ p{100*c['coord_bc_quantile']:g}, {row['n_nbr_clusters']} других кластеров, {max(row['up_hubs'], row['down_hubs'])} хабов",
            'peripheral': f'Признаков ролей нет: {a} отправителей, {b} получателей'}
        caveat = '; '.join(f"исходящие не прослежены (колено {c['boundary_depth']})" if x == 'boundary' else LIMITATIONS[x] for x in detail['limitations'])
        second = f"вход {money(row['in_kzt'])}, выход {money(row['out_kzt'])}"
        text = '; '.join(x for x in (texts[role], second, caveat) if x)
        if len(text) > c['evidence_max_len']:
            text = '; '.join(x for x in (texts[role], caveat) if x)
        if len(text) > c['evidence_max_len']:
            compact = f"{role}: входящих {a}, исходящих {b}"
            text = '; '.join(x for x in (compact, caveat) if x)
        if len(text) > c['evidence_max_len']:
            raise ValueError('evidence_max_len слишком мал для обязательных оговорок')
        evidences.append(text)
        if row['priority_rank'] <= c['top_n_api']:
            contributions = detail['priority_contributions']
            keys = sorted(LABELS, key=lambda key: (-contributions[key], key))[:2]
            facts = []
            for key in keys:
                value = f"{role}, score={row['role_score']:.4f}" if key == 'role' else f"{row[key]:.6g}"
                facts.append(f"{LABELS[key]}={value} (вклад {contributions[key]:.4f})")
            detail['why'] = f"{texts[role]} (score {row['role_score']:.4f}). " + '; '.join(facts) + '. ' + (caveat + '. ' if caveat else '') + 'Рекомендуется проверить контрагентов и полноту исходящих переводов.'
    frame['evidence'] = evidences
    # Flat EvidenceDetail columns are the §5 interface; nested copy supports snapshot consumers.
    for key in ('rule_id', 'rule_text', 'thresholds', 'values', 'strength', 'alternatives', 'limitations', 'priority_contributions', 'why'):
        frame[key] = [detail[key] for detail in frame.evidence_detail]
    return frame
