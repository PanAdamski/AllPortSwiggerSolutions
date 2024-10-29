# AllPortSwiggerSolutions
Here you will find all solutions to all tasks from the [https://portswigger.net/](https://portswigger.net/web-security/all-labs) platform written in python



Progress
| ID | Topic | Apprentice | Practitioner | Expert | 
| --- | --- | :---: | :---: | :---: |
| 01 | SQL injection | :white_check_mark: 2/2 | :white_check_mark: 15/15 | - |
| 02 | Cross-site scripting (XSS) | :white_check_mark: 9/9 | :white_check_mark: 15/15 | :x: 5/6 |
| 03 | Cross-site request forgery (CSRF) | :white_check_mark: 1/1 | :white_check_mark: 11/11 | - |
| 04 | Clickjacking | :white_check_mark: 3/3 | :white_check_mark: 2/2 | - |
| 05 | DOM-based vulnerabilities | - | :white_check_mark: 5/5 | :white_check_mark: 2/2 |
| 06 | Cross-origin resource sharing (CORS) | :white_check_mark: 2/2 | :white_check_mark: 1/1 | -  |
| 07 | XML external entity (XXE) injection | :white_check_mark: 2/2 | :white_check_mark: 6/6 | :white_check_mark: 1/1|
| 08 | Server-side request forgery (SSRF) | :white_check_mark: 2/2 | :white_check_mark: 3/3 | :white_check_mark: 2/2 |
| 09 | HTTP request smuggling | - | :x: 10/15 | :x: 0/6 |
| 10 | OS command injection | :white_check_mark: 1/1 | :white_check_mark: 4/4 | - |
| 11 | Server-side template injection | - | :white_check_mark: 5/5 | :white_check_mark: 2/2 |
| 12 | Path traversal | :white_check_mark: 1/1 | :white_check_mark: 5/5 | - |
| 13 | Access control vulnerabilities | :white_check_mark: 9/9 | :white_check_mark: 4/4 | - |
| 14 | Authentication | :white_check_mark: 3/3 | :white_check_mark: 9/9 | :white_check_mark: 2/2 | 
| 15 | WebSockets | :white_check_mark: 1/1 | :white_check_mark: 2/2 | - |
| 16 | Web cache poisoning | - | :white_check_mark: 9/9 | :x: 3/4 | 
| 17 | Insecure deserialization | :white_check_mark: 1/1 | :white_check_mark: 6/6 | :white_check_mark: 3/3 |
| 18 | Information disclosure | :white_check_mark: 4/4 | :white_check_mark: 1/1 | - |
| 19 | Business logic vulnerabilities | :white_check_mark: 4/4 | :white_check_mark: 7/7 | :white_check_mark: 1/1 |
| 20 | HTTP Host header attacks | :white_check_mark: 2/2 | :white_check_mark: 4/4 | :white_check_mark: 1/1 |
| 21 | OAuth authentication | :white_check_mark: 1/1 | :white_check_mark: 4/4 | :white_check_mark: 1/1 |
| 22 | File upload vulnerabilities | :white_check_mark: 2/2 | :white_check_mark: 4/4 | :x: 0/1 |
| 23 | JWT  | :white_check_mark: 2/2 | :white_check_mark: 4/4 | :x: 1/2 |
| 24 | Essential skills | - | :x: 1/2 | - |
| 25 | prototype pollution | - | :white_check_mark: 9/9 | :x: 0/1 |
| 26 | GraphQL API vulnerabilities| :white_check_mark: 1/1 | :white_check_mark: 4/4 | - |
| 27 | Race conditions | :x: 0/1 | :x: 0/4 | :x: 0/1 |
| 28 | NoSQL injection | :white_check_mark: 2/2 | :white_check_mark: 2/2 | - |
| 29 | API testing | :white_check_mark: 1/1 | :white_check_mark: 3/3 | :white_check_mark: 1/1 |
| 30 | Web LLM attacks | :white_check_mark: 1/1 | :x: 1/2 | :x: 0/1 |
| 31 | Web cache deception |  :white_check_mark: 1/1 | :x: 2/3 | :x: 1/1 |
| x | Overall progress| :x: 58/59 | :x: 159/171 | :x: 26/39 |





installation of the necessary libraries
```
pip3 install requests re sys time socket pytesseract pyautogui http.client selenium bs4 PIL webbrowser pyjwt jwcrypto h2 certifi
```
```
apt install exiftool tesseract-ocr
```


In each case the script works the same way

Correct
```
python3 solution.py https://<ID>.web-security-academy.net <collab ID>9.oastify.com
```

Wrong (I assumed that there is no `/` sign at the end of the)
```
python3 solution.py https://<ID>.web-security-academy.net/ <collab ID>.oastify.com
python3 solution.py https://<ID>.web-security-academy.net http://<collab ID>.oastify.com
python3 solution.py https://<ID>.web-security-academy.net/ http://<collab ID>.oastify.com
python3 solution.py <ID>.web-security-academy.net http://<collab ID>.oastify.com
python3 solution.py <ID>.web-security-academy.net/ http://<collab ID>.oastify.com
```

