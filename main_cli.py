import argparse
import os
import time
from PIL import Image

from text_generation import generate_comic_story
from image_generation import generate_comic_panels
from layout_generation import generate_comic_strip
from texture import apply_texture_overlay

def main(base_image_path, reference_style_path, name, story_guide):
    gstart = time.time()

    # --- Panel Generation ---
    print("Starting Panel Generation...")
    start = time.time()
    generate_comic_panels(
        story_guide=story_guide,
        base_image_path=base_image_path,
        reference_style_path=reference_style_path
    )
    end = time.time()
    print(f"Panel Generation Completed Successfully in {end - start:.2f} seconds")

    # --- Story Generation ---
    comic_panel_paths = [
        os.path.join(os.path.dirname(base_image_path), "..", "Individual_Panels", f"comic_panel_{i}.png")
        for i in range(1, 4)
    ]
    print("Starting Story Generation...")
    start = time.time()
    story = generate_comic_story(comic_panel_paths, name)
    end = time.time()
    print(f"Story Generation Completed Successfully in {end - start:.2f} seconds")

    # --- Load Panels ---
    comic_images = [Image.open(path) for path in comic_panel_paths]

    # --- Generate Final Comic ---
    print("Creating Final Comic...")
    final_path = apply_texture_overlay(generate_comic_strip(comic_images, story))
    gend = time.time()
    print(f"Whacky Comic Created Successfully in {gend - gstart:.2f} seconds")
    print(f"Output saved at: {final_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a whacky comic strip from an image.")
    parser.add_argument("--input", required=True, help="Path to the user image (JPG or PNG).")
    parser.add_argument("--style", required=False, help="Path to the style reference image (optional).")
    parser.add_argument("--name", required=True, help="User's name for personalizing the story.")
    parser.add_argument("--guide", default="", help="Storyline guide to shape the comic (optional).")

    args = parser.parse_args()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    default_style = os.path.join(BASE_DIR, "Test_Images", "StyleReference.jpg")
    style_path = args.style if args.style else default_style

    main(args.input, style_path, args.name, args.guide)
