import argparse

from src.static_site_generator import (
    copy_source_dir_to_target_dir,
    generate_pages_recursive,
    purge_dir,
)

parser = argparse.ArgumentParser(description="tango is basic static site generator")
parser.add_argument("base_path", type=str, help="Base Path")
args = parser.parse_args()

base_path = args.base_path
if base_path is None or len(base_path) == 0:
    base_path = "/"

SITE_GEN_OUTPUT_DIR = "./docs"
STATIC = "./static"
CONTENT = "./content"
TEMPLATE = "./template.html"


def main():
    purge_dir(SITE_GEN_OUTPUT_DIR)
    copy_source_dir_to_target_dir(STATIC, SITE_GEN_OUTPUT_DIR)
    generate_pages_recursive(CONTENT, TEMPLATE, SITE_GEN_OUTPUT_DIR, base_path)

main()
