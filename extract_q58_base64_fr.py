import requests
import json
import base64

# Download image
img_url = "https://ccnareponses.com/wp-content/uploads/2021/12/2021-11-13_112035.jpg"
response = requests.get(img_url)
img_data = response.content

# Encode to base64
base64_image = base64.b64encode(img_data).decode('utf-8')

api_key = "sk-navy-CPFLtUUlVBr6LKSuK3LrUDYCVXdsua-OgMkdJ6wPcBY"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Extract exactly the text in French from the image. Do not translate. Return the answer in pure JSON format: a list of dictionaries with 'left' (the item to drag, which is the long sentence) and 'right' (the correct destination it belongs to, which is the short category like 'Menace matérielle')."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    "max_tokens": 1000
}

r = requests.post("https://api.navy/v1/chat/completions", headers=headers, json=payload)
print(r.json()['choices'][0]['message']['content'])
