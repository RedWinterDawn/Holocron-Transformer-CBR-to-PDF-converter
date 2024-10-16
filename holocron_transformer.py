import sys
import subprocess
import os
from PIL import Image
import tempfile

def convert_cbr_to_pdf(cbr_file, output_pdf):
    try:
        # Create a temporary directory to extract CBR contents
        with tempfile.TemporaryDirectory() as temp_dir:
            # Use unar to extract the CBR file
            subprocess.run(['unar', '-o', temp_dir, cbr_file], check=True)

            # Get all image files from the extracted contents
            image_files = []
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        image_files.append(os.path.join(root, file))
            image_files.sort()  # Sort files to maintain order

            images = []
            for file in image_files:
                with Image.open(file) as img:
                    images.append(img.convert('RGB'))

            if images:
                images[0].save(output_pdf, save_all=True, append_images=images[1:])
                print(f"Conversion complete: {output_pdf}")
            else:
                print("No images found in the CBR file.")

    except FileNotFoundError:
        print(f"Error: {cbr_file} not found.")
    except subprocess.CalledProcessError:
        print("Error: Failed to extract CBR file. Make sure 'unar' is installed.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 comic.py <path_to_cbr_file>")
    else:
        cbr_path = sys.argv[1]
        output_pdf = cbr_path.replace(".cbr", ".pdf")
        convert_cbr_to_pdf(cbr_path, output_pdf)
