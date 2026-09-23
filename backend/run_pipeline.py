"""CLI entry point: real analysis by default, synthetic output only with --demo."""
import argparse
import sys
from pathlib import Path
from backend.pipeline import run_pipeline


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='Расчёт и публикация результата Graph Engine')
    base = Path(__file__).resolve().parent
    parser.add_argument('--data', type=Path, default=base / 'data')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--config', type=Path, default=Path('./config/methodology.yaml'))
    parser.add_argument('--demo', action='store_true', help='Явно использовать синтетические данные, без Graph Engine')
    args = parser.parse_args()
    output = args.output or base / ('output-demo' if args.demo else 'output')
    return run_pipeline(args.data, output, args.config, demo=args.demo)


if __name__ == '__main__':
    raise SystemExit(main())
