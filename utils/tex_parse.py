import re
from pathlib import Path


def extract_sections(tex_path):
    """
    Parses a LaTeX .tex file and returns a dict of sections and their content.
    """
    with open(tex_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Remove comments
    content = re.sub(r"(?<!\\)%.*", "", content)

    # Find all sections and their contents
    pattern = re.compile(r"\\(section|subsection|subsubsection)\*?\{([^}]*)\}")
    matches = list(pattern.finditer(content))

    sections = {}
    for i, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section_content = content[start:end].strip()
        sections[title] = section_content

    return sections


def find_keywords_in_sections(section_dict, keywords):
    """
    Given a dict of sections -> content, search for keywords and return matches with context.
    """
    results = []
    for section, text in section_dict.items():
        lowered = text.lower()
        for kw in keywords:
            if kw.lower() in lowered:
                # Extract snippet around keyword (first occurrence)
                match = re.search(re.escape(kw), text, flags=re.IGNORECASE)
                if match:
                    snippet_start = max(0, match.start() - 100)
                    snippet_end = min(len(text), match.end() + 100)
                    snippet = text[snippet_start:snippet_end].replace("\n", " ")
                    results.append({
                        "keyword": kw,
                        "section": section,
                        "snippet": snippet.strip()
                    })
    return results


def summarize_tex_keywords(folder_path, keywords):
    """
    Run full analysis: find .tex files, extract sections, match keywords, return structured matches.
    """
    folder = Path(folder_path)
    tex_dir = folder / "tex"
    results = []

    if not tex_dir.exists():
        return []

    for tex_file in tex_dir.glob("*.tex"):
        section_map = extract_sections(tex_file)
        keyword_hits = find_keywords_in_sections(section_map, keywords)
        for hit in keyword_hits:
            hit["tex_file"] = tex_file.name
            hit["arxiv_id"] = folder.name
        results.extend(keyword_hits)

    return results
