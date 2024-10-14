from pdf2image import convert_from_path
import os
 
# Store Pdf with convert_from_path function

 

def pdf_to_pngs(pdf_path, output_folder, dpi=300, display=True):
    # Open the PDF
    images = convert_from_path(pdf_path, size = (1190, 1540))
    
    # Create the output folder if it doesn't exist
    os.mkdir(output_folder)
    
    for i in range(len(images)):
       
      # Save pages as images in the pdf
        images[i].save(output_folder+ '/' + str(i) +'.png', 'PNG')
    

pdf_path = "exam_pdfs/"
output_folder = "images/"
for exam in ["18-spring-mid.pdf", "21-fall-mid.pdf", "21-fall-final.pdf", "18-spring-final.pdf"]:
    pdf_to_pngs(pdf_path + exam, output_folder + exam[:-4])