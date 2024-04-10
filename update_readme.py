""" Dynamic README generator for images in directory """

import os
from string import Template


def get_all_images():
    """Gets all images in current directory"""
    images = []
    for _, _, files in os.walk("."):
        for file in files:
            if (
                file.endswith(".png")
                or file.endswith(".jpg")
                or file.endswith(".jpeg")
                or file.endswith(".gif")
            ):
                images.append(file)
    return images


def generate_image_markdown(image):
    """Generates markdown for image"""
    return f"![{image}]({image})"


def main():
    """Main function"""
    images = get_all_images()
    with open("READMETEMPLATE.md", "r", encoding="utf-8") as template:
        data = template.read()
        template = Template(data)
        output = template.substitute(
            images="\n".join([generate_image_markdown(image) for image in images])
        )
        print(output)
        with open("README.md", "w", encoding="utf-8") as readme:
            readme.write(output)


if __name__ == "__main__":
    main()
