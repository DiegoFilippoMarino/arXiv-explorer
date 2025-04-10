# arXiv Explorer 🔍📚

A local-first pipeline and interactive interface for exploring, filtering, and analyzing arXiv papers — designed with one key goal in mind: **finding papers that contain implementable algorithms, methods, or code-worthy ideas.**

Built for engineers, coders, and researchers who want to turn theory into code.

---

## 🚀 Features

### 🗂️ Paper Discovery
- Automatically fetch and locally store new papers from arXiv (by category).
- Smart keyword matching across **3 tiers** of relevance (e.g., implementation, numerical method, training pipeline, etc.).
- Save and log matched papers with metadata, summary, score, and download status.

### 📚 Personal Library Interface
- Visual browser of all saved papers.
- Buttons to:
  - Show/hide summary
  - Show/hide matched keywords
  - Open PDF directly
- Displays relevance **Score** based on keyword hits.

### 📦 PDF + TeX Downloader
- One-click download for PDF and TeX source files.
- Automatic folder organization by arXiv ID.
- Option to extract and clean `.tex` to raw `.txt` for analysis.

### 📈 Keyword Analysis Tools
- **Co-occurrence heatmap** to visualize which keywords often appear together.
- **Interactive PyVis graph** of keyword relations (threshold-adjustable).

### 💡 Intelligent .TeX Analysis *(in progress)*
- Extract cleaned text from `.tex` source for deeper analysis.
- Planned features:
  - Sentiment/tone classifier: "Is this a proposal? A benchmark? A theoretical contribution?"
  - Semantic search: find similar papers by idea, not keywords.
  - Clustering and concept mapping via co-occurrence graphs.

---

## 🔧 Tech Stack

- Python 3.10+
- [PyTorch, NumPy, Pandas, Matplotlib, Seaborn](https://www.python.org/)
- `pyvis`, `ipywidgets`, `jinja2`, `scikit-learn`
- Local-first architecture (no cloud dependency)
- VSCode / Jupyter for exploration

---

## 📂 Folder Structure

📁 data/           # arxiv_library.csv, keyword matches, scores, logs, etc.
📁 pdfs/           # Downloaded PDFs and TeX sources, organized by arXiv ID
📁 widgets/        # Jupyter-based UI components (library view, keyword filter, analysis tools)
📁 utils/          # Utility modules: downloaders, matchers, scorers, co-occurrence tools
📁 keywords/       # Tiered keyword lists used for scoring and filtering
📄 main.ipynb      # Main control notebook: run discovery, filtering, download, analysis


---

## 🔍 Why?

As a developer passionate about code and theory, I wanted a way to:

- **Cut through arXiv clutter** and focus on papers that offer implementable ideas.
- **Track and analyze** those papers offline.
- **Build a portfolio** by turning research into code.

---

## 📌 Roadmap

- [x] Paper downloader + keyword matcher
- [x] Library browser with summary/keywords
- [x] Co-occurrence analysis
- [x] Relevance scoring
- [ ] Tone classifier (rule-based → ML)
- [ ] Semantic similarity search (via embeddings)
- [ ] Paper clustering and thematic grouping
- [ ] Tagging system + personal notes

---

## 📄 License

This project is licensed under the **MIT License** – free to use, fork, and contribute.

---

## 🙋‍♂️ Author

**Diego Filippo Marino**  
[GitHub](https://github.com/DiegoFilippoMarino)

Contributions, feedback, and ideas are welcome!
