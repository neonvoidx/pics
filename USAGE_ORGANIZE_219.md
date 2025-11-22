# 21:9 Image Organization Script

## Purpose

The `organize_219_images.py` script helps maintain organization of 21:9 ultrawide images by automatically moving high-resolution images (>= 3440x1440) from subfolders to the root directory.

## Usage

```bash
python3 organize_219_images.py
```

## What It Does

1. **Searches** for 21:9 subfolders (checks for folders named "21:9" or "21-9")
2. **Identifies** images with 21:9 aspect ratio (ratio between 2.3 and 2.4)
3. **Moves** images that meet the size threshold (width >= 3440 AND height >= 1440) to the root folder
4. **Cleans up** by deleting the subfolder if it becomes empty after moving images

## Behavior

### Images that will be moved:
- Have 21:9 aspect ratio (approximately 2.33:1)
- Have dimensions >= 3440x1440 pixels
- Are not already present in the root folder

### Images that will be skipped:
- Wrong aspect ratio (e.g., 16:9 images)
- Below size threshold (e.g., 2560x1080)
- Already exist in root folder (prevents duplicates)

### Folder deletion:
- The subfolder is only deleted if it becomes completely empty after moving images
- If any images remain (didn't meet criteria), the folder is kept

## Example Output

```
============================================================
21:9 Image Organizer
============================================================
This script moves 21:9 images >= 3440x1440
from subfolder(s) to root folder.
============================================================

Processing subfolder: 21-9
Found 3 image(s) in 21-9
Moving wallpaper1.jpg (3440x1440) to root folder
Moving wallpaper2.png (3840x1600) to root folder
Skipping small-image.png: Size 2560x1080 is less than 3440x1440

Summary for 21-9:
  Moved: 2
  Skipped: 1

21-9 still contains 1 file(s), keeping folder

============================================================
Processing complete!
============================================================
```

## Requirements

- Python 3
- Pillow (PIL) library: `pip install Pillow`

## When to Use

Run this script when:
- You've added new images to a 21:9 subfolder
- You want to promote high-resolution 21:9 images to the main collection
- You need to reorganize the image structure
