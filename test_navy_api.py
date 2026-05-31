import requests

url = "https://api.navy/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-navy-CPFLtUUlVBr6LKSuK3LrUDYCVXdsua-OgMkdJ6wPcBY"
}
data = {
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello, tell me a fun fact."}]
}

try:
    response = requests.post(url, json=data, headers=headers)
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error:", e)
