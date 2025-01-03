import os
import time
import argparse
from extract_frames import extract_frames
from ascii import image_to_ascii

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_gif(gif_path, width=100, frame_delay=0.1):
    # Extract all frames from the GIF
    frames = extract_frames(gif_path)
    if not frames:
        return
    
    # Convert each frame to ASCII and display
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
    parser = argparse.ArgumentParser(description="Convert and display GIF as ASCII animation.")
    parser.add_argument("gif_path", help="Path to the input GIF file")
    parser.add_argument("--width", type=int, default=100, help="Width of ASCII output")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between frames in seconds")
    args = parser.parse_args()

    animate_gif(args.gif_path, args.width, args.delay)
