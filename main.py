from text_generation import generate_comic_story
from image_generation import generate_comic_panels
from layout_generation import generate_comic_strip
from texture import apply_texture_overlay
from PIL import Image
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
base_image_path= os.path.join(BASE_DIR,"Test_Images","Input.jpg")
reference_style_path = os.path.join(BASE_DIR,"Test_Images","StyleReference.jpg")

gstart = time.time()
start = time.time()
print("Starting Panel Generation...")
generate_comic_panels(
        story_guide="Make jokes about GitHub",
        base_image_path=base_image_path,
        reference_style_path= reference_style_path
)
end=time.time()
print(f"Panel Generation Completed Succedflly in {end-start}")


comic_images = [
    os.path.join(BASE_DIR,"Individual_Panels", "comic_panel_1.png"),
    os.path.join(BASE_DIR,"Individual_Panels", "comic_panel_2.png"),
    os.path.join(BASE_DIR,"Individual_Panels", "comic_panel_3.png")

]


start = time.time()
print("Starting Story Generatio...n")
story = generate_comic_story(comic_images,"Your Name")
end=time.time()
print(f"Story Generation Completed Succedflly in {end-start}")


comic_images = [
    Image.open(os.path.join(BASE_DIR,"Individual_Panels","comic_panel_1.png")),
    Image.open(os.path.join(BASE_DIR,"Individual_Panels","comic_panel_2.png")),
    Image.open(os.path.join(BASE_DIR,"Individual_Panels","comic_panel_3.png"))
]


print("Creating Final Comic...")
apply_texture_overlay(generate_comic_strip(comic_images, story))

gend=time.time()
print(f"Whacky Comic Created succesfully in {gend-gstart}")