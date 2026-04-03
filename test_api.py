import urllib.request
import urllib.error
import json

url = "https://finance-backend-api-vn1t.onrender.com/api/auth/register"
data = json.dumps({"username": "sysadmin", "email": "sysadmin@test.com", "password": "password123"}).encode("utf-8")
headers = {"Content-Type": "application/json"}

req = urllib.request.Request(url, data=data, headers=headers, method="POST")
try:
    with urllib.request.urlopen(req) as response:
        print("Status", response.status)
        print("Response:", response.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("Error Status:", e.code)
    print("Error Response:", e.read().decode("utf-8"))
except Exception as e:
    print("Failed completely:", str(e))
