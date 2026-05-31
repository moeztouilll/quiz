import json
import base64
import requests
import urllib.request
import os

qs_path = r"C:\Users\MSI\Downloads\quiz\public\questions.json"
with open(qs_path, "r", encoding="utf-8") as f:
    qs = json.load(f)

api_key = "sk-navy-CPFLtUUlVBr6LKSuK3LrUDYCVXdsua-OgMkdJ6wPcBY"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# The images that contain answers (from manual inspection)
# Q27 answer: 2024-10-14_061752.jpg
# We will just manually supply the URL of the answer image for the known matching questions.

answer_images = {
    27: "https://ccnareponses.com/wp-content/uploads/2021/12/2024-10-14_061752.jpg",
    33: "https://ccnareponses.com/wp-content/uploads/2021/12/2021-11-11_235847.jpg",
    35: "https://ccnareponses.com/wp-content/uploads/2021/12/2021-11-12_000004.jpg",
    82: "https://ccnareponses.com/wp-content/uploads/2021/12/2021-12-20_221916.jpg", # Q83 is actually Q82? Let's check
    113: "https://itexamanswers.net/wp-content/uploads/2020/06/i304957v1n1_209418-1591171569.7915.png",
    116: "https://ccnareponses.com/wp-content/uploads/2021/12/2023-04-10_103226.jpg",
    117: "https://itexamanswers.net/wp-content/uploads/2020/01/2021-09-18_110901.jpg"
}

for q in qs:
    num = q.get("original_num", q["num"])
    if num in answer_images:
        url = answer_images[num]
        print(f"Processing Q{num} with image {url}")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                img_data = response.read()
            b64 = base64.b64encode(img_data).decode('utf-8')
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract exactly the text in French from the image. Do not translate. Return the answer in pure JSON format: a list of dictionaries with 'left' (the item to drag, the sentence or characteristic) and 'right' (the correct destination it belongs to, like the category). Only output the JSON."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{b64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 1000
            }
            
            r = requests.post("https://api.navy/v1/chat/completions", headers=headers, json=payload)
            content = r.json()['choices'][0]['message']['content']
            
            # Clean json
            content = content.replace("```json", "").replace("```", "").strip()
            table_data = json.loads(content)
            
            q["table"] = table_data
            print(f"Success for Q{num}")
        except Exception as e:
            print(f"Error Q{num}: {e}")

with open(qs_path, "w", encoding="utf-8") as f:
    json.dump(qs, f, ensure_ascii=False, indent=2)

print("Finished processing matching questions.")
