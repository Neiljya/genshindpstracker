import os
import subprocess

"""
This file trains tesseract on the generated images:
- For each image, generate a .box file
- Extract the character set (unicharset) from the .box files using `unicharset_extractor`
- Generate necessary files for training
- Generate shapetable using cntraining
- Combine the trainnig data into a final tesseract file in `combine_tessdata`
"""

train_dir = 'training_images'
tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Tesseract's installation path

def generate_box_files(image_dir):
    for image_file in os.listdir(image_dir):
        if image_file.endswith('.png'):
            image_path = os.path.join(image_dir, image_file)
            base_name = os.path.splitext(image_file)[0]
            box_file = os.path.join(image_dir, base_name + '.box')

            # Generate box file
            subprocess.run([tesseract_cmd, image_path, base_name, 'batch.nochop', 'makebox'])
            print(f"Generated box file: {box_file}")

def train_tesseract(image_dir):
    os.chdir(image_dir)

    # Extract unicharset from box files
    subprocess.run(['unicharset_extractor'] + [f for f in os.listdir() if f.endswith('.box')])
    print("Generated unicharset.")

    # Generate .tr files
    for image_file in os.listdir():
        if image_file.endswith('.png'):
            base_name = os.path.splitext(image_file)[0]
            subprocess.run([tesseract_cmd, image_file, base_name, 'box.train'])
            print(f"Generated .tr file for: {image_file}")

    with open('font_properties', 'w') as f:
        f.write('custom_font 0 0 0 0 0\n')
    print("Created font_properties file.")

    subprocess.run(
        ['mftraining', '-F', 'font_properties', '-U', 'unicharset', '-O', 'output.unicharset'] + [f for f in
                                                                                                      os.listdir() if
                                                                                                      f.endswith(
                                                                                                          '.tr')])
    print("Generated inttemp, normproto, and pffmtable.")

    subprocess.run(['cntraining'] + [f for f in os.listdir() if f.endswith('.tr')])
    print("Generated shapetable.")

    # Combine tessdata
    for f in ['inttemp', 'normproto', 'pffmtable', 'shapetable']:
        subprocess.run(['combine_tessdata', f])
    print("Combined tessdata.")

if __name__ == "__main__":

    output_dir = 'trained_data'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Step 1: Generate box files for training images
    generate_box_files(train_dir)

    # Step 2: Train Tesseract with the generated data
    train_tesseract(train_dir)
