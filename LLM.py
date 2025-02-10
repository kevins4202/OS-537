import google.generativeai as genai
import os
import re
import pandas as pd
import anthropic
from openai import OpenAI
from llamaapi import LlamaAPI
import numpy as np


def getChars(text):
    j = 0
    while True:
        if j >= len(text):
            break
        text[j] = text[j].strip()

        pattern = r"\b\d{1,3}\.\s?\(?([A-Za-z])\)?"

        match = re.search(pattern, text[j])
        if match:
            text[j] = match.group(1)
        elif len(text[j]) != 1 or not text[j][-1].isalpha():
            text.pop(j)
            continue

        text[j] = text[j][-1].lower()
        if not text[j][0].isalpha():
            text.pop(j)
            continue
        j += 1
    return text


genai.configure(api_key=os.environ["GEMINI_API_KEY"])


class LLM:
    def __init__(self):
        self.context = "You are an expert in operating systems with extensive knowledge of topics such as process management, memory management, file systems, synchronization, virtualization, and operating system design principles. You are about to take a multiple choice exam designed to assess your expertise in these areas. The exam includes multiple operating systems concepts listed above."
        self.models = {
            "claude": [
                "claude-3-5-sonnet-latest",
                "claude-3-5-haiku-latest",
                "claude-3-opus-latest",
            ],
            "openai": [
                "o3-mini",
                "o1",
                "gpt-4o",
                "gpt-3.5-turbo",
                "o1-preview",
                "gpt-4o-mini",
                "gpt-4-turbo",
                "o1-mini",
            ],
            "llama": [
                "llama3.2-3b",
                "llama3.1-405b",
                "llama3-70b",
            ],
            "gemini": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.5-flash-8b"],
            "deepseek": ["deepseek-chat", "deepseek-reasoner"],
        }
        self.model_types = {}
        for model_type, models in self.models.items():
            for model_name in models:
                self.model_types[model_name] = model_type

        self.exam_info = pd.read_csv("exams.csv")
        self.exams = [
            "18-spring-mid",
            "21-fall-mid",
            "18-spring-final",
            "21-fall-final",
        ]

    def call_model(self, exams_path, models, exams, iterations):
        for model_name in models:
            try:
                model_type = self.model_types[model_name]
            except KeyError:
                print(f"Model {model_name} not found")
                continue

            for exam in exams:
                print("model", model_name, "exam", exam)
                df = pd.DataFrame()
                if os.path.exists(f"results/{model_name}_text_{exam}.csv"):
                    df = pd.read_csv(f"results/{model_name}_text_{exam}.csv")

                iteration = len(df.columns)
                while iteration < iterations:
                    answers = []
                    lst = sorted(os.listdir(exams_path + "/" + exam))
                    file_index = 0

                    print(lst)

                    while file_index < len(lst):
                        try:
                            file = lst[file_index]

                            if file == ".DS_Store":
                                file_index += 1
                                continue

                            with open(f"{exams_path}/{exam}/{file}", "r") as f:
                                data = f.read()
                                text = None

                                message = (
                                    "\n"
                                    + data
                                    + "\nDo not provide any explanation and answer with a single letter for each question. Carefully think about the number of questions on each page. For each question, answer in the format 'digit. letter'. For example, '1. a'.\n"
                                )

                                model = None
                                if model_type == "claude":
                                    model = anthropic.Anthropic(
                                        api_key=os.environ["CLAUDE_API_KEY"]
                                    )

                                    response = model.messages.create(
                                        max_tokens=1024,
                                        model=model_name,
                                        messages=[
                                            {
                                                "role": "user",
                                                "content": self.context + message,
                                            }
                                        ],
                                    )

                                    text = response.content[0].text.strip().split("\n")
                                elif model_type == "gemini":
                                    model = genai.GenerativeModel(model_name)

                                    response = model.start_chat(
                                        history=[
                                            {"role": "user", "parts": self.context},
                                            {
                                                "role": "model",
                                                "parts": "Thank you. Will you provide me with the problems?",
                                            },
                                        ]
                                    )
                                    response = response.send_message(message)

                                    text = response.text.strip().split("\n")
                                elif model_type == "llama":
                                    model = LlamaAPI(os.environ["LLAMA_API_KEY"])

                                    api_request_json = {
                                        "model": model_name,
                                        "messages": [
                                            {
                                                "role": "user",
                                                "content": [
                                                    {
                                                        "type": "text",
                                                        "text": self.context + message,
                                                    }
                                                ],
                                            },
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
                                    # print(response)
                                    text = (
                                        response["choices"][0]["message"]["content"]
                                        .strip()
                                        .split("\n")
                                    )
                                elif model_type == "openai":
                                    model = OpenAI()
                                    completion = model.chat.completions.create(
                                        model=model_name,
                                        messages=[
                                            {
                                                "role": "user",
                                                "content": self.context + message,
                                            }
                                        ],
                                    )
                                    text = (
                                        completion.choices[0]
                                        .message.content.strip()
                                        .split("\n")
                                    )
                                elif model_type == "deepseek":
                                    model = OpenAI(
                                        api_key=os.environ["DEEPSEEK_API_KEY"],
                                        base_url="https://api.deepseek.com",
                                    )
                                    response = model.chat.completions.create(
                                        model=model_name,
                                        messages=[
                                            {"role": "system", "content": self.context},
                                            {"role": "user", "content": message},
                                        ],
                                        stream=False,
                                    )

                                    text = response.choices[0].message.content
                                else:
                                    raise ValueError("Invalid model type")

                                print(file)
                                print(text)
                                text = getChars(text)
                                print(len(text), text)
                                if len(text) == 0:
                                    continue
                                answers.extend(text)
                                file_index += 1
                        except Exception as e:
                            print(e)
                            continue
                    print(answers)
                    print(len(answers))
                    num_questions = int(
                        self.exam_info.loc[
                            self.exam_info["exam"] == exam, "total_points"
                        ].values[0]
                    )
                    if num_questions == len(answers):
                        df[f"{exam}{iteration}"] = answers
                        iteration += 1
                        print(df)
                        df.to_csv(f"results/{model_name}_text_{exam}.csv", index=False)

    def get_results(self, models, exams):
        results = pd.DataFrame(index=exams)

        if os.path.exists(f"results.csv"):
            results = pd.read_csv(f"results.csv")
            results.set_index("exam", inplace=True)

        for model in models:
            dct = {}
            if model not in results.columns:
                results[model] = [-1.0 for _ in range(len(self.exams))]

            for exam in exams:
                outputs = pd.read_csv(f"results/{model}_text_{exam}.csv")
                answers = pd.read_csv(f"answers/{exam}.csv")

                if outputs.shape[0] != answers.shape[0]:
                    raise ValueError(
                        "Number of rows in outputs and answers do not match"
                    )

                dct[exam] = (
                    outputs[f"{exam}0"] == answers["answer"]
                ).sum() / answers.shape[0]

            for ex, v in dct.items():
                results.loc[ex, model] = v
                print(results)

        results.rename_axis("exam", inplace=True)

        results.to_csv(f"results.csv")


def main():
    models = ["o3-mini", "deepseek-chat", "deepseek-reasoner"]
    llm = LLM()
    llm.call_model("text", models, llm.exams[:], 1)

    llm.get_results(models, llm.exams)


if __name__ == "__main__":
    main()
