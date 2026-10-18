# Tango

A lightweight static site generator built with Python.

Tango transforms Markdown content into static HTML, serves sites locally, watches for file changes, and automatically reloads your browser while you work.

## Features

- Markdown to HTML generation
- Recursive content processing
- Template-based page rendering
- Static asset copying
- Configurable site settings with `tango.toml`
- Local development server
- File watching
- Live browser reload
- GitHub Pages friendly output

# Quick Start

Navigate to a Tango site:

```bash
cd my-site
```

Start the development server:

```bash
tango dev
```

Open:

```text
http://localhost:8888
```

Edit files in:

```text
content/
static/
template.html
tango.toml
```

Tango will automatically:

- Rebuild the site
- Refresh the browser
- Keep serving your site

# Installation

## Using uv

Clone Tango:

```bash
git clone <your-tango-repository>
cd tango
```

Install dependencies:

```bash
uv sync
```

Install Tango as a CLI tool:

```bash
uv tool install .
```

Verify installation:

```bash
tango --help
```

# Site Structure

```text
my-site/
├── content/
│   ├── index.md
│   └── blog/
├── static/
│   ├── styles.css
│   └── images/
├── docs/
├── template.html
└── tango.toml
```

# Configuration

Create a `tango.toml` file in the site root.

```toml
title = "My Website"

[deployment]
base_path = "/"
```

For GitHub Pages project sites:

```toml
title = "My Website"

[deployment]
base_path = "/my-site/"
```

# Commands

## Build

Generate the site into the `docs` directory.

```bash
tango build
```

Build a different site:

```bash
tango build ../my-site
```

## Serve

Serve the generated site locally.

```bash
tango serve
```

Custom port:

```bash
tango serve --port 3000
```

## Development Mode

Build, serve, watch files, and live reload.

```bash
tango dev
```

Custom port:

```bash
tango dev --port 3000
```

## Example

Markdown:

```markdown
# Hello World

Welcome to my Tango-powered website.
```

Generated HTML:

```html
<h1>Hello World</h1>
<p>Welcome to my Tango-powered website.</p>
```

# Roadmap

## Completed

- [x] Static site generation
- [x] Recursive page generation
- [x] Static asset handling
- [x] CLI packaging
- [x] Build command
- [x] Serve command
- [x] Development server
- [x] File watching
- [x] Live reload
- [x] TOML configuration

## Planned

- [ ] Theme support
- [ ] Site scaffolding (`tango new`)
- [ ] Build statistics
- [ ] GitHub Actions templates
- [ ] Plugin system

## AI usage 

- README.md was generated with AI based on the project spec
- AI assistance was used for dev live server reload and websocket
- All other code was human written
