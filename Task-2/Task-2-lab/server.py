#!/usr/bin/env python3
"""Server for technical indicator calculator - static files + stock API proxy"""
import http.server, json, re, os, sys, urllib.request, urllib.parse, ssl, socketserver, threading

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

def fetch_url(url):
    """Fetch URL with urllib, using proper SSL context. Runs in thread."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
        return resp.read().decode('utf-8')

def get_kline(code):
    prefix = 'sh' if code.startswith('6') else 'sz'
    url = f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={prefix}{code},day,,,500,qfq'
    try:
        text = fetch_url(url)
        raw = json.loads(text)
    except Exception as e:
        return None, str(e)
    key = f'{prefix}{code}'
    data = raw.get('data', {}).get(key, {})
    klines = data.get('qfqday') or data.get('day')
    if not klines:
        return None, 'no data'
    dates, opens, closes, highs, lows, vols = [], [], [], [], [], []
    for k in klines:
        if len(k) < 6: continue
        dates.append(k[0].replace('-', ''))
        opens.append(float(k[1])); closes.append(float(k[2]))
        highs.append(float(k[3])); lows.append(float(k[4])); vols.append(float(k[5]))
    return {'dates': dates, 'open': opens, 'high': highs, 'low': lows, 'close': closes, 'vol': vols}, None

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/stock?'):
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            code = (params.get('code', [None])[0] or '').strip()
            if not re.match(r'^\d{6}$', code):
                self.send_json({'error': 'invalid code'}, 400)
                return
            result, err = get_kline(code)
            self.send_json(result if not err else {'error': err}, 500 if err else 200)
        else:
            super().do_GET()
    def send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8890
    server = socketserver.ThreadingTCPServer(('127.0.0.1', port), Handler)
    print(f'Serving at http://127.0.0.1:{port} (threaded)')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
