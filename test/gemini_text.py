import google.generativeai as genai
import os

genai.configure(api_key=os.environ['GEMINI_API_KEY'])



context = "You are an undergraduate Operating Systems student who is going to be taking an exam. Think carefully about the number of questions on each page."

import pandas as pd

exam_info = pd.read_csv("exams.csv")
# print((exam_info.loc[exam_info['exam'] == '18-spring-mid', 'total_points'].values[0]))
exams = ["18-spring-mid", "21-fall-mid", "18-spring-final", "21-fall-final"]
df = pd.read_csv("gemini_text.csv")
# For all files in the images folder, upload all of them to the API and generate content, joined into a single list
for exam in exams[1:4]:
    print(exam)
    print(exam_info.loc[exam_info['exam'] == exam, 'total_points'].values[0])
    i = 0
    while i < 5:
        model = genai.GenerativeModel('gemini-1.5-pro')
        answers = []
        lst = sorted(os.listdir("text/" + exam))
        k = 0
        while k < len(lst):
            try:
                file = lst[k]
                print(file)
                with open(f'text/{exam}/{file}', 'r') as file:
                    data = file.read()

                    # sample_file = genai.upload_file(path=f'images/{exam}/{file}',
                    #                     display_name=f'{exam} {file}')
                    # print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
                    chat = model.start_chat(
                        history=[
                            {"role": "user", "parts": context},
                            {"role": "model", "parts": "Thank you. Will you provide me with the problems?"},
                        ]
                    )
                    response = chat.send_message("How many individual multiple choice questions are on this page? Think carefully and slowly.")
                    # print(response.text)
                    response = chat.send_message("You are only to answer with the lowercase letter representing the correct answer. Do not include any question numbers, code, or explanation in your response. For example, if the answer to question 1 is A, you should only respond with 'a'. Think about each question before answering.")
                    # print(response.text)
                    response = chat.send_message("Now, begin the exam and answer the questions I have provided.\n" +data)
                    # print(response.text)

                    # response = model.generate_content(context + "\n" + data)
                    # text = response.candidates[0].content.parts[0].text.strip()
                    text = response.text.strip().split("\n")
                    print(text)
                    for j in range(len(text)):
                        text[j] = text[j].strip()
                        if text[j] == "" or not text[j][-1].isalpha():
                            text.pop(j)
                            j-=1

                        text[j] = text[j][-1]

                    print(len(text), text)

                    answers.extend(text)
                    k+=1
            except:
                pass
        print(answers)
        print(len(answers))
        num_questions = int(exam_info.loc[exam_info['exam'] == '18-spring-mid', 'total_points'].values[0])
        if num_questions == len(answers):
            df[f'{exam}{i}'] = answers
            i+=1
            print(df)
            df.to_csv(f'gemini_text.csv', index=False)
            
    #     df[f'gemini{i}'] = answers


