from django.shortcuts import render
from django.http import HttpResponse
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

        lines = textwrap.wrap(topic, width=15)
        y = 200
        for line in lines:
            w, h = draw.textsize(line, font=font)
            draw.text(((size[0]-w)/2, y), line, font=font, fill="white")
            y += h+10

        caption = re.sub(r"#\w+", "", caption)
        w, h = draw.textsize(caption, font=small_font)
        draw.text(((size[0]-w)/2, size[1]-200), caption, font=small_font, fill="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        image_url = f"data:image/png;base64,{image_base64}"

    return render(request, "generator/form.html", {"image_url": image_url})
