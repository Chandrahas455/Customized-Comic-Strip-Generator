from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
texture = os.path.join(BASE_DIR, "Textures", "Paper_texture.png")

def apply_texture_overlay(base_image_path, texture_paths=[texture], output_path="textured_comic.png", blend_mode="normal"):
    # Open comic strip
    base = Image.open(base_image_path).convert("RGBA")

    for texture_path in texture_paths:
        texture = Image.open(texture_path).convert("RGBA")
        texture = texture.resize(base.size)

        # Optional: reduce texture opacity
        alpha = texture.split()[3]
        alpha = alpha.point(lambda p: p * 0.7)  # 40% opacity
        texture.putalpha(alpha)

        # Blend based on mode
        if blend_mode == "multiply":
            base = Image.blend(base, texture, alpha=0.2)
        else:
            base = Image.alpha_composite(base, texture)

    base.convert("RGB").save(output_path)
    #print(f"Saved textured image at {output_path}")

