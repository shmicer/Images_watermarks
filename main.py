from PIL import Image, ImageFont, ImageDraw
from config import color1, color2, text1, text2, opacity, input_folder_path, output_folder_path, logo_path
import os


def make_transparent_watermark():
    """Make logo transparent and save it to a file"""
    im_rgb = Image.open(f"{logo_path}/logo.jpg")
    im_rgba = im_rgb.copy()
    im_rgba.putalpha(opacity)
    datas = im_rgba.getdata()
    new_data = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    im_rgba.putdata(new_data)
    im_rgba.save(f"{logo_path}/transparent_logo.png", "PNG")


def add_watermark(input_path, output_path):
    """Add transparent logo form file to image.
    Add two texts(because it has to be different colors)
    to image"""
    im = Image.open(input_path).convert("RGBA")
    wm = Image.open(f"{logo_path}/transparent_logo.png").convert("RGBA")
    width, height = im.size
    width_percent = (wm.size[0] / wm.size[1])
    new_watermark = wm.resize((int((width / 7.5) * width_percent), int(int(width / 7.5))))
    width_of_watermark, height_of_watermark = new_watermark.size
    position = ((width // 100), (height // 2 - height_of_watermark // 2))
    im.paste(new_watermark, position, mask=new_watermark)

    txt = Image.new("RGBA", im.size, (255, 255, 255, 0))
    width, height = txt.size
    font = ImageFont.truetype("arial.ttf", size=height_of_watermark)
    draw_text = ImageDraw.Draw(txt)
    draw_text.text(
        (width_of_watermark * 1.3, height / 2),
        text1,
        anchor='lm',
        font=font,
        fill=color1)
    draw_text.text(
        (width_of_watermark * 4.8, height / 2),
        text2,
        anchor='lm',
        font=font,
        fill=color2)
    out = Image.alpha_composite(im, txt)
    out.save(output_path)


def modernize_webp_files(input_folder, output_folder):
    """Iterate over all files and folders within the input folder"""
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            # Check if the file has a .webp extension
            if file.endswith(".webp"):
                # Create the file paths
                input_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_folder_path = os.path.join(output_folder, relative_path)
                output_file_path = os.path.join(output_folder_path, file)

                # Create the output folder if it doesn't exist
                os.makedirs(output_folder_path, exist_ok=True)

                add_watermark(input_file_path, output_file_path)


if __name__ == '__main__':
    make_transparent_watermark()
    modernize_webp_files(input_folder_path, output_folder_path)