"""Serve only the public Mini App, with portable JavaScript MIME types."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'miniapp'


class MiniAppHandler(SimpleHTTPRequestHandler):
    # Windows registry MIME mappings can otherwise serve .mjs as text/plain.
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map,
                      '.mjs': 'text/javascript', '.js': 'text/javascript',
                      '.css': 'text/css', '.svg': 'image/svg+xml'}

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()


def main():
    parser = argparse.ArgumentParser(description='Serve the public Freedom Graph Mini App')
    parser.add_argument('--port', type=int, default=5175)
    args = parser.parse_args()
    with ThreadingHTTPServer(('127.0.0.1', args.port), partial(MiniAppHandler, directory=str(ROOT))) as server:
        print(f'Mini App: http://127.0.0.1:{args.port} (Ctrl+C to stop)', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
