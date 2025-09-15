import generator
import sys


def main():
    basepath = sys.argv[1]
    if basepath == None: basepath = "/"
    generator.copy_dir("static/", "docs/")
    generator.generate_page_recursive("content/", "template.html", "docs/", basepath)

main()