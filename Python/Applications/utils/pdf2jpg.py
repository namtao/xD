# Import libraries
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os

def pdf2jpg(pdfPath, jpgPath):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pages = convert_from_path(
        pdfPath, 500, poppler_path=r'C:\Projects\Python\Library\poppler\bin')
    image_counter = 1
    for page in pages:
        filename = "page_"+str(image_counter)+".jpg"
        page.save(os.path.join(jpgPath, filename), 'JPEG')
        image_counter = image_counter + 1

if __name__ == "__main__":
    pdfPath = sys.argv[1]
    jpgPath = sys.argv[2]
    pdf2jpg(pdfPath, jpgPath)
    
    
