import argparse
from PIL import Image, ImageDraw, ImageFont
import numpy as np

#orders input characters by brightness

def get_char_brightness(char, size=32):
    # Create image with white background
    img = Image.new('L', (size, size), 255)
    draw = ImageDraw.Draw(img)
    
    # Load a monospace font
    try:
        font = ImageFont.truetype("consolas", size)
    except:
        font = ImageFont.load_default()
    
    # Draw character in black
    draw.text((0, 0), char, font=font, fill=0)
    
    # Calculate average brightness (0 is black, 255 is white)
    brightness = np.array(img).mean()
    return brightness

def sort_by_brightness(chars):
    # Create list of (char, brightness) tuples
    char_brightness = [(char, get_char_brightness(char)) for char in chars]
    # Sort by brightness (darkest to lightest)
    sorted_chars = sorted(char_brightness, key=lambda x: x[1])
    # Return just the characters
    return ''.join(char for char, _ in sorted_chars)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort ASCII characters by brightness.")
    parser.add_argument("chars", nargs='?', default="$░⣴⣿▀▄█",
                      help="String of characters to sort (default: $░⣴⣿▀▄█)")
    args = parser.parse_args()

    sorted_chars = sort_by_brightness(args.chars)
    print(f"Original: {args.chars}")
    print(f"Sorted (dark to light): {sorted_chars}")