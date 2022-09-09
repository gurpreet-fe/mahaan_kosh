import os, re
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

pdfs = r"./assets/pdf/urra.pdf"
OUTPUT = r"./assets/output/"

print("Clearing contents from output folder:")
for i, f in enumerate(os.listdir(OUTPUT)):
    os.remove(os.path.join(OUTPUT, f))
    print("\tRemoved file " + str(i + 1))

print("Transforming PDFs to images")
pages = convert_from_path(pdfs, output_folder=OUTPUT, fmt="jpeg")

print("Renaming")
for i, f in enumerate(os.listdir(OUTPUT)):
    old_name = str(f)
    new_name = "page-" + old_name[-7:]

    print("Renaming " + old_name + " to " + new_name)
    os.rename(os.path.join(OUTPUT, old_name), os.path.join(OUTPUT, new_name))

text = ""
for i, f in enumerate(os.listdir(OUTPUT)):
    print("Appending text of page" + str(i))
    text += pytesseract.image_to_string(Image.open(os.path.join(OUTPUT, f)), lang="pan")

print("Writing text to output.txt")
with open(OUTPUT + "output.txt", "w") as file:
    file.write(text)

print("Done!")
