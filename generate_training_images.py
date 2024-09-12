from PIL import Image, ImageDraw, ImageFont
import os


# Function to create synthetic images with custom text
def create_synthetic_image(text, font_path, font_size, image_path):
    font = ImageFont.truetype(font_path, font_size)
    # Adjust the image size based on the text and font size
    text_bbox = font.getbbox(text)
    image_width = text_bbox[2] - text_bbox[0]
    image_height = text_bbox[3] - text_bbox[1]
    image = Image.new('RGB', (image_width + 20, image_height + 20), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, font=font, fill=(0, 0, 0))
    image.save(image_path)


# Example usage
if __name__ == "__main__":
    font_path = 'font/zh-cn.ttf'
    font_size = 48
    output_dir = 'training_images'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    texts = ['3453445', '51890', 'A dps text 12345', 'Another dps text 67890', 'More dps 101010', 'the quick brown fox jumped over the garden gate or something']

    for i, text in enumerate(texts):
        image_path = os.path.join(output_dir, f'training_image_{i}.png')
        create_synthetic_image(text, font_path, font_size, image_path)
        print(f"Generated image: {image_path}")