import google.generativeai as genai
import os
import PIL.Image

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

model = genai.GenerativeModel('gemini-1.5-pro')

context = "You are an undergraduate Operating Systems student who is going to be taking an exam. Think carefully about the number of questions on each page. You are only to answer with the lowercase letter representing the correct answer. Do not include any question numbers, code, or explanation in your response. For example, if the answer to question 1 is A, you should only respond with 'a'. Think about each question before answering. There are 150 questions total."

import pandas as pd

exams = ["18-spring-mid", "21-fall-mid", "18-spring-final", "21-fall-final"]

df = pd.DataFrame()
# For all files in the images folder, upload all of them to the API and generate content, joined into a single list
for exam in exams[0:1]:  
    for i in range(1):
        answers = []
        prompt = [context]
        
        file = genai.upload_file(path=f'exam_pdfs/{exam}.pdf',
                                display_name="Gemini 1.5 PDF")
        
        response = model.generate_content([context, file])
        text = response.candidates[0].content.parts[0].text.strip()
        answers = text.split("\n")
        print(answers)
        print(len(answers))
            
    #     df[f'gemini{i}'] = answers
    # df.to_csv(f'{exam}.csv', index=False)

