import csv, json

rows = []
with open('D:/online internship/Task-2/兆易创新_近一年交易数据.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append({
            'd': r['trade_date'],
            'o': float(r['open']),
            'h': float(r['high']),
            'l': float(r['low']),
            'c': float(r['close']),
            'v': float(r['vol'])
        })
rows.reverse()

dates = json.dumps([r['d'] for r in rows], separators=(',', ':'))
opens = json.dumps([r['o'] for r in rows], separators=(',', ':'))
highs = json.dumps([r['h'] for r in rows], separators=(',', ':'))
lows  = json.dumps([r['l'] for r in rows], separators=(',', ':'))
closes = json.dumps([r['c'] for r in rows], separators=(',', ':'))
vols  = json.dumps([r['v'] for r in rows], separators=(',', ':'))

with open('D:/online internship/Task-2/Task-2-lab/data.js', 'w', encoding='utf-8') as f:
    f.write('// ' + str(len(rows)) + ' rows of 兆易创新 data\n')
    f.write('const STOCK_PRESETS = {\n')
    f.write('  "兆易创新": {\n')
    f.write('    dates: ' + dates + ',\n')
    f.write('    open: ' + opens + ',\n')
    f.write('    high: ' + highs + ',\n')
    f.write('    low: ' + lows + ',\n')
    f.write('    close: ' + closes + ',\n')
    f.write('    vol: ' + vols + '\n')
    f.write('  }\n')
    f.write('};\n')

print('done,', len(rows), 'rows')
