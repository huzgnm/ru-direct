import os, sys, geosite
D = sys.argv[1]; RF = sys.argv[2]
def load(name, seen=None):
    seen = seen if seen is not None else set()
    if name in seen: return []
    seen.add(name); out = []
    p = os.path.join(D, name)
    if not os.path.exists(p): return out
    for line in open(p, encoding='utf-8'):
        line = line.split('#')[0].strip()
        if not line: continue
        if line.startswith('include:'):
            out += load(line[8:].split()[0], seen); continue
        if '@ads' in line: continue
        tok = line.split()[0]
        if tok.startswith(('regexp:','keyword:')): continue
        t = 'domain'
        if tok.startswith('full:'): t, tok = 'full', tok[5:]
        elif tok.startswith('domain:'): tok = tok[7:]
        out.append((t, tok.lower()))
    return out
TLDS = load('tld-ru')
tldset = {v for _,v in TLDS}
cats = [
 ('ru-bank', 'Ngân hàng / tài chính', ['category-bank-ru']),
 ('ru-gov', 'Chính phủ / dịch vụ công', ['category-gov-ru']),
 ('ru-medicine', 'Y tế', ['category-medicine-ru']),
 ('ru-shop', 'Mua sắm / bán lẻ', ['category-ecommerce-ru','category-retail-ru','ozon','wildberries','avito']),
 ('ru-social', 'Yandex / VK / Mail.ru / OK / Rutube', ['yandex','vk','mailru-group','rutube']),
 ('ru-telecom', 'Nhà mạng', ['megafon','mts-ru','rostelecom','t2-ru']),
 ('ru-media', 'Báo chí / giải trí', ['category-media-ru','category-entertainment-ru','category-tech-media-ru','category-forums-ru']),
 ('ru-travel', 'Du lịch / giao thông', ['category-travel-ru']),
 ('ru-edu', 'Giáo dục', ['category-education-ru']),
]
EXTRA = {'ru-media':['ivi.tv','tass.com'], 'ru-travel':['onetwotrip.com','pobeda.aero'],
         'ru-bank':['qiwi.com'], 'ru-other':['bitrix24.com']}
used = set(); out = {}
for code, title, files in cats:
    s = {}
    for f in files:
        for t,v in load(f):
            if v not in used and v not in tldset: s.setdefault(v, t)
    for v in EXTRA.get(code, []): s.setdefault(v, 'domain')
    used.update(s); out[code] = (title, s)
rest = {}
for t,v in load('category-ru'):
    if v not in used and v not in tldset: rest.setdefault(v, t)
inside = geosite.decode(open(RF,'rb').read(), only={'ru-available-only-inside'})['RU-AVAILABLE-ONLY-INSIDE']
for t,v in inside:
    if v not in used and v not in tldset: rest.setdefault(v, t)
for v in EXTRA['ru-other']: rest.setdefault(v, 'domain')
used.update(rest); out['ru-other'] = ('Khác (công ty Nga, phần mềm, hosting...)', rest)
out = {'ru-tld': ('TLD Nga (.ru .su .рф .рус .moscow ...)', {v:t for t,v in TLDS}), **out}

# xuất data/ dạng nguồn v2fly + txt
for code,(title,s) in out.items():
    with open(f'data/{code}','w') as f:
        f.write(f'# {title}\n')
        for v in sorted(s): f.write(('full:' if s[v]=='full' else '')+v+'\n')
with open('data/ru-direct','w') as f:
    f.write('# Tất cả domain Nga nên đi DIRECT\n'+''.join(f'include:{c}\n' for c in out))
entries = {c: sorted((t,v) for v,t in s.items()) for c,(_,s) in out.items()}
entries['ru-direct'] = [x for c in out for x in entries[c]]
# bản không TLD: chỉ domain không đuôi Nga, dùng khi đã có geosite:tld-ru riêng
entries['ru-direct-notld'] = [(t,v) for t,v in entries['ru-direct'] if v.split('.')[-1] not in tldset]
entries = dict(sorted(entries.items()))
open('geosite.dat','wb').write(geosite.encode(entries))
with open('ru-direct.txt','w') as f:
    for c,(title,s) in out.items():
        f.write(f'# === {title} ({len(s)}) ===\n'+''.join(('full:' if s[v]=='full' else 'domain:')+v+'\n' for v in sorted(s))+'\n')
for c,v in entries.items(): print(c, len(v))
