import argparse

from .static_site_generator import (
    copy_source_dir_to_target_dir,
    generate_pages_recursive,
    purge_dir,
)

parser = argparse.ArgumentParser(description="tango is basic static site generator")

parser.add_argument(
    "site_root",
    type=str,
    help="Path to site root",
)

parser.add_argument(
    "base_path",
    type=str,
    nargs="?",
    default="/",
    help="Base URL path",
)

args = parser.parse_args()

SITE_ROOT = args.site_root

SITE_GEN_OUTPUT_DIR = f"{SITE_ROOT}/docs"
STATIC = f"{SITE_ROOT}/static"
CONTENT = f"{SITE_ROOT}/content"
TEMPLATE = f"{SITE_ROOT}/template.html"


def main():
    purge_dir(SITE_GEN_OUTPUT_DIR)
    copy_source_dir_to_target_dir(STATIC, SITE_GEN_OUTPUT_DIR)
    generate_pages_recursive(
        CONTENT,
        TEMPLATE,
        SITE_GEN_OUTPUT_DIR,
        args.base_path,
    )


main()
