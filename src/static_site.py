import os
import shutil


def purge_dir(dir_path: str):
    shutil.rmtree(dir_path, True)


def copy_source_dir_to_target_dir(src_path: str, dst_path: str):
    if not os.path.exists(src_path):
        raise ValueError(f"{src_path} source directory doesn't exist")

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    src_contents = os.listdir(src_path)
    for item in src_contents:
        item_path = os.path.join(src_path, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dst_path)
        else:
            copy_source_dir_to_target_dir(item_path, os.path.join(dst_path, item))
