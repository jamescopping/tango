import argparse
import http.server
import os
import socketserver
import threading
from functools import partial
from time import sleep

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .config import load_config
from .live_reload import start_live_reload_server, trigger_reload
from .logger import error, header, info
from .static_site_generator import (
    copy_source_dir_to_target_dir,
    generate_pages_recursive,
    purge_output_dir,
)

parser = argparse.ArgumentParser(description="tango is a static site generator")

subparsers = parser.add_subparsers(dest="command", required=True)

build_parser = subparsers.add_parser("build", help="Build a site")

build_parser.add_argument("site_root", nargs="?", default=".", help="Path to site root")

serve_parser = subparsers.add_parser("serve", help="Serve a generated site")

serve_parser.add_argument("site_root", nargs="?", default=".", help="Path to site root")

serve_parser.add_argument(
    "--port",
    type=int,
    default=8888,
)

dev_parser = subparsers.add_parser("dev", help="Build, serve and watch a site")

dev_parser.add_argument("site_root", nargs="?", default=".", help="Path to site root")

dev_parser.add_argument(
    "--port",
    type=int,
    default=8888,
)

def dev_site(site_root: str, port: str):
    build_site(site_root, True)

    server_thread = threading.Thread(
        target=serve_site,
        args=(site_root, port),
        daemon=True,
    )

    server_thread.start()

    observer = Observer()

    handler = TangoFileHandler(site_root)

    observer.schedule(
        handler,
        f"{site_root}/content",
        recursive=True,
    )

    observer.schedule(
        handler,
        f"{site_root}/static",
        recursive=True,
    )

    content_dir = f"{site_root}/content"
    static_dir = f"{site_root}/static"

    info(f"Watching {content_dir}")
    info(f"Watching {static_dir}")

    reload_thread = threading.Thread(
        target=start_live_reload_server,
        daemon=True,
    )

    reload_thread.start()

    observer.start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def build_site(site_root: str, dev_mode: bool = False):

    output_dir = f"{site_root}/docs"
    static_dir = f"{site_root}/static"
    content_dir = f"{site_root}/content"
    html_template = f"{site_root}/template.html"

    config = load_config(site_root)

    base_path = config["deployment"]["base_path"]

    header("Tango Build")
    info(f"Title: {config['title']}")
    info(f"Site: {site_root}")
    info(f"Output: {output_dir}")
    info(f"Base Path: {base_path}")

    purge_output_dir(output_dir)
    copy_source_dir_to_target_dir(static_dir, output_dir)
    generate_pages_recursive(
        content_dir, html_template, output_dir, base_path, dev_mode
    )


def serve_site(site_root: str, port: int):
    output_dir = f"{site_root}/docs"

    if not os.path.exists(output_dir):
        raise ValueError(f"{output_dir} doesn't exist. Run 'tango build' first.")

    header("Tango Server")

    info(f"Site: {output_dir}")
    info(f"URL: http://localhost:{port}")
    info("Press Ctrl+C to stop")

    handler = partial(
        http.server.SimpleHTTPRequestHandler,
        directory=output_dir,
    )

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping Tango server...")


def main():
    args = parser.parse_args()
    if args.command == "build":
        build_site(args.site_root)

    if args.command == "serve":
        serve_site(args.site_root, args.port)

    if args.command == "dev":
        dev_site(args.site_root, args.port)


class TangoFileHandler(FileSystemEventHandler):
    def __init__(self, site_root):
        self.site_root = site_root

    def on_modified(self, event):
        if event.is_directory:
            return

        info(f"Detected change: {event.src_path}")

        try:
            build_site(self.site_root, True)
            trigger_reload()
        except Exception as e:  # noqa: BLE001
            error(str(e))


if __name__ == "__main__":
    main()
