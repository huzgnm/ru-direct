# Encode/decode geosite.dat (v2ray routercommon.GeoSiteList) không cần protobuf lib
TYPES = {'plain':0,'regexp':1,'domain':2,'full':3}
def varint(n):
    b = bytearray()
    while True:
        x = n & 0x7f; n >>= 7
        if n: b.append(x|0x80)
        else: b.append(x); return bytes(b)
def ld(field, data): return varint(field<<3|2) + varint(len(data)) + data
def enc_domain(t, v):
    out = b''
    if TYPES[t]: out += varint(1<<3|0) + varint(TYPES[t])
    return out + ld(2, v.encode())
def encode(entries):  # entries: {code: [(type,value)]}
    out = b''
    for code, doms in entries.items():
        body = ld(1, code.upper().encode()) + b''.join(ld(2, enc_domain(t,v)) for t,v in doms)
        out += ld(1, body)
    return out
def rd_varint(b, i):
    n = s = 0
    while True:
        x = b[i]; i += 1; n |= (x&0x7f)<<s; s += 7
        if x < 0x80: return n, i
def fields(b):
    i = 0
    while i < len(b):
        k, i = rd_varint(b, i); f, w = k>>3, k&7
        if w == 0: v, i = rd_varint(b, i)
        elif w == 2:
            l, i = rd_varint(b, i); v = b[i:i+l]; i += l
        else: raise ValueError(w)
        yield f, v
def decode(b, only=None):
    R = {v:k for k,v in TYPES.items()}; res = {}
    for f, site in fields(b):
        code = None; doms = []
        for f2, v in fields(site):
            if f2 == 1: code = v.decode()
            elif f2 == 2:
                if only and code and code.lower() not in only: continue
                t = 0; val = ''
                for f3, v3 in fields(v):
                    if f3 == 1: t = v3
                    elif f3 == 2: val = v3.decode()
                doms.append((R[t], val))
        if not only or code.lower() in only: res[code] = doms
    return res
