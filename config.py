from datetime import datetime, timedelta

# Categories of interest (Mathematics, CS, etc.)
CATEGORIES = [
    "math.NA", "math.AP", "math.OC", "math.CA", "math.DS", "math.PR", "math.ST", "math.MP", "math.SP",
    "cs.DS", "cs.NA", "cs.MS", "cs.CE", "cs.CR", "cs.CG", "cs.FL", "cs.SY", "cs.RO", "cs.NE", "cs.SI",
    "q-fin.CP", "q-fin.MF", "q-fin.PR", "q-fin.RM", "q-fin.ST",
    "stat.CO", "stat.ME", "stat.ML", "stat.TH", "stat.AP",
    "q-bio.QM", "q-bio.PE", "q-bio.NC"
]

# Time settings
DAYS_BACK = 30
DATE_THRESHOLD = datetime.now() - timedelta(days=DAYS_BACK)
NOW_STR = datetime.now().strftime("%Y-%m-%d")

# ArXiv fetch configuration
MAX_RESULTS_PER_CATEGORY = 1000
SLEEP_BETWEEN_CALLS = 3.0
TIMEOUT_PER_REQUEST = 15

# File paths
SCAN_LOG_FILE = "data/arxiv_category_log.json"
OUTPUT_RAW = "data/arxiv_recent_raw.csv"
OUTPUT_FILTERED = "data/arxiv_recent_filtered.csv"
OUTPUT_MULTI = "data/arxiv_multi_tier_keywords.csv"
LIBRARY_CSV = "data/arxiv_library.csv"
PDF_BASE_DIR = "pdfs"

# Default column names
LIBRARY_COLUMNS = [
    "Arxiv ID", "Title", "Category", "Score", "Summary", "All Keywords", "Published",
    "PDF Downloaded", "TeX Downloaded", "Folder Path"
]