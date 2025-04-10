import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
from pyvis.network import Network
import os


def build_cooccurrence_matrix(df, keyword_col="All Keywords", min_cooccurrence=2):
    """
    Builds a symmetric co-occurrence matrix for keywords that appear in the same paper.
    """
    co_counts = Counter()

    for keywords in df[keyword_col]:
        if isinstance(keywords, str):
            keywords = [kw.strip() for kw in keywords.split(",") if kw.strip()]
        keywords = list(set(keywords))
        for pair in combinations(sorted(keywords), 2):
            co_counts[pair] += 1

    # Extract all keywords that meet the threshold
    keywords = set()
    for (kw1, kw2), count in co_counts.items():
        if count >= min_cooccurrence:
            keywords.update([kw1, kw2])

    keywords = sorted(keywords)
    matrix = pd.DataFrame(0, index=keywords, columns=keywords)

    for (kw1, kw2), count in co_counts.items():
        if kw1 in matrix.index and kw2 in matrix.columns:
            matrix.at[kw1, kw2] = count
            matrix.at[kw2, kw1] = count  # symmetric

    return matrix


def plot_cooccurrence_heatmap(matrix, title="Keyword Co-occurrence Heatmap"):
    """
    Plot the co-occurrence matrix as a heatmap.
    """
    plt.figure(figsize=(min(24, 1 + matrix.shape[0] * 0.4), 10))
    sns.heatmap(matrix, cmap="YlGnBu", linewidths=.5, annot=True, fmt=".0f", cbar_kws={'label': 'Co-occurrence Count'})
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def build_pyvis_cooccurrence_graph(matrix, output_html="cooccurrence_graph.html", threshold=2):
    """
    Generate an interactive graph from the co-occurrence matrix using PyVis.
    """
    net = Network(height="750px", width="100%", notebook=True, bgcolor="#ffffff", font_color="#000000")
    net.barnes_hut()
    
    # Cast all matrix values to native Python int
    matrix = matrix.astype(int)

    for node in matrix.columns:
        net.add_node(str(node), label=str(node), title=str(node))

    for i, src in enumerate(matrix.index):
        for j, tgt in enumerate(matrix.columns):
            if j <= i:
                continue  # avoid duplicates
            weight = matrix.iat[i, j]
            if int(weight) >= threshold:  # force cast here too
                net.add_edge(
                    str(src),
                    str(tgt),
                    value=int(weight),
                    title=f"{int(weight)} papers"
                )


    net.show(output_html)
    print(f"✅ Interactive graph saved to: {os.path.abspath(output_html)}")
