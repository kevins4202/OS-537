import anthropic
import os, re
import pandas as pd

api_key = os.environ["CLAUDE_API_KEY"]
# Initialize the Anthropic client

exams = ["18-spring-mid", "21-fall-mid", "18-spring-final", "21-fall-final"]
context = "You are an undergraduate Operating Systems student who is going to be taking an exam. Think carefully about the number of questions on each page."
exam_info = pd.read_csv("exams.csv")

models = [
    "claude-3-5-sonnet-latest",
]

for m in models:
    for exam in exams[2:3]:
        if os.path.exists(f"results/{m}_text_{exam}.csv"):
            df = pd.read_csv(f"results/{m}_text_{exam}.csv")
        else:
            df = pd.DataFrame()
        i = 0
        while i < 5:
            model = anthropic.Anthropic(api_key=api_key)
            answers = []
            lst = sorted(os.listdir("text/" + exam))
            print(exam, lst)
            k = 0
            while k < len(lst):
                try:
                    file = lst[k]
                    if "txt" not in file:
                        k += 1
                        continue
                    print("file name: ", file)
                    with open(f"text/{exam}/{file}", "r") as file:
                        data = file.read()

                        response = model.messages.create(
                            model="claude-3-5-haiku-latest",
                            max_tokens=1024,
                            messages=[
                                {
                                    "role": "user",
                                    "content": 
                                    data
                                    + context + "\n"
                                    + "\nFor each question, answer in the format 'QUESTION_NUMER DOT SPACE ANSWER_CHOICE'. Do not provide any explanation and answer with a single letter for each question. Carefully think about the number of questions on each page.",
                                }
                            ],
                        )

                        text = response.content[0].text.strip().split("\n")
                        print(text)

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
                            if text[j] not in "abcde":
                                text.pop(j)
                                continue
                            j += 1

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
                df.to_csv(f"results/{m}_text_{exam}.csv", index=False)
