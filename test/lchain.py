import openai
from langchain_openai import OpenAI
from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain

import os

# Set your OpenAI API key
llm = OpenAI(model="gpt-4", api_key=os.environ['openai'])

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

file_path = os.getcwd().replace('test', '') + '/exam_pdfs/18-spring-mid.pdf'
loader = PyPDFLoader(file_path)
documents = loader.load()

# pdf_content = "\n".join([doc.page_content for doc in documents])

# Generate output using the OpenAI model
chain = load_qa_chain(llm,verbose=True)
question = input("Enter your question here : ")
response = chain.run(input_documents=documents, question=question)
print(response) 