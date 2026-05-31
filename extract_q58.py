import requests
import json

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
                    "text": "Extract the matching question data from this image. Return a JSON object with 'table' and 'choices'. The 'table' should be an array of dictionaries with 'left' (the prompt) and 'right' (the correct answer). 'choices' should be an empty list, as it's a matching question."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://reponseccna.com/wp-content/uploads/2021/12/2021-11-13_112035.jpg"
                    }
                }
            ]
        }
    ],
    "max_tokens": 1000
}

response = requests.post("https://api.navy/v1/chat/completions", headers=headers, json=payload)
print(response.json())
