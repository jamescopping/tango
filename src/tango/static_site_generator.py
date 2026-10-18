import os
import shutil

from .live_reload import LIVE_RELOAD_SCRIPT
from .logger import info, success
from .markdown_parser import extract_title, markdown_to_html_node


def generate_pages_recursive(
    dir_path_content: str,
    template_path: str,
    dest_dir_path: str,
    base_path: str,
    dev_mode: bool = False,
):
    if not os.path.exists(dir_path_content):
        raise ValueError(
            f"{dir_path_content} source directory to content doesn't exist"
        )

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
        info(f"Created directory {dest_dir_path}")

    src_contents = os.listdir(dir_path_content)
    for item in src_contents:
        item_path = os.path.join(dir_path_content, item)
        new_dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            generate_page(item_path, template_path, new_dest_path, base_path, dev_mode)
        else:
            generate_pages_recursive(
                item_path, template_path, new_dest_path, base_path, dev_mode
            )


def generate_page(
    from_path: str,
    template_path: str,
    dest_path: str,
    base_path: str,
    dev_mode: bool = False,
):
    info(f"Generating page from {from_path}")

    with open(from_path) as markdown_fd:
        markdown_contents = markdown_fd.read()

    with open(template_path) as template_fd:
        template_contents = template_fd.read()

    html_node = markdown_to_html_node(markdown_contents)
    html_content = html_node.to_html()

    title = extract_title(markdown_contents)
    page = template_contents.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_content)
    page = page.replace('href="/', f'href="{base_path}')
    page = page.replace('src="/', f'src="{base_path}')

    if dev_mode:
        page = page.replace("</body>", f"{LIVE_RELOAD_SCRIPT}</body>")

    path = os.path.dirname(dest_path)
    os.makedirs(path, exist_ok=True)
    filename = os.path.basename(from_path)
    filename = filename.split(".")[0] + ".html"
    with open(os.path.join(path, filename), "w") as html_file:
        html_file.write(page)
        success(f"Generated {os.path.join(path, filename)}")


def purge_output_dir(dir_path: str):
    shutil.rmtree(dir_path, True)
    info(f"Removed {dir_path}")


def copy_source_dir_to_target_dir(src_dir_path: str, dest_dir_path: str):
    if not os.path.exists(src_dir_path):
        raise ValueError(f"{src_dir_path} source directory doesn't exist")

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
        info(f"Created directory {dest_dir_path}")

    src_contents = os.listdir(src_dir_path)
    for item in src_contents:
        item_path = os.path.join(src_dir_path, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_dir_path)
            success(f"Copied {item}")
        else:
            copy_source_dir_to_target_dir(item_path, os.path.join(dest_dir_path, item))
