"""Dynamic README generator for images in directory"""

import os
from string import Template


def get_all_images(walk_path):
    """Gets all images in current directory"""
    images = []
    for _, _, files in os.walk(walk_path):
        for file in files:
            if (
                file.endswith(".png")
                or file.endswith(".jpg")
                or file.endswith(".jpeg")
                or file.endswith(".gif")
            ):
                # Only add images not in vertical/ for ultrawide
                if walk_path == ".":
                    # Exclude images in vertical/
                    if not os.path.relpath(root, ".").startswith("vertical"):
                        images.append(file)
                else:
                    images.append(file)
    return images


def generate_image_markdown(image):
    """Generates markdown for image"""
    return f"![{image}](./vertical/{image})"


def main():
    """Main function"""
    images = get_all_images(".")
    vert_images = get_all_images("vertical")
    with open("READMETEMPLATE.md", "r", encoding="utf-8") as template:
        data = template.read()
        template = Template(data)
        output = template.substitute(
            images="\n".join([generate_image_markdown(image) for image in images]),
            vert_images="\n".join(
                [generate_image_markdown(image) for image in vert_images]
            ),
        )
        print(output)
        with open("README.md", "w", encoding="utf-8") as readme:
            readme.write(output)


if __name__ == "__main__":
    main()
