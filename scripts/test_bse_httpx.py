import httpx, sys
from dotenv import load_dotenv; load_dotenv()
import os

url = "https://starmfv2demo.bseindia.com/api/login"
payload = {
    "data": {
        "username": os.getenv("STARMF_LOGIN_USERNAME"),
        "password": os.getenv("STARMF_LOGIN_PASSWORD"),
    }
}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

r = httpx.post(url, json=payload, headers=headers, timeout=30, verify=True)
print("STATUS:", r.status_code)
print("CONTENT-TYPE:", r.headers.get("content-type"))
body = r.text
# mask token if present
import re
body = re.sub(r'(access_token["\s:]+)["\']?[\w\.\-]+["\']?', r'\1<TOKEN>', body)
print("BODY:", body[:1000])
