from static_site import copy_source_dir_to_target_dir, generate_page, purge_dir

PUBLIC = "./public"
STATIC = "./static"
CONTENT = "./content"
TEMPLATE = "./template.html"


def main():
    purge_dir(PUBLIC)
    copy_source_dir_to_target_dir(STATIC, PUBLIC)
    generate_page(f"{CONTENT}/index.md", TEMPLATE, PUBLIC)

main()
