import argparse
from PIL import Image

def extract_frames(gif_path):
    try:
        with Image.open(gif_path) as im:
            # Check if image is animated GIF
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from a GIF file.")
    parser.add_argument("gif_path", help="Path to the input GIF file")
    args = parser.parse_args()

    frames = extract_frames(args.gif_path)
    if frames:
        print(f"Successfully extracted {len(frames)} frames")
