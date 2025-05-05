from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

def generate_comic_panels(story_guide,base_image_path, reference_style_path, output_dir="Individual_Panels"):
    # Load environment and Gemini API key
    load_dotenv()
    KEY = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=KEY)

    # Load images
    base_image = Image.open(base_image_path)
    reference_style = Image.open(reference_style_path)
    # Prompt
    text_input = """
    Turn this into 3 square comic style images as in the reference comic image.
    The three images should have a whacky story between them.
    Generate the 3 comic panels as separate images, in order.

    STRICTLY DO NOT CHANGE THE CHARACTER OR ITS RESEMBLANCE. NO REALISM ONLY CARTOON IMAGES
    THE STYLE MUST BE ALWAYS CONSISTENT IN ALL THREE IMAGES, THE OUTPUT IMAGE SHOULD ALWAYS BE IN 1:1 OR SQUARE ASPECT RATIO

    CARTOON STYLE IMAGES ONLY IN OUTPUT, NO TEXT BUBBLE IN THE IMAGE
    """+ f"Story Guidance from User is {story_guide} (Ignore if empty)"

    # Generate content
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[text_input, base_image, reference_style],
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save comic panels
    image_count = 0
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image_count += 1
            image.save(os.path.join(output_dir, f"comic_panel_{image_count}.png"))
        elif part.text is not None:
            print("Text response:", part.text)

    print(f"{image_count} comic panels saved to '{output_dir}'.")

