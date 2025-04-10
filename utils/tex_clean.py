import re
from pathlib import Path

def clean_tex_file(tex_path):
    with open(tex_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    content = re.sub(r"(?<!\\)%.*", "", content)
    content = re.split(r"\\begin\{document\}", content, maxsplit=1)[-1]
    content = re.split(r"\\(?:bibliography|end\{document\})", content, maxsplit=1)[0]
    content = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", "", content)
    content = re.sub(r"\\begin\{(figure|table|equation|align)\}.*?\\end\{\1\}", "", content, flags=re.DOTALL)
    content = re.sub(r"\$.*?\$", "", content)
    content = re.sub(r"\\\[.*?\\\]", "", content, flags=re.DOTALL)
    content = re.sub(r"\$\$.*?\$\$", "", content, flags=re.DOTALL)
    content = re.sub(r"[{}]", "", content)
    content = re.sub(r"\\", "", content)
    content = re.sub(r"\s+", " ", content)

    return content.strip()

def clean_all_tex_in_folder(paper_folder):
    from pathlib import Path

    tex_dir = Path(paper_folder) / "tex"
    output_dir = Path(paper_folder) / "cleaned"
    tar_path = Path(paper_folder) / f"{Path(paper_folder).name}.tar.gz"

    print(f"🧪 Looking for tar file at: {tar_path}")
    if not tar_path.exists():
        print("❌ No .tar.gz found.")
        return "❌ No .tar.gz found"

    if tex_dir.exists():
        print("✅ Already extracted.")
        return "✅ Already extracted"

    try:
        tex_dir.mkdir(exist_ok=True)
        import tarfile
        with tarfile.open(tar_path, "r:gz") as tar:
            members = [m for m in tar.getmembers() if m.name.endswith(".tex")]
            print(f"🧵 Found {len(members)} .tex files")
            if not members:
                return "⚠️ No .tex files in archive"
            tar.extractall(path=tex_dir, members=members)

        return f"✅ Extracted {len(members)} .tex files"
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return f"❌ Error: {e}"
