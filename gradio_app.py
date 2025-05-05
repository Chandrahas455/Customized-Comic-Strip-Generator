import gradio as gr
from PIL import Image
import time
import os

from text_generation import generate_comic_story
from image_generation import generate_comic_panels
from layout_generation import generate_comic_strip
from texture import apply_texture_overlay
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
style_reference_img = os.path.join(BASE_DIR,"Defaults", "Default_Style_Ref.png")

def comic_creator(user_image, name, style_reference=None,story_guide=""):
    """
    Generates a customized whacky comic strip based on a user-uploaded photo, name, and optional style reference.

    This function performs the following steps:
    1. Saves the uploaded user image locally.
    2. Uses a provided style reference image or falls back to a default style image.
    3. Generates comic-style image panels based on the user input and optional storyline guidance.
    4. Creates a narrative comic story incorporating the user's name and guided prompt.
    5. Arranges the generated panels into a final comic strip layout.
    6. Optionally applies a texture overlay to enhance visual appearance.
    7. Returns the file path to the final textured comic strip image.

    Args:
        user_image (PIL.Image.Image): User-uploaded base image for comic character.
        name (str): User's name to personalize the comic story.
        style_reference (PIL.Image.Image, optional): Optional reference image to influence comic style.
        story_guide (str, optional): Optional textual guide to direct the comic story's theme.

    Returns:
        str: File path to the final generated textured comic strip image.
    """
    gstart = time.time()

    # Save uploaded base image
    base_image_path = user_image

    # Use uploaded style image or fallback to default
    if style_reference:
        style_reference_path = style_reference
    else:
        style_reference_path = style_reference_img # default style

    # --- Panel Generation ---
    generate_comic_panels(
        story_guide,
        base_image_path=base_image_path,
        reference_style_path=style_reference_path
    )

    # --- Comic Story Generation ---
    comic_panel_paths = [
        "Individual_Panels/comic_panel_1.png",
        "Individual_Panels/comic_panel_2.png",
        "Individual_Panels/comic_panel_3.png"
    ]
    story = generate_comic_story(comic_panel_paths, name+"("+story_guide+")")

    comic_images = [Image.open(path) for path in comic_panel_paths]



    # --- Optional Texture Overlay ---
    apply_texture_overlay(generate_comic_strip(comic_images, story))

    # Return final comic strip
    return "textured_comic.png"

# Gradio Interface
with gr.Blocks(title="Customized Whacky Comic Strip Generator", theme="soft") as demo:
    gr.Markdown(
    """
    <h2 style='text-align: center;'>
        <a href='https://github.com/Chandrahas455/Customized-Comic-Strip-Generator.git' target='_blank' style='text-decoration: none; color: inherit;'>
            Customized Whacky Comic Strip Generator 
        </a>
    </h2>
    """
)

    with gr.Row():
        user_image_input = gr.Image(type="filepath", label="Upload Your Picture")
        style_image_input = gr.Image(type="filepath", label="Optional Style Reference Image")

    name_input = gr.Textbox(label="Enter Your Name")

    story_guide = gr.Textbox(label="Guide The Storyline (Optional)")
    
    generate_button = gr.Button("Generate Comic Strip")

    output_image = gr.Image(type="filepath", label="Your Whacky Comic Strip")

    generate_button.click(
        fn=comic_creator,
        inputs=[user_image_input, name_input, style_image_input,story_guide],
        outputs=output_image
    )

if __name__ == "__main__":
    demo.launch()
