import json
from urllib.parse import parse_qs


def pretty_json(d):
    return json.dumps(d, indent=4, ensure_ascii=False)


def get_qs_dict(request):
    qs_bytes = request.query_string
    qs = qs_bytes.decode('utf-8')
    return parse_qs(qs)
