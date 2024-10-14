import base64
import os
from PIL import Image
from openai import OpenAI
import requests

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
exams = ["18-spring-mid", "21-fall-mid", "18-spring-final", "21-fall-final"]

client = OpenAI()

def call_exam(exam):
    content = [
        {
          "type": "text",
          "text": "You are an undergraduate Operating Systems student who is going to be taking an exam. Answer the questions on each page. You are only to answer with the lowercase letter representing the correct answer. Do not include any other information, code, or explanation in your response. For example, if the answer to question 1 is A, you should only respond with 'a'. If the answer to question 2 is B, you should only respond with 'b'. If the answer to question 3 is C, you should only respond with 'c'. If the answer to question 4 is D, you should only respond with 'd'. If the answer to question 5 is E, you should only respond with 'e'.",
        },
    ]

    dir = os.getcwd() + f'/images/{exam}'
    lst = sorted(os.listdir(dir))
    print(lst)

    ret = []

    for file in lst[2:3]:
        print(file)
        img = encode_image(f'{dir}/{file}')
        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{img}"
                }
            }
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                "role": "user",
                "content": content
                }
            ]
        )

        # print(response.choices[0].message.content)
        res = response.choices[0].message.content.split("\n")
        for i in range(len(res)):
            res[i] = res[i].strip()
        print(len(res))
        ret.extend(res)

    return ret

def call_exam_post(exam):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
    }

    dir = os.getcwd() + f'/images/{exam}'
    lst = sorted(os.listdir(dir))
    print(lst)

    ret = []

    for file in lst[7:8]:
        print(file)
        
        Image.open(f'{dir}/{file}').show()
        
        img = encode_image(f'{dir}/{file}') 
        content = [
        {
          "type": "text",
          "text": "You are an undergraduate Operating Systems student who is going to be taking an exam. Answer the questions on each page. You are only to answer with the lowercase letter representing the correct answer. Do not include any other information, code, or explanation in your response.",
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{img}"
            }
        }
        ]
        

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                "role": "user",
                "content": content
                }
            ]
        }

        res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        res = res.json()['choices'][0]['message']['content'].split("\n")
        print(res)

        for i in range(len(res)):
            res[i] = res[i].strip()[-1]
        print(len(res))
        print()
        ret.extend(res)

    return ret

    

results = []

for i in range(1):
    # result = call_exam(exams[i])
    result = call_exam_post(exams[i])
    results.append(result)

print(results)

print("\n\n\n\n\n".join(["".join(l) for l in results]))
for l in results:
    print(len(l))