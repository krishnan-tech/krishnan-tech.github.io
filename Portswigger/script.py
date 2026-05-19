import os
import re
import shutil
from datetime import datetime

# ============ USER CONFIG =============
# Where your Obsidian images live (source)
ASSETS_FOLDER = r'D:\Obsidian\Personal\Obsidian\04 - assets\images'

# Where to put images for Hugo static site
HUGO_STATIC_IMAGES_BASE = r'D:\Projects\g4nd1v-blog\static\images\Portswigger'

# Where to write the converted content files
HUGO_CONTENT_BASE = r'D:\Projects\g4nd1v-blog\content\en\Portswigger'

# File extension to process
MD_EXT = '.md'
# ======================================

def make_title_from_filename(fname):
    # fname without extension, e.g. "Portswigger-XSS" -> "Portswigger XSS Writeups"
    base = os.path.splitext(fname)[0]
    parts = base.split('-')
    title = " ".join(parts) + " Writeups"
    return title

def make_tag_from_filename(fname):
    # try to use the part after first hyphen as tag; fallback to filename
    base = os.path.splitext(fname)[0]
    if '-' in base:
        tag = base.split('-', 1)[1]
    else:
        tag = base
    # Clean up common file name chars and uppercase tag
    tag = re.sub(r'[_\s]+', ' ', tag).strip()
    return tag.upper()

def make_description(title):
    # short generated description
    return f"A collection of {title.lower()} with examples, notes and writeups."

def hugo_front_matter(title, date_iso, description, tag, category, image):
    # ensure YAML values that may contain special characters are quoted
    # image is already a path string
    return f"""---
title: "{title}"
date: {date_iso}
description: "{description}"
draft: false
hideToc: false
enableToc: true
enableTocContent: true
author: g4nd1v
authorEmoji: 👨‍
tags:
  - Portswigger
  - {tag}
categories:
  - {category}
image: {image}
---
"""

def process_markdown_file(md_path):
    fname = os.path.basename(md_path)
    basename = os.path.splitext(fname)[0]
    print(f"\nProcessing: {fname}")

    # read file
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # If file already starts with front matter (---), skip adding template to avoid overwriting.
    if content.lstrip().startswith('---'):
        print("  Skipping: file already has front matter (starts with '---').")
        return

    # Prepare metadata
    title = make_title_from_filename(fname)
    tag = make_tag_from_filename(fname)
    category = 'portswigger'
    date_iso = '2025-10-11'  # e.g. 2025-10-11T13:05:00.123456
    description = make_description(title)
    # default image: use first image if present, otherwise empty
    image_path_for_frontmatter = ''

    # Find pasted images pattern like: ![[Portswigger/images/Pasted image 1.png]]
    # Accept png/jpg/jpeg and optional spaces
    image_pattern = re.compile(r'!\[\[Pasted image (\d+)\.(png|jpg|jpeg)\]\]', flags=re.IGNORECASE)
    matches = image_pattern.findall(content)

    # Destination image folder for this file
    dest_image_folder = os.path.join(HUGO_STATIC_IMAGES_BASE, basename)
    os.makedirs(dest_image_folder, exist_ok=True)

    # Copy images and replace links
    if matches:
        for match in matches:
            image_id, ext = match
            src_filename = f'Pasted image {image_id}.{ext}'
            src_path = os.path.join(ASSETS_FOLDER, src_filename)
            dest_filename = f'Pasted_image_{image_id}.{ext}'
            dest_path = os.path.join(dest_image_folder, dest_filename)

            if os.path.exists(src_path):
                try:
                    shutil.copy(src_path, dest_path)
                    print(f"  Copied image {src_filename} -> {dest_path}")
                except Exception as e:
                    print(f"  ERROR copying {src_path}: {e}")
                    continue
            else:
                print(f"  WARNING: source image not found: {src_path}")
                # still replace link to point to expected location (but it will be broken until image exists)

            # Replace Obsidian-style image with markdown image using site path
            web_path = f'/images/Portswigger/{basename}/{dest_filename}'
            content = re.sub(
                rf'!\[\[Pasted image {re.escape(image_id)}\.(?:png|jpg|jpeg)\]\]',
                f'![Pasted image {image_id}]({web_path})',
                content,
                flags=re.IGNORECASE
            )

            # Set the first image as frontmatter image if not set
            if not image_path_for_frontmatter:
                image_path_for_frontmatter = web_path

    # Build front matter (if no image, set empty string)
    image_field = image_path_for_frontmatter if image_path_for_frontmatter else ''
    front = hugo_front_matter(title, date_iso, description, tag, category, image_field)

    # Compose final content: front matter + blank line + original content
    final_content = front + "\n" + content

    # Write to Hugo content folder (lowercase file name as in your original example)
    os.makedirs(HUGO_CONTENT_BASE, exist_ok=True)
    output_fname = fname.lower()
    output_path = os.path.join(HUGO_CONTENT_BASE, output_fname)

    with open(output_path, 'w', encoding='utf-8') as out_f:
        out_f.write(final_content)

    print(f"  Wrote: {output_path}")

def main():
    cwd = os.getcwd()
    print(f"Running in: {cwd}")
    md_files = [f for f in os.listdir(cwd) if f.lower().endswith(MD_EXT) and os.path.isfile(f)]
    if not md_files:
        print("No markdown files found in current directory.")
        return

    for md in md_files:
        process_markdown_file(os.path.join(cwd, md))

if __name__ == '__main__':
    main()
