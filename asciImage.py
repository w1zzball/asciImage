import os
import time
import argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class ASCIIArtConverter:
    DEFAULT_ASCII_CHARS = ".:-=+*#%@"

    def __init__(self, width=100, frame_delay=0.1, dither=False, ascii_chars=None):
        self.width = width
        self.frame_delay = frame_delay
        self.dither = dither
        self.ascii_chars = self._prepare_chars(ascii_chars or self.DEFAULT_ASCII_CHARS)

    def _prepare_chars(self, chars):
        """Sort and reverse chars by brightness."""
        return self.sort_by_brightness(chars)[::-1]

    @staticmethod
    def get_char_brightness(char, size=32):
        img = Image.new('L', (size, size), 255)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("consolas", size)
        except:
            font = ImageFont.load_default()
        draw.text((0, 0), char, font=font, fill=0)
        return np.array(img).mean()

    @staticmethod
    def sort_by_brightness(chars):
        char_brightness = [(char, ASCIIArtConverter.get_char_brightness(char)) for char in chars]
        sorted_chars = sorted(char_brightness, key=lambda x: x[1])
        return ''.join(char for char, _ in sorted_chars)

    def resize_image(self, image):
        width, height = image.size
        ratio = height / width
        new_height = int(self.width * ratio * 0.5)
        return image.resize((self.width, new_height))

    def extract_frames(self, gif_path):
        try:
            with Image.open(gif_path) as im:
                if not getattr(im, "is_animated", False):
                    return None
                
                frames = []
                try:
                    while True:
                        frames.append(im.copy())
                        im.seek(im.tell() + 1)
                except EOFError:
                    pass
                
                return frames
                
        except Exception as e:
            print(f"Error processing file: {e}")
            return None

    def convert_to_ascii(self, image):
        if isinstance(image, str):
            try:
                image = Image.open(image)
            except Exception as e:
                print(e)
                return None

        image = self.resize_image(image)
        if self.dither:
            image = image.convert('1', dither=Image.FLOYDSTEINBERG)
        image = image.convert("L")

        pixels = image.getdata()
        interval = 256 / len(self.ascii_chars)
        ascii_str = "".join(self.ascii_chars[int(pixel / interval)] for pixel in pixels)

        return "\n".join(ascii_str[i:i + image.width] 
                        for i in range(0, len(ascii_str), image.width))

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def process_file(self, file_path, output=None):
        frames = self.extract_frames(file_path)
        
        if frames is None:  # Static image
            ascii_art = self.convert_to_ascii(file_path)
            if ascii_art:
                if output:
                    try:
                        with open(output, 'w') as f:
                            f.write(ascii_art)
                        print(f"ASCII art saved to {output}")
                    except Exception as e:
                        print(f"Error saving to file: {e}")
                else:
                    print(ascii_art)
            return

        # Animated GIF
        try:
            while True:
                for frame in frames:
                    self.clear_screen()
                    print(self.convert_to_ascii(frame))
                    time.sleep(self.frame_delay)
        except KeyboardInterrupt:
            self.clear_screen()
            print("Animation stopped by user")

def main():
    parser = argparse.ArgumentParser(description="Convert images/GIFs to ASCII art")
    parser.add_argument("file_path", help="Path to the input image/GIF file")
    parser.add_argument("--width", type=int, default=100, help="Width of ASCII output")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between frames in seconds")
    parser.add_argument("--output", help="Output file for saving ASCII art (optional)")
    parser.add_argument("--dither", action="store_true", help="Apply dithering to the image")
    parser.add_argument("--chars", default=None, help="Custom ASCII characters (will be sorted by brightness)")
    args = parser.parse_args()

    converter = ASCIIArtConverter(
        width=args.width,
        frame_delay=args.delay,
        dither=args.dither,
        ascii_chars=args.chars
    )
    converter.process_file(args.file_path, args.output)

if __name__ == "__main__":
    main()
