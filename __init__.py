import os, re
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

pdfs = r"./assets/pdf"
OUTPUT = r"./assets/output"

print("Clearing contents from output folder:")
for _, c in enumerate(os.listdir(OUTPUT)):
    for _, gc in enumerate(os.listdir(f"{OUTPUT}/{c}")):
        os.rmdir(os.path.join(OUTPUT, f"{c}/{gc}"))
        print(f"\tRemoved file: {gc}")

jpgs = {}

print("Begin transformation from PDF to JPG")
for _, c in enumerate(os.listdir(pdfs)):
    for _, gc in enumerate(os.listdir(f"{pdfs}/{c}")):
        print(f"Current directory: {c}/{gc}")
        gc_stem = os.path.splitext(gc)[0]

        out_dir = f"{OUTPUT}/{c}/{gc_stem}"
        os.mkdir(out_dir)

        pages = convert_from_path(f"{pdfs}/{c}/{gc}", output_folder=out_dir, fmt="jpeg")

        print(f"\tTransformed {gc_stem} to image(s)")
        jpgs[gc_stem] = pages

for _, c in enumerate(os.listdir(OUTPUT)):
    for _, gc in enumerate(os.listdir(f"{OUTPUT}/{c}")):
        for _, ggc in enumerate(os.listdir(f"{OUTPUT}/{c}/{gc}")):
            old_name = str(ggc)
            new_name = "page-" + old_name.split("-")[-1]

            old_path = os.path.join(OUTPUT, f"{c}/{gc}/{old_name}")
            new_path = os.path.join(OUTPUT, f"{c}/{gc}/{new_name}")

            print("Renaming " + old_name + " to " + new_name)
            os.rename(old_path, new_path)

for _, c in enumerate(os.listdir(OUTPUT)):
    for _, gc in enumerate(os.listdir(f"{OUTPUT}/{c}")):
        text = ""
        for _, ggc in enumerate(os.listdir(f"{OUTPUT}/{c}/{gc}")):
            image_path = os.path.join(OUTPUT, f"{c}/{gc}/{ggc}")

            print(f"Appending text of {ggc}")
            text += pytesseract.image_to_string(Image.open(image_path), lang="pan")

        print(f'Writing text of akhar "{gc}" to akhar_{gc}.txt')
        with open(f"{OUTPUT}/{c}" + f"akhar_{gc}.txt", "w") as file:
            file.write(text)

print("Done!")
