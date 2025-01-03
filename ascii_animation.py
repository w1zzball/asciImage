import os
import time
import argparse
from extract_frames import extract_frames
from ascii import image_to_ascii

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_gif(file_path, width=100, frame_delay=0.1, output=None, dither=False):
    # Extract frames if it's a GIF
    frames = extract_frames(file_path)
    
    # If not a GIF or frames extraction failed, treat as static image
    if frames is None:
        ascii_art = image_to_ascii(file_path, width, dither)
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

    # Handle animated GIF
    try:
        while True:  # Loop forever
            for frame in frames:
                clear_screen()
                ascii_frame = image_to_ascii(frame, width, dither)
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
    parser.add_argument("--output", help="Output file for saving ASCII art (optional)")
    parser.add_argument("--dither", action="store_true", help="Apply dithering to the image")
    args = parser.parse_args()

    animate_gif(args.file_path, args.width, args.delay, args.output, args.dither)
