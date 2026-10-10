import os
from PIL import Image, ImageDraw, ImageFont

icons_dir = r"c:\VoiceVision-voice\voice_age_prediction\static\icons"
os.makedirs(icons_dir, exist_ok=True)

def create_app_icon(filename, bg_color, text, is_shape=None):
    size = (512, 512)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw rounded rectangle
    r = 110
    draw.rounded_rectangle([0, 0, 512, 512], radius=r, fill=bg_color)
    
    if is_shape == "play":
        # YouTube play triangle
        draw.rounded_rectangle([100, 150, 412, 362], radius=60, fill=(255,255,255))
        draw.polygon([(215, 200), (335, 256), (215, 312)], fill=bg_color)
    elif is_shape == "facebook":
        try:
            font = ImageFont.truetype("arial.ttf", 360)
        except:
            font = ImageFont.load_default()
        draw.text((270, 100), "f", fill=(255,255,255), font=font)
    elif is_shape == "linkedin":
        try:
            font = ImageFont.truetype("arial.ttf", 260)
        except:
            font = ImageFont.load_default()
        draw.text((140, 130), "in", fill=(255,255,255), font=font)
    else:
        try:
            font = ImageFont.truetype("arialbd.ttf", 100)
        except:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((512-w)/2, (512-h)/2 - 10), text, fill=(255,255,255), font=font)
        
    img.save(os.path.join(icons_dir, filename), "PNG")
    print(f"Created {filename}")

create_app_icon("facebook.png", (24, 119, 242, 255), "f", is_shape="facebook")
create_app_icon("youtube.png", (255, 0, 0, 255), "", is_shape="play")
create_app_icon("discord.png", (88, 101, 242, 255), "Discord")
create_app_icon("steam_chat.png", (23, 26, 33, 255), "Steam")
create_app_icon("twitch.png", (145, 70, 255, 255), "Twitch")
create_app_icon("linkedin.png", (0, 119, 181, 255), "in", is_shape="linkedin")
