import fitz
import os
from PIL import Image
import matplotlib.pyplot as plt

def pdf_to_pngs(pdf_path, output_folder, dpi=300, display=False):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    # Create the output folder if it doesn't exist
    os.mkdir(output_folder)
    
    images = []

    # Iterate through each page
    for page_num in range(len(doc)):
        # Get the page
        page = doc[page_num]
        
        # Convert page to pixmap (image)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
        
        # Define output PNG file name
        output_file = os.path.join(output_folder, f"page_{page_num + 1}.png")
        
        # Save the pixmap as PNG
        pix.save(output_file)
        
        print(f"Saved page {page_num + 1} as {output_file}")
        
        # Open the saved image and append to list
        if display:
            img = Image.open(output_file)
            images.append(img)
    
    # Close the document
    doc.close()
    
    print("Conversion completed.")
    
    # Display the images
    if display:
        for i, img in enumerate(images):
            plt.figure(figsize=(10, 14))
            plt.imshow(img)
            plt.axis('off')
            plt.title(f"Page {i + 1}")
            plt.show()

pdf_path = "exam_pdfs/"
output_folder = "images/"
for exam in ["18-spring-mid.pdf", "18-spring-final.pdf", "21-fall-mid.pdf", "21-fall-final.pdf"]:
    pdf_to_pngs(pdf_path + exam, output_folder + exam[:-4])