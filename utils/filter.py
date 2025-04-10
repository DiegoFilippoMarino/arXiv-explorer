import pandas as pd
from tqdm import tqdm
from datetime import datetime
from utils.match import match_keywords
from keywords.tiers import TIERED_KEYWORDS


def filter_papers_by_keywords(df, tiered_keywords=TIERED_KEYWORDS):
    """
    Filters a DataFrame of arXiv papers by tiered keyword matches.
    Returns filtered DataFrame and list of matched papers.
    """
    results = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Filtering Papers"):
        combined_text = str(row["Title"]) + " " + str(row["Summary"])
        for tier, keywords in tiered_keywords.items():
            matched = match_keywords(combined_text, keywords)
            if matched:
                row_data = row.to_dict()
                row_data["Tier"] = tier
                row_data["Matched Keywords"] = ", ".join(matched)
                results.append(row_data)
                break  # Only first matching tier is assigned

    return pd.DataFrame(results)


def extract_multi_tier_matches(df, tiered_keywords=TIERED_KEYWORDS):
    """
    For each paper, collect all keyword matches across all tiers.
    """
    results = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Matching Tiers"):
        combined_text = str(row["Title"]) + " " + str(row["Summary"])
        tier_matches = {}
        all_matches = []

        for tier, keywords in tiered_keywords.items():
            matched = match_keywords(combined_text, keywords)
            tier_matches[tier] = matched
            all_matches.extend(matched)

        if all_matches:
            row_data = row.to_dict()
            row_data["Tier 1 Keywords"] = ", ".join(tier_matches.get("Tier 1", []))
            row_data["Tier 2 Keywords"] = ", ".join(tier_matches.get("Tier 2", []))
            row_data["Tier 3 Keywords"] = ", ".join(tier_matches.get("Tier 3", []))
            row_data["All Keywords"] = ", ".join(sorted(set(all_matches)))
            results.append(row_data)

    return pd.DataFrame(results)