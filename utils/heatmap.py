import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from utils.match import safe_split

def build_keyword_heatmap(df, tier_column="Tier", keyword_column="Matched Keywords"):
    """
    Builds a heatmap of keyword frequencies across tiers.
    """
    df[keyword_column] = df[keyword_column].apply(safe_split)

    tier_keyword_freq = {}
    for tier in df[tier_column].unique():
        tier_df = df[df[tier_column] == tier]
        keyword_counter = Counter()
        for kws in tier_df[keyword_column]:
            keyword_counter.update(kws)
        tier_keyword_freq[tier] = keyword_counter

    all_keywords = sorted(set().union(*[c.keys() for c in tier_keyword_freq.values()]))
    heatmap_data = pd.DataFrame(index=tier_keyword_freq.keys(), columns=all_keywords).fillna(0)

    for tier, counter in tier_keyword_freq.items():
        for kw, count in counter.items():
            heatmap_data.at[tier, kw] = count

    plt.figure(figsize=(min(24, 1 + len(all_keywords) * 0.4), 6))
    sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=.5, cbar_kws={'label': 'Frequency'})
    plt.title("Keyword Frequency Heatmap by Tier")
    plt.xlabel("Keywords")
    plt.ylabel("Tier")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()