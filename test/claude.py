import anthropic
import os
import pandas as pd

api_key = os.environ["key_claude"]
    # Initialize the Anthropic client
client = anthropic.Anthropic(api_key = api_key)
exams = ["18-spring-mid", "21-fall-mid", "18-spring-final", "21-fall-final"]

df = pd.DataFrame()
# For all files in the images folder, upload all of them to the API and generate content, joined into a single list
for exam in exams[0:1]:  
    for i in range(1):
        answers = []
        for file in os.listdir("text/" + exam):
            with open(f'text/{exam}/{file}', 'r') as file:
                data = file.read()

                # sample_file = genai.upload_file(path=f'images/{exam}/{file}',
                #                     display_name=f'{exam} {file}')
                # print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

                print(data)
                context = "You are an undergraduate Operating Systems student who is going to be taking an exam. Answer the questions on each page. You are only to answer with the lowercase letter representing the correct answer. Do not include any other information, code, or explanation in your response. For example, if the answer to question 1 is A, you should only respond with 'a'. If the answer to question 2 is B, you should only respond with 'b'. If the answer to question 3 is C, you should only respond with 'c'. If the answer to question 4 is D, you should only respond with 'd'. If the answer to question 5 is E, you should only respond with 'e'."
                response = client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    messages=[{"content": context + "\n\n" + data}]
                )
                print(response)
                answers.extend(response.strip().split("\n"))
        print(answers)
        print(len(answers))
