import os
import shutil

from markdown_parser import extract_title, markdown_to_html_node


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    if not os.path.exists(dir_path_content):
        raise ValueError(
            f"{dir_path_content} source directory to content doesn't exist"
        )

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
        print(f"{dest_dir_path} directory created")

    src_contents = os.listdir(dir_path_content)
    for item in src_contents:
        item_path = os.path.join(dir_path_content, item)
        new_dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            generate_page(item_path, template_path, new_dest_path)
        else:
            generate_pages_recursive(item_path, template_path, new_dest_path)


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as markdown_fd:
        print(f"Reading {from_path}...", end="")
        markdown_contents = markdown_fd.read()
        print("DONE")

    with open(template_path) as template_fd:
        print(f"Reading {template_path}...", end="")
        template_contents = template_fd.read()
        print("DONE")

    print("Parsing markdown to html nodes...", end="")
    html_node = markdown_to_html_node(markdown_contents)
    print("DONE")
    print("Generating raw html...", end="")
    html_content = html_node.to_html()
    print("DONE")

    print("Extracting title...", end="")
    title = extract_title(markdown_contents)
    print("DONE")
    print("Replacing template Title + Content...", end="")
    page = template_contents.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_content)
    print("DONE")

    path = os.path.dirname(dest_path)
    print("Creating destination directories...", end="")
    os.makedirs(path, exist_ok=True)
    print("DONE")
    filename = os.path.basename(from_path)
    filename = filename.split(".")[0] + ".html"
    with open(os.path.join(path, filename), "w") as html_file:
        print(f"Creating {filename}...", end="")
        html_file.write(page)
        print("DONE")

def purge_dir(dir_path: str):
    shutil.rmtree(dir_path, True)
    print(f"Directory tree deleted {dir_path}")


def copy_source_dir_to_target_dir(src_dir_path: str, dest_dir_path: str):
    if not os.path.exists(src_dir_path):
        raise ValueError(f"{src_dir_path} source directory doesn't exist")

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
        print(f"{dest_dir_path} directory created")

    src_contents = os.listdir(src_dir_path)
    for item in src_contents:
        item_path = os.path.join(src_dir_path, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_dir_path)
            print(f"Copied {item} to {dest_dir_path}")
        else:
            copy_source_dir_to_target_dir(item_path, os.path.join(dest_dir_path, item))
