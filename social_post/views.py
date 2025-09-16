from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFont
import textwrap, random, re
from io import BytesIO
import base64

def home(request):
    image_url = None
    if "topic" in request.GET and "caption" in request.GET:
        topic = request.GET["topic"]
        caption = request.GET["caption"]

        size = (1080, 1080)
        palettes = [("#FF9A9E", "#FAD0C4"), ("#A18CD1", "#FBC2EB"), ("#F6D365", "#FDA085")]
        start, end = random.choice(palettes)

        img = Image.new("RGB", size, start)
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 60)
            small_font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        # Draw title with text wrapping
        lines = textwrap.wrap(topic, width=15)
        y = 200
        for line in lines:
            # Get text bounding box
            bbox = draw.textbbox((0, 0), line, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            # Draw text
            draw.text(((size[0]-w)/2, y), line, font=font, fill="white")
            y += h + 10

        # Clean and draw caption
        caption = re.sub(r"#\w+", "", caption)
        bbox = draw.textbbox((0, 0), caption, font=small_font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((size[0]-w)/2, size[1]-200), caption, font=small_font, fill="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        image_url = f"data:image/png;base64,{image_base64}"

    return render(request, "social_post/form.html", {"image_url": image_url})
