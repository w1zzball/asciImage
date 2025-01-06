# ASCII Image Converter

Convert images and animated GIFs to ASCII art in your terminal. Supports both static images and animated GIFs with customizable output options.

## Requirements
- Python 3.6+
- Pillow (PIL)

Usage
Basic command:

python asciImage.py <image_path>

Options
--width <pixels>: Set output width in characters (default: 100)
--delay <seconds>: Set frame delay for GIF animations (default: 0.1)
--output <filename>: Save output to file instead of displaying
--dither: Apply Floyd-Steinberg dithering
--chars <string>: Use custom ASCII characters (sorted by brightness)

Examples
Convert static image:

python asciImage.py image.jpg --width 80

Convert and save to file:

python asciImage.py image.png --width 120 --output art.txt

Play animated GIF:

python asciImage.py animation.gif --delay 0.05

Use custom characters:

python asciImage.py image.jpg --chars ".:-=+*#%@"

Features
Static image conversion
Animated GIF support
Adjustable output size
Optional dithering
Custom ASCII character sets
Save to file option
Controls
Press Ctrl+C to stop animated GIFs