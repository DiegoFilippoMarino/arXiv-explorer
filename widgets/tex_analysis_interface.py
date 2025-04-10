import os
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, Markdown
from utils.tex_parse import summarize_tex_keywords
from utils.tex_clean import clean_all_tex_in_folder
from keywords.tiers import TIERED_KEYWORDS

class TexAnalyzer:
    def __init__(self, library_csv="data/arxiv_library.csv"):
        self.library_csv = library_csv
        self.library_df = pd.read_csv(library_csv)
        self.library_df.dropna(subset=["Arxiv ID"], inplace=True)
        self.keywords = self._load_all_keywords()
        self.dropdown = None
        self.output = widgets.Output()

    def _load_all_keywords(self):
        return [kw for tier in TIERED_KEYWORDS.values() for kw in tier]  

    def _analyze_selected_paper(self, b):
        arxiv_id = self.dropdown.value
        folder = self.library_df[self.library_df["Arxiv ID"] == arxiv_id]["Folder Path"].values[0]

        self.output.clear_output()
        with self.output:
            display(Markdown(f"## 🧪 TeX Analysis for `{arxiv_id}`"))

            # 🔧 Clean tex before summarizing
            result = clean_all_tex_in_folder(folder)
            if not result:
                display(Markdown("⚠️ No `.tex` files were found or cleaned."))
                return

            matches = summarize_tex_keywords(folder, self.keywords)

            if not matches:
                display(Markdown("❌ No keyword matches found in TeX files."))
                return

            for match in matches:
                display(Markdown(
                    f"**🔹 Keyword:** `{match['keyword']}`  \\\n"
                    f"**📑 Section:** *{match['section']}*  \\\n"
                    f"**🧵 Snippet:** {match['snippet']}"
                ))

    

    def render(self):
        # Dropdown for paper selection
        self.dropdown = widgets.Dropdown(
            options=[(row["Title"], row["Arxiv ID"]) for _, row in self.library_df.iterrows()],
            description="Paper:",
            layout=widgets.Layout(width="90%")
        )

        analyze_btn = widgets.Button(description="🔍 Analyze TeX", button_style="info")
        analyze_btn.on_click(self._analyze_selected_paper)

        display(Markdown("### 🔬 Analyze TeX Content of a Paper"))
        display(widgets.VBox([self.dropdown, analyze_btn, self.output]))
