import pymupdf
import fitz
import os

def pdf_to_text(pdf_path, output_folder):
    doc = pymupdf.open(pdf_path) # open a document
    os.mkdir(output_folder)
    
    for i, page in enumerate(doc): # iterate the document pages
        out = open(f'{output_folder}/{i}.txt', "wb") # create a text output
        text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
        out.write(text) # write text of page
        out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
        
        out.close()

for exam in ["18-spring-mid.pdf", "21-fall-mid.pdf", "18-spring-final.pdf", "21-fall-final.pdf"][:1]:
    pdf_to_text("exam_pdfs/" + exam, "test_text/" + exam[:-4])