import os
import webbrowser
from functools import partial
import ipywidgets as widgets
from IPython.display import display, Markdown
import pandas as pd
from utils.match import safe_split
from utils.library import update_library
from utils.tex_clean import clean_all_tex_in_folder
import ast

def parse_keywords(cell):
    if pd.isna(cell):
        return []
    if isinstance(cell, list):
        return cell
    if isinstance(cell, str):
        try:
            # Try to parse if it's a stringified list
            parsed = ast.literal_eval(cell)
            if isinstance(parsed, list):
                return parsed
            else:
                return [kw.strip() for kw in cell.split(",") if kw.strip()]
        except Exception:
            return [kw.strip() for kw in cell.split(",") if kw.strip()]
    return []

class ArxivKeywordInterface:
    def __init__(self, df, pdf_base_dir="pdfs"):
        self.df = df.copy()
        self.df["All Keywords"] = self.df["All Keywords"].apply(parse_keywords)
        self.all_keywords = sorted(set(kw for row in self.df["All Keywords"] for kw in row))

        self.dropdowns = []
        self.pdf_base_dir = pdf_base_dir
        self.output = widgets.Output()
        self.dropdown_box = widgets.HBox()

        self.add_button = widgets.Button(description="➕ Add Keyword", button_style="info")
        self.reset_button = widgets.Button(description="🔁 Reset", button_style="warning")
        self.show_button = widgets.Button(description="📄 Display Results", button_style="success")
        self.remove_button = widgets.Button(description="❌ Remove Last", button_style="danger")

        self._setup_ui()

    def _setup_ui(self):
        self.add_button.on_click(self.add_dropdown)
        self.reset_button.on_click(self.reset_dropdowns)
        self.remove_button.on_click(self.remove_last_dropdown)
        self.show_button.on_click(self.display_results)

        self.add_dropdown()
        display(Markdown("## 🔍 Build a Filter by Stacking Keywords"))
        display(widgets.HBox([self.add_button, self.remove_button, self.reset_button, self.show_button]))
        display(self.dropdown_box)
        display(self.output)

    def add_dropdown(self, b=None):
        dd = widgets.Dropdown(
            options=[""] + self.all_keywords,
            value="",
            layout=widgets.Layout(width="200px", margin="0 5px 0 0")
        )
        self.dropdowns.append(dd)
        self.dropdown_box.children = self.dropdowns

    def remove_last_dropdown(self, b=None):
        if self.dropdowns:
            self.dropdowns.pop()
            self.dropdown_box.children = self.dropdowns

    def reset_dropdowns(self, b=None):
        self.dropdowns.clear()
        self.dropdown_box.children = []
        self.output.clear_output()

    def display_results(self, b=None):
        selected = [dd.value for dd in self.dropdowns if dd.value]
        self.output.clear_output()

        if not selected:
            with self.output:
                display(Markdown("ℹ️ Select at least one keyword to begin filtering."))
            return

        filtered_df = self.df[self.df["All Keywords"].apply(lambda kws: all(kw in kws for kw in selected))]

        with self.output:
            display(Markdown(f"### 📄 Papers containing: {', '.join(f'{kw}' for kw in selected)}"))
            display(Markdown(f"**Matches found:** {len(filtered_df)}"))

            for _, row in filtered_df.iterrows():
                self._render_result(row)

    def _render_result(self, row):
        arxiv_id = row["Link"].split("/")[-1]
        folder_path = os.path.join(self.pdf_base_dir, arxiv_id)

        title_html = widgets.HTML(
            value=f"<b><a href='{row['Link']}' target='_blank'>{row['Title']}</a></b> — <i>{row['Category']}</i>, {row['Published']}"
        )

        summary_box = widgets.Output()
        toggle_btn = widgets.Button(description="🔍 Show Summary", layout=widgets.Layout(width="150px"))

        def on_toggle_summary(b, box=summary_box, summary=row["Summary"]):
            if b.description.startswith("🔍"):
                box.clear_output()
                with box:
                    display(Markdown(f"**Summary:** {summary}"))
                b.description = "🙈 Hide Summary"
            else:
                box.clear_output()
                b.description = "🔍 Show Summary"

        toggle_btn.on_click(on_toggle_summary)

        pdf_btn = widgets.Button(description="📥 Download PDF", layout=widgets.Layout(width="160px"))

        def download_pdf(b):
            try:
                os.makedirs(folder_path, exist_ok=True)
                pdf_path = os.path.join(folder_path, f"{arxiv_id}.pdf")
                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

                if os.path.exists(pdf_path):
                    b.description = "✅ PDF Ready"
                    b.button_style = "success"
                else:
                    import requests
                    r = requests.get(pdf_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
                    if r.status_code == 200:
                        with open(pdf_path, "wb") as f:
                            f.write(r.content)
                        b.description = "✅ PDF Ready"
                        b.button_style = "success"
                        score = row.get("Score", 0)
                        score = int(score) if pd.notna(score) else 0
                        update_library(
                            arxiv_id,
                            row["Title"],
                            row["Category"],
                            score,
                            row["Published"],
                            pdf=True,
                            summary=row.get("Summary", ""),
                            keywords=row.get("All Keywords", "")
                        )
                    else:
                        b.description = "❌ PDF Failed"
                        b.button_style = "danger"
            except Exception as e:
                b.description = "❌ PDF Error"
                b.button_style = "danger"
                print(f"PDF Download Error ({arxiv_id}): {e}")

        pdf_btn.on_click(download_pdf)

        tex_btn = widgets.Button(description="📦 Download TeX", layout=widgets.Layout(width="160px"))

        def download_tex(b):
            try:
                os.makedirs(folder_path, exist_ok=True)
                tex_url = f"https://arxiv.org/src/{arxiv_id}"
                tex_path = os.path.join(folder_path, f"{arxiv_id}.tar.gz")

                if os.path.exists(tex_path):
                    b.description = "✅ TeX Ready"
                    b.button_style = "success"
                else:
                    import requests
                    r = requests.get(tex_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
                    if r.status_code == 200:
                        with open(tex_path, "wb") as f:
                            f.write(r.content)
                        b.description = "✅ TeX Ready"
                        b.button_style = "success"
                        score = row.get("Score", 0)
                        score = int(score) if pd.notna(score) else 0
                        update_library(
                            arxiv_id,
                            row["Title"],
                            row["Category"],
                            score,
                            row["Published"],
                            tex=True,
                            summary=row.get("Summary", ""),
                            keywords=row.get("All Keywords", "")
                        )
                    else:
                        b.description = "❌ TeX Failed"
                        b.button_style = "danger"
            except Exception as e:
                b.description = "❌ TeX Error"
                b.button_style = "danger"
                print(f"TeX Download Error ({arxiv_id}): {e}")

        tex_btn.on_click(download_tex)

        extract_btn = widgets.Button(description="🧹 Extract TeX", layout=widgets.Layout(width="140px"))
        def run_tex_extract(b):
            result = clean_all_tex_in_folder(folder_path)
            extract_btn.description = str(result) if result is not None else "❌ No result"
        
        extract_btn.on_click(run_tex_extract)

        display(widgets.HBox([title_html, toggle_btn, pdf_btn, tex_btn, extract_btn]))
        display(summary_box)
