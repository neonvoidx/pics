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
                ):
                    images.append(file)
    return sorted(images)


def main():
    """Main function"""
    # Generate README content
    output = []
    output.append("### Wallpapers\n")
    output.append("This my collection of wallpapers that I find visually pleasing. ")
    output.append("I do not take credit for any of these, most of then are found on ")
    output.append("/r/unixporn or wallhaven.cc.\n")
    output.append("\nPreviews are dynamically generated below:\n")

    # Statically define folders and titles
    folders_and_titles = [
        ("ultrawide", "Ultrawide (21:9 or close enough)"),
        ("vertical", "Vertical (Portrait Mode)"),
    ]
    for folder, title in folders_and_titles:
        folder_images = get_all_images(folder)
        if folder_images:
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
