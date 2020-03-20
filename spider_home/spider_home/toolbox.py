from http.cookies import SimpleCookie


def extract_ck2dict(rep):
    cookie_bytes = rep.headers.getlist('Set-Cookie')
    cookie = SimpleCookie()
    for b in cookie_bytes:
        cookie.load(b.decode('utf-8'))
    cookie_dict = {}
    for k, m in cookie.items():
        cookie_dict[k] = m.value
    return cookie_dict
