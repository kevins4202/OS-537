import time
from openai import OpenAI
from openai.types.beta.threads.message_create_params import (
    Attachment,
    AttachmentToolFileSearch,
)
import os

filename = os.getcwd()+"/exam_pdfs/18-spring-mid.pdf"
prompt = "You are an undergraduate Operating Systems student who is going to be taking an exam. Answer the questions on each page. You are only to answer with the lowercase letter representing the correct answer. Do not include any other information, code, or explanation in your response. For example, if the answer to question 1 is A, you should only respond with 'a'. If the answer to question 2 is B, you should only respond with 'b'. If the answer to question 3 is C, you should only respond with 'c'. If the answer to question 4 is D, you should only respond with 'd'. If the answer to question 5 is E, you should only respond with 'e'."
client = OpenAI()

pdf_assistant = client.beta.assistants.create(
    model="gpt-4o",
    description="An assistant to take OS exams.",
    tools=[{"type": "file_search"}],
    name="OS537",
)

# Create thread
thread = client.beta.threads.create()

file = client.files.create(file=open(filename, "rb"), purpose="assistants")

# Create assistant
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    attachments=[
        Attachment(
            file_id=file.id, tools=[AttachmentToolFileSearch(type="file_search")]
        )
    ],
    content=prompt,
)

response = None
while not response:
    time.sleep(2)  # Wait for a couple of seconds before checking again
    # Fetch the latest messages in the thread
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    
    # Look for a message from the assistant
    for msg in messages:
        if msg.role == "assistant":
            response = msg
            break

# Print the assistant's response content
if response:
    print(response['content'])
else:
    print("No response from the assistant yet.")