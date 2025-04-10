from collections import Counter
import pandas as pd

# You can tune these weights later
TIER_WEIGHTS = {
    "Tier 1": 3,
    "Tier 2": 2,
    "Tier 3": 1,
}

def compute_keyword_score(row):
    """
    Given a row with Tier 1/2/3 Keywords (as lists), compute a weighted score.
    """
    score = 0
    for tier, weight in TIER_WEIGHTS.items():
        kws = row.get(f"{tier} Keywords")
        if isinstance(kws, str):
            kws = [kw.strip() for kw in kws.split(",") if kw.strip()]
        elif not isinstance(kws, list):
            kws = []
        score += weight * len(kws)
    return score

def apply_scoring(df):
    """
    Apply score computation to the full DataFrame. Adds a `Score` column.
    """
    df = df.copy()
    df["Score"] = df.apply(compute_keyword_score, axis=1)
    return df

def plot_score_histogram(df):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    df["Score"].hist(bins=20, color="skyblue", edgecolor="black")
    plt.title("Distribution of Paper Scores")
    plt.xlabel("Score")
    plt.ylabel("Number of Papers")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("❌ Please provide the CSV path as argument.")
        sys.exit(1)

    input_path = sys.argv[1]
    df = pd.read_csv(input_path)
    df = apply_scoring(df)
    df.to_csv(input_path, index=False)
    print(f"✅ Updated scores and saved to: {input_path}")

    if "--plot" in sys.argv:
        plot_score_histogram(df)