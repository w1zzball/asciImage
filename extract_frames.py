import os
import argparse
from PIL import Image

def extract_frames(gif_path, output_dir=None):
    try:
        frames = []
        with Image.open(gif_path) as im:
            # Check if image is animated
            try:
                while True:
                    # Copy the current frame
                    current = im.copy()
                    if output_dir:
                        frame_path = os.path.join(output_dir, f"frame_{len(frames):03d}.png")
                        current.save(frame_path, 'PNG')
                    frames.append(current)
                    # Go to next frame
                    im.seek(im.tell() + 1)
            except EOFError:
                pass  # End of sequence
            
            return frames

    except Exception as e:
        print(f"Error processing GIF: {e}")
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from a GIF file.")
    parser.add_argument("gif_path", help="Path to the input GIF file")
    parser.add_argument("--output", default="frames", help="Directory to save the frames (default: frames)")
    args = parser.parse_args()

    frames = extract_frames(args.gif_path, args.output)
    if frames:
        print(f"Successfully extracted {len(frames)} frames to {args.output}/")
