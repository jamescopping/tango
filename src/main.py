from static_site import (
    copy_source_dir_to_target_dir,
    generate_pages_recursive,
    purge_dir,
)

PUBLIC = "./public"
STATIC = "./static"
CONTENT = "./content"
TEMPLATE = "./template.html"


def main():
    purge_dir(PUBLIC)
    copy_source_dir_to_target_dir(STATIC, PUBLIC)
    generate_pages_recursive(CONTENT, TEMPLATE, PUBLIC)

main()
