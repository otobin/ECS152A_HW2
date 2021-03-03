import requests

proxys = {
    'http': 'http://localhost:8888',
    'https': 'http://localhost:8888',
}

files = [
    'http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file1.html',
    'http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html',
    'http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html',
    'http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file4.html',
    'http://gaia.cs.umass.edu/pearson.png',
    'http://kurose.cslash.net/8E_cover_small.jpg',
]

for f in files:
    r = requests.get(f, proxies=proxys, allow_redirects=True)
    print(r)
    if r.status_code == 200:
        print(r.headers.get('Content-Type'))

        if r.headers.get('Content-Type') == 'text/plain':
            print(r.text)
