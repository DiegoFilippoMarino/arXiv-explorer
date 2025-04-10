import os
import pandas as pd
from IPython.display import display, Markdown
import ipywidgets as widgets
import webbrowser

def display_library_interface(library_csv="arxiv_library.csv"):
    if not os.path.exists(library_csv):
        print("❌ Library CSV not found.")
        return

    df = pd.read_csv(library_csv)
    if df.empty:
        display(Markdown("ℹ️ No papers in your library yet."))
        return

    for _, row in df.iterrows():
        arxiv_id = row.get("Arxiv ID", "N/A")
        title = row.get("Title", "Untitled")
        category = row.get("Category", "")
        published = row.get("Published", "")
        folder_path = row.get("Folder Path", "")
        summary = row.get("Summary")
        summary = str(summary) if pd.notna(summary) else "No summary available."
        keywords = row.get("All Keywords")
        keywords = str(keywords) if pd.notna(keywords) else "None"
        score = row.get("Score")
        score_str = f" — 🧮 Score: {int(score)}" if pd.notna(score) else ""
        title_html = widgets.HTML(
            value=f"<b>{title}</b> — <i>{category}</i>, {published}{score_str}"
        )

        summary_box = widgets.Output()
        keywords_box = widgets.Output()

        def toggle_summary(b, box=summary_box, text=summary):
            if b.description.startswith("📄"):
                box.clear_output()
                with box:
                    display(Markdown(f"**Summary:** {text}"))
                b.description = "🙈 Hide Summary"
            else:
                box.clear_output()
                b.description = "📄 Show Summary"

        def toggle_keywords(b, box=keywords_box, kw_text=keywords):
            if b.description.startswith("🏷️"):
                box.clear_output()
                with box:
                    display(Markdown("**Keywords:** " + kw_text))
                b.description = "🙈 Hide Keywords"
            else:
                box.clear_output()
                b.description = "🏷️ Show Keywords"

        def open_pdf(b, path=folder_path, arxiv_id=arxiv_id):
            pdf_path = os.path.join(path, f"{arxiv_id}.pdf")
            if os.path.exists(pdf_path):
                webbrowser.open("file://" + os.path.abspath(pdf_path))
            else:
                print(f"❌ PDF not found: {pdf_path}")

        summary_btn = widgets.Button(description="📄 Show Summary", layout=widgets.Layout(width="140px"))
        keywords_btn = widgets.Button(description="🏷️ Show Keywords", layout=widgets.Layout(width="140px"))
        open_btn = widgets.Button(description="📂 Open PDF", layout=widgets.Layout(width="140px"))

        summary_btn.on_click(toggle_summary)
        keywords_btn.on_click(toggle_keywords)
        open_btn.on_click(open_pdf)

        controls = widgets.HBox([summary_btn, keywords_btn, open_btn])
        display(widgets.VBox([title_html, controls, summary_box, keywords_box]))

