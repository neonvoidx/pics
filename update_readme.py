"""Dynamic README generator for images in directory"""

import os
from string import Template


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
    return images


def main():
    """Main function"""
    images = get_all_images(".")
    vert_images = get_all_images("vertical")
    with open("READMETEMPLATE.md", "r", encoding="utf-8") as template:
        data = template.read()
        template = Template(data)
        output = template.substitute(
            images="\n".join([f"![{image}](./{image})" for image in images]),
            vert_images="\n".join(
                [f"![{image}](./vertical/{image})" for image in vert_images]
            ),
        )
        print(output)
        with open("README.md", "w", encoding="utf-8") as readme:
            readme.write(output)


if __name__ == "__main__":
    main()
