import os
import pandas as pd
from config import LIBRARY_CSV, LIBRARY_COLUMNS

# Ensure library CSV exists
if os.path.exists(LIBRARY_CSV):
    library_df = pd.read_csv(LIBRARY_CSV)
else:
    library_df = pd.DataFrame(columns=LIBRARY_COLUMNS)
    library_df.to_csv(LIBRARY_CSV, index=False)

def update_library(arxiv_id, title, category, score, published, pdf=False, tex=False, summary=None, keywords=None):
    folder_path = os.path.join("pdfs", arxiv_id)
    os.makedirs(folder_path, exist_ok=True)

    exists = library_df["Arxiv ID"] == arxiv_id
    if exists.any():
        idx = library_df[exists].index[0]
        if pdf:
            library_df.at[idx, "PDF Downloaded"] = "✅"
        if tex:
            library_df.at[idx, "TeX Downloaded"] = "✅"
        if summary is not None:
            library_df.at[idx, "Summary"] = summary
        if keywords is not None:
            formatted = ", ".join(keywords) if isinstance(keywords, list) else keywords
            library_df.at[idx, "All Keywords"] = formatted
    else:
        library_df.loc[len(library_df)] = {
            "Arxiv ID": arxiv_id,
            "Title": title,
            "Category": category,
            "Score": score,
            "Summary": summary or "",
            "All Keywords": ", ".join(keywords) if isinstance(keywords, list) else (keywords or ""),
            "Published": published,
            "PDF Downloaded": "✅" if pdf else "",
            "TeX Downloaded": "✅" if tex else "",
            "Folder Path": folder_path
        }

    library_df.to_csv(LIBRARY_CSV, index=False)
