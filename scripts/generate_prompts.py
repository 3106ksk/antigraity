import os
import re
import sys
import datetime
import argparse

def create_prompt_content(slide_content):
    template = """以下の説明文を元に、見やすいスライド資料を作成してください。

・フォーマット
アスペクト比: 16:9
解像度: 2K

・デザイン
シンプルな白背景、黒文字、メインカラーは青、フラットーカラー
イメージキャラクターとしてかわいい黒猫。
小物はワイン、本、ペン、ノートを必要に応じて使用すること。
見やすいスッキリした図解にしてください。
最後に文字を清書するように再生成してください。文字以外の要素は変更禁止です。

・説明文
{content}
"""
    return template.format(content=slide_content.strip())

def sanitize_filename(text):
    # Remove special characters and replace spaces with underscores, keeps japanese characters
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    text = text.replace(" ", "_")
    return text[:50] # Limit length

def extract_title(content):
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1)
    match = re.search(r'^##\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1)
    return "Untitled"

def main():
    parser = argparse.ArgumentParser(description='Split Marp slides into prompt files.')
    parser.add_argument('input_file', help='Path to the input markdown file (e.g., slides.md)')
    args = parser.parse_args()

    input_path = args.input_file
    
    if not os.path.exists(input_path):
        print(f"Error: File {input_path} not found.")
        sys.exit(1)

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Split by Marp slide delimiter (---)
    # Using regex to handle potential whitespace around the delimiter
    slides = re.split(r'^\s*---\s*$', content, flags=re.MULTILINE)

    # Filter out empty slides and the initial configuration block if present
    valid_slides = []
    for i, slide in enumerate(slides):
        if i == 0 and "marp: true" in slide:
            continue # Skip header
        if not slide.strip():
            continue
        valid_slides.append(slide)

    # Create output directory
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_dir = os.path.join("prompts", timestamp)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Generating prompts in: {output_dir}")

    for i, slide in enumerate(valid_slides):
        title = extract_title(slide)
        safe_title = sanitize_filename(title)
        filename = f"{i+1:02d}_{safe_title}.md"
        filepath = os.path.join(output_dir, filename)
        
        prompt_content = create_prompt_content(slide)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(prompt_content)
        
        print(f"Created: {filename}")

if __name__ == "__main__":
    main()
