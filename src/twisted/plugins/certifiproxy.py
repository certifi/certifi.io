from twisted.application.service import ServiceMaker

rproxy = ServiceMaker(
    "certifiproxy",
    "certifiproxy",
    ("HTTP reverse proxy for certifi.io"),
    "certifiproxy")