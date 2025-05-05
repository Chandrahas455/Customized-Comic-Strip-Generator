from PIL import Image
from google import genai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()
KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=KEY)

def generate_comic_story(image_paths, name):
    """
    Generate a funny 3-panel comic story from a list of 3 image paths.

    Args:
        image_paths (list): List of 3 image file paths.

    Returns:
        dict: A dictionary with 'title', 'text1', 'text2', and 'text3' keys.
    """
    if len(image_paths) != 3:
        raise ValueError("You must provide exactly 3 image paths.")

    images = [Image.open(path) for path in image_paths]

    prompt =  """Create a 3-panel comic story based on these images. 
Just give one line narrating the scene for each image THE STORY SHOULD BE CONSISTENT OVER THE THREE IMAGES
I need the response in the following format: ONLY THE JSON NOTHING ELSE IN RESPONSE(start with { and end with })
{title:"", text1:"", text2:"",text3:""}
Example Response: 
{
  "title": "The Unexpected Curry",
  "text1": "Gopal discovers the curry his wife made is surprisingly spicy.",
  "text2": "He realizes the overwhelming heat might be more than he bargained for.",
  "text3": "But Gopal, ever the comedian, decides to embrace the heat and declare this the spiciest curry champion!"
}
CREATE WACKY FUNNY AND QUIRKY STORIES, KEEP THE LINES SHORT(less than 20 words each). 
USE TELUGU MOVIE/MEME REFERENCES(BE BRUTAL IN ROASTING)""" + f"The character's name is {name}"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=images + [prompt]
    )

    story_json = response.text.strip()

    # Remove triple backticks and "json" language hint
    story_json = re.sub(r"^```json\s*|\s*```$", "", story_json.strip(), flags=re.MULTILINE)

    try:
        story_dict = json.loads(story_json)
        return story_dict
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Gemini output: {e}\nCleaned output was:\n{story_json}")
