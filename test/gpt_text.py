import time
from openai import OpenAI
import os
import pandas as pd
import re

context = "You are an undergraduate Operating Systems student who is going to be taking an exam. Think carefully about the number of questions on each page."
exam_info = pd.read_csv("exams.csv")
exams = ["18-spring-mid", "21-fall-mid", "18-spring-final", "21-fall-final"]

class AnswerList:
    answers: list[chr]

models = ["gpt-4o", "o1-preview"]
for m in models[:1]:
    for exam in exams[2:]:
        print(exam)
        print(exam_info.loc[exam_info['exam'] == exam, 'total_points'].values[0])

        df = pd.DataFrame()
        i = 0
        while i < 5:

            answers = []
            lst = sorted(os.listdir("text/" + exam))
            k = 0
            while k < len(lst):
                try:
                    file = lst[k]
                    print("file name", file)
                    with open(f'text/{exam}/{file}', 'r') as file:
                        model  = OpenAI()
                        data = file.read()

                        completion = model.chat.completions.create(
                            model=m,
                            messages=[
                                {
                                "role": "system", 
                                "content": [
                                        {
                                            "type": "text",
                                            "text": "You are an undergraduate Operating Systems student who is going to be taking an exam. Answer the questions on each page. Do not include any other information, code, or explanation in your response. You are only to answer with the lowercase letter representing the correct answer."
                                        }
                                    ]
                                },
                                {
                                    "role": "user",
                                    "content": data
                                }
                            ]
                        ) 
                        
                        text = completion.choices[0].message.content.strip()
                        if "\n" in text:
                            text = text.split("\n")
                        else:
                            if " " in text:
                                text = text.replace(" ", "")
                            text = [text]
                        print("text", text)
                        
                        j = 0
                        
                        while True:
                            if j >= len(text):
                                break
                            text[j] = text[j].strip()

                            pattern = r"\b\d{1,3}[.:]\s\(?([A-Za-z])\)?\s*"

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

                        print(len(text), text)

                        answers.extend(text)
                        k+=1
                        time.sleep(1)
                except Exception as e:
                    print(e)
            print(answers)
            print(len(answers))
            num_questions = int(exam_info.loc[exam_info['exam'] == exam, 'total_points'].values[0])
            if num_questions == len(answers):
                df[f'{exam}{i}'] = answers
                i+=1
                print(df)
                df.to_csv(f'results/{m}_text_{exam}.csv', index=False)
