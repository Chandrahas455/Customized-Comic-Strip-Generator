from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
font_title_path = os.path.join(BASE_DIR, "Fonts", "Some_Time_Later.otf")
font_text_path =os.path.join(BASE_DIR, "Fonts", "digistrip.ttf")
base_image_path =os.path.join(BASE_DIR, "Defaults","baseimage.png")
def generate_comic_strip(images, story_dict, base_image_path=base_image_path, output_path="comic_strip_centered.png",
                         font_title_path=font_title_path,
                         font_text_path=font_text_path):
    """
    Creates a comic strip layout from 3 images and a story dictionary with title, text1, text2, text3.

    Args:
        images (list of PIL.Image): List of 3 panel images.
        story_dict (dict): Dictionary with keys: 'title', 'text1', 'text2', 'text3'.
        base_image_path (str): Optional path to a background image to use as the comic canvas.
        output_path (str): Path to save the final composed comic strip.
        font_title_path (str): Path to the title font file.
        font_text_path (str): Path to the text font file.
    """

    try:
        font_title = ImageFont.truetype(font_title_path, 50)
        font_text = ImageFont.truetype(font_text_path, 14)
    except Exception as e:
        print(f"Error loading fonts: {e}. Falling back to default fonts.")
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

    image_width = 300
    image_height = 300
    images = [img.resize((image_width, image_height)) for img in images]

    panel_count = 3
    padding = 20
    title_height = 80
    text_box_height = 100

    panel_width = image_width * panel_count + padding * (panel_count + 1)
    panel_height = title_height + image_height + text_box_height + padding * 3

    # Load base image or create a white canvas
    if base_image_path and os.path.exists(base_image_path):
        base_img = Image.open(base_image_path).convert("RGB")
        base_img = base_img.resize((panel_width, panel_height))
        canvas = base_img.copy()
    else:
        canvas = Image.new("RGB", (panel_width, panel_height), color="white")

    draw = ImageDraw.Draw(canvas)

    # Draw title centered
    title = story_dict["title"]
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_x = (panel_width - (bbox[2] - bbox[0])) // 2
    draw.text((title_x, padding), title, fill="black", font=font_title)

    texts = [story_dict["text1"], story_dict["text2"], story_dict["text3"]]

    for i in range(panel_count):
        x = padding + i * (image_width + padding)
        y_img = title_height + padding
        y_text = y_img + image_height + 10

        # Paste image
        canvas.paste(images[i], (x, y_img))

        # Wrap and center text
        text = texts[i]
        wrapped = textwrap.wrap(text, width=28)
        for j, line in enumerate(wrapped):
            line_bbox = draw.textbbox((0, 0), line, font=font_text)
            text_x = x + (image_width - (line_bbox[2] - line_bbox[0])) // 2
            text_y = y_text + j * (font_text.getbbox(line)[3] + 5)
            draw.text((text_x, text_y), line, fill="black", font=font_text)

        # Optional border
        draw.rectangle([x - 2, y_img - 2, x + image_width + 2, y_img + image_height + text_box_height],
                       outline="black", width=2)

    canvas.save(output_path)
    print(f"Saved comic strip with background to: {output_path}")
    return output_path
