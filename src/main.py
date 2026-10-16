from static_site import copy_source_dir_to_target_dir, purge_dir

PUBLIC_DIR = "./public"
STATIC_DIR = "./static"


def main():
    purge_dir(PUBLIC_DIR)
    copy_source_dir_to_target_dir(STATIC_DIR, PUBLIC_DIR)

main()
