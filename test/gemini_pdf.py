import google.generativeai as genai
import os
import PIL.Image

genai.configure(api_key=os.environ['key_gemini'])

model = genai.GenerativeModel('gemini-1.5-pro')

context = "You are an undergraduate Operating Systems student who is going to be taking an exam. Answer the questions on each page. You are only to answer with the lowercase letter representing the correct answer. Do not include any other information, code, or explanation in your response. For example, if the answer to question 1 is A, you should only respond with 'a'. If the answer to question 2 is B, you should only respond with 'b'. If the answer to question 3 is C, you should only respond with 'c'. If the answer to question 4 is D, you should only respond with 'd'. If the answer to question 5 is E, you should only respond with 'e'."

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
        
        response = model.generate_content([file, context])
        text = response.candidates[0].content.parts[0].text.strip()
        answers = text.split("\n")
        print(answers)
        print(len(answers))
            
    #     df[f'gemini{i}'] = answers
    # df.to_csv(f'{exam}.csv', index=False)

