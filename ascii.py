import argparse
from PIL import Image

# ASCII characters used in the output art
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    # Adjust for terminal character aspect ratio (approximately 2:1)
    new_height = int(new_width * ratio * 0.5)  # multiply by 0.5 to compensate for terminal chars
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel // 32]
    return ascii_str

def image_to_ascii(image, new_width=100):
    if isinstance(image, str):
        try:
            image = Image.open(image)
        except Exception as e:
            print(e)
            return

    image = resize_image(image, new_width)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image)

    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i + img_width] + "\n"
    
    return ascii_img

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument("--width", type=int, default=100, help="Desired output width of the ASCII art")
    parser.add_argument("--output", help="Path to save the ASCII art output file")
    args = parser.parse_args()

    ascii_art = image_to_ascii(args.image_path, args.width)
    if ascii_art:
        if args.output:
            try:
                with open(args.output, 'w') as f:
                    f.write(ascii_art)
                print(f"ASCII art saved to {args.output}")
            except Exception as e:
                print(f"Error saving to file: {e}")
        else:
            print(ascii_art)
