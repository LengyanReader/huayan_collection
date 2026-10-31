import urllib.request

# Try different IIIF URL patterns
patterns = [
    "https://iiif.bdrc.io/bdr:I1PD105152::I1PD1051520001.jpg/full/full/0/default.jpg",
    "https://iiif.bdrc.io/bdr:I1PD105152::I1PD1051520001.jpg/full/!200,200/0/default.jpg",
    "https://iiif.bdrc.io/bdr:I1PD105152::I1PD1051520001.jpg/full/,200/0/default.jpg",
]
for url in patterns:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
            print("OK: {} -> status={}, type={}, len={}".format(url, r.status, r.headers.get("Content-Type"), len(data)))
    except Exception as e:
        print("FAIL: {} -> {}".format(url, e))
