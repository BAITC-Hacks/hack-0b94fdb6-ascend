"""Build a self-contained offline viewer of an existing analysis snapshot."""
import argparse
import json
from pathlib import Path


def build_view(snapshot_path, output_path):
    source, target = Path(snapshot_path), Path(output_path)
    if source.resolve() == target.resolve():
        raise ValueError('HTML не должен перезаписывать исходный снимок')
    data = json.loads(source.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or any(not isinstance(data.get(k), list) for k in ('nodes', 'edges', 'clusters')):
        raise ValueError('Ожидается снимок с nodes, edges и clusters')
    if not data['nodes']:
        raise ValueError('В снимке нет узлов для просмотра')
    for node in data['nodes']:
        if not isinstance(node.get('gid'), str):
            raise ValueError('gid в снимке должен быть строкой')
    # Preserve IDs; prevent data from breaking out of the script element.
    payload = json.dumps(data, ensure_ascii=False, allow_nan=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    template = Path(__file__).with_name('viewer.html').read_text(encoding='utf-8')
    html = template.replace('__SNAPSHOT_JSON__', payload)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding='utf-8')
    return target.resolve()


def main():
    p = argparse.ArgumentParser(description='Локальный просмотр готового графа без сервера и интернета')
    p.add_argument('--snapshot', type=Path, required=True)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    try:
        path = build_view(a.snapshot, a.output or a.snapshot.with_name('graph-view.html'))
    except (OSError, ValueError) as exc:
        p.exit(2, f'Не удалось создать просмотр: {exc}\n')
    print(f'Откройте в браузере: {path}')


if __name__ == '__main__':
    main()
