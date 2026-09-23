"""Convenient server launcher with an explicit demo mode."""
import argparse
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Запустить API')
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--port', type=int, default=int(os.getenv('API_PORT', '8000')))
    args = parser.parse_args()
    if args.demo:
        os.environ['OUTPUT_DIR'] = str(Path(__file__).parent / 'output-demo')
    import uvicorn
    uvicorn.run('backend.api:app', host=os.getenv('API_HOST', '127.0.0.1'), port=args.port)


if __name__ == '__main__':
    main()
