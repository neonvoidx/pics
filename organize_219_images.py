#!/usr/bin/env python3
"""
Script to organize 21:9 aspect ratio images.
Moves images >= 3440x1440 from 21:9 subfolder to root folder.
Deletes 21:9 subfolder if empty after moving.
"""

import os
import shutil
from PIL import Image


def is_219_aspect_ratio(width, height):
    """Check if image has 21:9 aspect ratio (allowing small tolerance)"""
    if height == 0:
        return False
    ratio = width / height
    # 21:9 is approximately 2.33, allow small tolerance
    return 2.3 <= ratio <= 2.4


def get_image_dimensions(image_path):
    """Get dimensions of an image file"""
    try:
        with Image.open(image_path) as img:
            return img.size  # Returns (width, height)
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return None, None


def process_219_subfolder(subfolder_names=None):
    """
    Process 21:9 images from subfolder(s).
    
    Args:
        subfolder_names: List of folder names to check. 
                        Defaults to ["21:9", "21-9"] if None.
    """
    if subfolder_names is None:
        subfolder_names = ["21:9", "21-9"]
    
    for subfolder_name in subfolder_names:
        subfolder_path = os.path.join(".", subfolder_name)
        
        # Check if subfolder exists
        if not os.path.isdir(subfolder_path):
            print(f"Subfolder '{subfolder_name}' does not exist, skipping.")
            continue
        
        print(f"\nProcessing subfolder: {subfolder_name}")
        
        # Get all image files in the subfolder
        image_files = []
        for file in os.listdir(subfolder_path):
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                image_files.append(file)
        
        if not image_files:
            print(f"No images found in {subfolder_name}")
            continue
        
        print(f"Found {len(image_files)} image(s) in {subfolder_name}")
        
        moved_count = 0
        skipped_count = 0
        
        # Process each image
        for image_file in image_files:
            image_path = os.path.join(subfolder_path, image_file)
            width, height = get_image_dimensions(image_path)
            
            if width is None or height is None:
                print(f"Skipping {image_file}: Could not read dimensions")
                skipped_count += 1
                continue
            
            # Check if it's 21:9 aspect ratio
            if not is_219_aspect_ratio(width, height):
                print(f"Skipping {image_file}: Not 21:9 aspect ratio ({width}x{height})")
                skipped_count += 1
                continue
            
            # Check if dimensions meet threshold
            if width >= 3440 and height >= 1440:
                # Move to root folder
                destination = os.path.join(".", image_file)
                
                # Check if file already exists in root
                if os.path.exists(destination):
                    print(f"Skipping {image_file}: File already exists in root folder")
                    skipped_count += 1
                    continue
                
                print(f"Moving {image_file} ({width}x{height}) to root folder")
                shutil.move(image_path, destination)
                moved_count += 1
            else:
                print(f"Skipping {image_file}: Size {width}x{height} is less than 3440x1440")
                skipped_count += 1
        
        print(f"\nSummary for {subfolder_name}:")
        print(f"  Moved: {moved_count}")
        print(f"  Skipped: {skipped_count}")
        
        # Check if subfolder is now empty
        remaining_files = os.listdir(subfolder_path)
        if not remaining_files:
            print(f"\n{subfolder_name} is now empty, deleting folder...")
            os.rmdir(subfolder_path)
            print(f"Deleted empty folder: {subfolder_name}")
        else:
            print(f"\n{subfolder_name} still contains {len(remaining_files)} file(s), keeping folder")


def main():
    """Main function"""
    print("=" * 60)
    print("21:9 Image Organizer")
    print("=" * 60)
    print("This script moves 21:9 images >= 3440x1440")
    print("from subfolder(s) to root folder.")
    print("=" * 60)
    
    process_219_subfolder()
    
    print("\n" + "=" * 60)
    print("Processing complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
