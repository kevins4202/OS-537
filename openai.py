from openai import OpenAI

client = OpenAI(
  organization='org-BubNBXFIjssYICdgwStQNtNn',
  project='proj_JCI4LO5G0sDnAk0HTOK6v7zT',
  api_key='sk-proj-x35ewBhZUapE12kaV58fT3BlbkFJuzfItKJebHauhUHOGdKF'
)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "user",
      "content": "Analyze the pros and cons of remote work vs. office work"
    }
  ],
  temperature=0.8,
  max_tokens=64,
  top_p=1
)

print(response)