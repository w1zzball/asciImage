import os
import time
import argparse
from extract_frames import extract_frames
from ascii import image_to_ascii

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_gif(file_path, width=100, frame_delay=0.1, output=None):
    # Extract frames if it's a GIF
    frames = extract_frames(file_path)
    
    # If not a GIF or frames extraction failed, treat as static image
    if frames is None:
        if not output:
            print("Error: --output must be specified for non-GIF files")
            return
        ascii_art = image_to_ascii(file_path, width)
        if ascii_art:
            try:
                with open(output, 'w') as f:
                    f.write(ascii_art)
                print(f"ASCII art saved to {output}")
            except Exception as e:
                print(f"Error saving to file: {e}")
        return

    # Handle animated GIF
    try:
        while True:  # Loop forever
            for frame in frames:
                clear_screen()
                ascii_frame = image_to_ascii(frame, width)
                print(ascii_frame)
                time.sleep(frame_delay)
    except KeyboardInterrupt:
        clear_screen()
        print("Animation stopped by user")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert and display image/GIF as ASCII art.")
    parser.add_argument("file_path", help="Path to the input image/GIF file")
    parser.add_argument("--width", type=int, default=100, help="Width of ASCII output")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between frames in seconds")
    parser.add_argument("--output", help="Output file for static images (required for non-GIF files)")
    args = parser.parse_args()

    animate_gif(args.file_path, args.width, args.delay, args.output)
