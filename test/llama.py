from llamaapi import LlamaAPI
import os
import json

client = LlamaAPI(os.environ['llama_api'])
context = "You are an undergraduate Operating Systems student who is going to be taking an exam. Answer the questions on each page. You are only to answer with the lowercase letter representing the correct answer. Do not include any other information, code, or explanation in your response. For example, if the answer to question 1 is A, you should only respond with 'a'. If the answer to question 2 is B, you should only respond with 'b'. If the answer to question 3 is C, you should only respond with 'c'. If the answer to question 4 is D, you should only respond with 'd'. If the answer to question 5 is E, you should only respond with 'e'."

import pandas as pd

exams = ["18-spring-mid", "21-fall-mid", "18-spring-final", "21-fall-final"]

for exam in exams[:1]:  
    df = pd.read_csv(f'{exam}.csv')

    for i in range(1):
        answers = []
        for file in os.listdir("text/" + exam):
            with open(f'text/{exam}/{file}', 'r') as file:
                datum = file.read()
                api_request_json = {
                    "messages": [
                        {"role": "user", "content": context + "\n\n" + datum},
                    ],
                }
                print(datum)

                data = client.run(api_request_json).json()
                # print(type(data))
                splitted = data['choices'][0]['message']['content'].strip().split("\n")
                print(splitted)
                for i in range(len(splitted)):
                    if len(splitted[i]) == 0:
                        splitted.pop(i)
                        i -= 1
                    if len(splitted[i]) > 1:
                        splitted[i] = splitted[i][-1]
                answers += splitted
                print(f'add length {len(splitted)}')
                print(answers)
                print(len(answers))