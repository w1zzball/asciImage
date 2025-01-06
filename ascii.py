import argparse
from PIL import Image

# Default ASCII characters from darkest to lightest
DEFAULT_ASCII_CHARS = ".:-=+*#%@"

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

def apply_dithering(image):
    return image.convert('1', dither=Image.FLOYDSTEINBERG)

def pixels_to_ascii(image, ascii_chars=DEFAULT_ASCII_CHARS):
    pixels = image.getdata()
    ascii_str = ""
    # Adjust division factor for the new range of characters
    interval = 256 / len(ascii_chars)
    for pixel in pixels:
        ascii_str += ascii_chars[int(pixel / interval)]
    return ascii_str

def image_to_ascii(image, new_width=100, dither=False, ascii_chars=DEFAULT_ASCII_CHARS):
    if isinstance(image, str):
        try:
            image = Image.open(image)
        except Exception as e:
            print(e)
            return

    image = resize_image(image, new_width)
    
    # Apply dithering before grayscale if requested
    if dither:
        image = apply_dithering(image)
    image = grayify(image)
    
    ascii_str = pixels_to_ascii(image, ascii_chars)

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
    parser.add_argument("--dither", action="store_true", help="Apply dithering to the image")
    parser.add_argument("--chars", default=DEFAULT_ASCII_CHARS, 
                      help="Custom ASCII characters (darkest to lightest)")
    args = parser.parse_args()

    ascii_art = image_to_ascii(args.image_path, args.width, args.dither, args.chars)
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
