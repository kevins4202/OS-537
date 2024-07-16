import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyACQFe9RG5raYIFaGZl1z_LlKb8Jnb_0BE")

model = genai.GenerativeModel('gemini-1.5-pro')

context = "You are an undergraduate Operating Systems student who is going to be taking an exam. You are only to answer with the lowercase letter representing the correct answer. Do not include any other information or explanation in your response. Answer all questions on the page. The page will be inputted as a PNG image. Here it is. Good luck!"

# TEXT INPUT TEST
# question = "Problem I: A program’s main function is as follows: \nint main(int argc, char *argv[]) {\nchar *str = argv[1];\nwhile (1)\nprintf(str);\nreturn 0;\n}\n\n Two processes, both running instances of this program, are currently running (you can assume nothing else of relevance is, except perhaps the shell itself). The programs were invoked as follows, assuming a “parallel command” as per project 2a (the wish shell):\n\nwish> main a && main b\n\nBelow are possible (or impossible?) screen captures of some of the output from the beginning of the run of the programs. Which of the following are possible? To answer: Fill in A for possible, B for not possible.\n\n1. abababab\n\n2. aaaaaaaa"
# from pypdf import PdfReader

# reader = PdfReader("18-spring-mid.pdf")
# text = '\n'.join([page.extract_text() for page in reader.pages])

# IMAGE INPUT TEST

# sample_file = genai.upload_file(path="output_images/page_1.png",
#                             display_name="Exam Page 1")

# print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
# # print(text)
# response = model.generate_content([sample_file, context])

# # response = model.generate_content(context + "\n\n" + text)
# print(response.text.strip().split("\n"))

import pandas as pd

exams = ["18-spring-mid", "18-spring-final", "21-fall-mid", "21-fall-final"]

df = pd.DataFrame(columns=exams.append("answer"))
# For all files in the images folder, upload all of them to the API and generate content, joined into a single list
for exam in exams[:1]:  
    answers = []
    for file in os.listdir("images/" + exam):
        sample_file = genai.upload_file(path=f'images/{exam}/{file}',
                            display_name=f'{exam} {file}')
        print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
        response = model.generate_content([sample_file, context])

        answers.append(response.text.strip().split("\n"))
    df[exam] = answers

df.to_csv("gemini_answers.csv", index=False)

