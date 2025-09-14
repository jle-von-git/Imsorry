import generator


def main():
    generator.copy_dir("static/", "public/")
    generator.generate_page_recursive("content/", "template.html", "public/")
    """
    generator.generate_page(
        "content/index.md", "template.html",
        "public/index.html"
    )
    generator.generate_page(
        "content/blog/glorfindel/index.md", "template.html",
        "public/blog/glorfindel/index.md"
    )
    generator.generate_page(
        "content/blog/tom/index.md", "template.html",
        "public/blog/tom/index.md"
    )
    generator.generate_page(
        "content/blog/majesty/index.md", "template.html",
        "public/blog/majesty/index.md"
    )
    generator.generate_page(
        "content/contact/index.md", "template.html",
        "public/contact/index.md"
    )
    """

main()