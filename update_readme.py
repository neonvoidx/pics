"""Dynamic README generator for images in directory"""

import os


def get_all_images(walk_path):
    """Gets all images in specified directory only (not recursive)"""
    images = []
    for root, _, files in os.walk(walk_path):
        # Only add images from the exact directory specified
        if os.path.abspath(root) == os.path.abspath(walk_path):
            for file in files:
                if (
                    file.endswith(".png")
                    or file.endswith(".jpg")
                    or file.endswith(".jpeg")
                    or file.endswith(".gif")
                    or file.endswith(".webp")
                ):
                    images.append(file)
    return sorted(images)


def get_aspect_ratio_folders():
    """Get all aspect ratio folders (excluding .git, .github, vertical)"""
    folders = []
    for item in os.listdir("."):
        if os.path.isdir(item) and item not in [".git", ".github", "vertical"]:
            folders.append(item)
    return sorted(folders)


def folder_name_to_title(folder_name):
    """Convert folder name to readable title"""
    ratio_names = {
        "16-9": "16:9 (Standard Widescreen)",
        "21-9": "21:9 (Ultrawide)",
        "2-1": "2:1",
        "3-2": "3:2",
        "4-3": "4:3",
        "8-5": "8:5 (16:10)",
        "48-25": "48:25",
        "43-18": "43:18",
        "64-27": "64:27",
        "12-5": "12:5",
    }
    return ratio_names.get(folder_name, folder_name.replace("-", ":"))


def main():
    """Main function"""
    # Generate README content
    output = []
    output.append("### Wallpapers\n")
    output.append("This my collection of wallpapers that I find visually pleasing. ")
    output.append("I do not take credit for any of these, most of then are found on ")
    output.append("/r/unixporn or wallhaven.cc.\n")
    output.append("\nPreviews are dynamically generated below:\n")
    
    # 21:9 Ultrawide images (root folder)
    ultrawide_images = get_all_images(".")
    if ultrawide_images:
        output.append("\n#### 21:9 Ultrawide\n")
        for image in ultrawide_images:
            output.append(f"\n![{image}](./{image})")
        output.append("\n")
    
    # Vertical images
    vert_images = get_all_images("vertical")
    if vert_images:
        output.append("\n#### Vertical (Portrait Mode)\n")
        for image in vert_images:
            output.append(f"\n![{image}](./vertical/{image})")
        output.append("\n")
    
    # Other aspect ratio folders
    aspect_folders = get_aspect_ratio_folders()
    for folder in aspect_folders:
        folder_images = get_all_images(folder)
        if folder_images:
            title = folder_name_to_title(folder)
            output.append(f"\n#### {title}\n")
            for image in folder_images:
                output.append(f"\n![{image}](./{folder}/{image})")
            output.append("\n")
    
    # Write to README
    readme_content = "".join(output)
    print(readme_content)
    
    with open("README.md", "w", encoding="utf-8") as readme:
        readme.write(readme_content)


if __name__ == "__main__":
    main()
