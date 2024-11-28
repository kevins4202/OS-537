import json
import os
import re
from openai import OpenAI
from llamaapi import LlamaAPI

context = "You are an undergraduate Operating Systems student who is going to be taking an exam. Think carefully about the number of questions on each page."

import pandas as pd

exam_info = pd.read_csv("exams.csv")
# print((exam_info.loc[exam_info['exam'] == '18-spring-mid', 'total_points'].values[0]))
exams = ["18-spring-mid", "21-fall-mid", "18-spring-final", "21-fall-final"]

def getChars(text):
    j = 0
    while True:
        if j >= len(text):
            break
        text[j] = text[j].strip()

        pattern = r"\b\d{1,3}\.\s\(?([A-Za-z])\)?\s*"

        match = re.search(pattern, text[j])
        if match:
            text[j] = match.group(1)
        elif len(text[j]) != 1 or not text[j][-1].isalpha():
            text.pop(j)
            continue

        text[j] = text[j][-1].lower()
        if text[j] not in 'abcde':
            text.pop(j)
            continue
        j += 1
    return text

# For all files in the images folder, upload all of them to the API and generate content, joined into a single list
for exam in exams[:]:
    print(exam)
    print(exam_info.loc[exam_info["exam"] == exam, "total_points"].values[0])

    if os.path.exists(f"results/llama3.1_text_{exam}.csv"):
        df = pd.read_csv(f"results/llama3.1_text_{exam}.csv")
    else:
        df = pd.DataFrame()
    i = 2
    while i < 5:
        answers = []
        lst = sorted(os.listdir("text/" + exam))
        k = 0
        while k < len(lst):
            try:
                file = lst[k]
                print(file)

                model = LlamaAPI(os.environ["LLAMA_API_KEY"])

                with open(f"text/{exam}/{file}", "r") as file:
                    data = file.read()

                    api_request_json = {
                        # "model": "llama3.2-3b",
                        "model": "llama3.1-70b",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "You are an undergraduate Operating Systems student who is going to be taking an exam. Answer the questions on each page. Do not include any other information, code, or explanation in your response. You are only to answer with the lowercase letter representing the correct answer.",
                                    }
                                ],
                            },
                            {"role": "user", "content": data},
                        ],
                        "functions": [
                            {
                                "name": "take_exam",
                                "description": "take the exam",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "exam_questions": {
                                            "type": "string",
                                            "description": "The exam questions",
                                        },
                                    },
                                },
                            }
                        ],
                        "stream": False,
                        "function_call": "take_exam",
                    }
                    response = model.run(api_request_json).json()

                    print(response)

                    text = response['choices'][0]['message']['content']

                    text = text.strip().split("\n")
                    print(text)

                    text = getChars(text)

                    print(len(text), text)

                    answers.extend(text)
                    k += 1
            except Exception as e:
                print(e)
        print(answers)
        print(len(answers))
        num_questions = int(
            exam_info.loc[exam_info["exam"] == exam, "total_points"].values[0]
        )
        if num_questions == len(answers):
            df[f"{exam}{i}"] = answers
            i += 1
            print(df)
            df.to_csv(f"results/llama3.1_text_{exam}.csv", index=False)