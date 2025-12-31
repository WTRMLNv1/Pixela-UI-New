# Save_chart.py
# Save a heatmap chart of Pixela pixel data
# -----------------------------------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from datetime import datetime, timedelta
import requests, time
import os
from Functions.getCreds import get_creds


def save_chart(): 
    # --- CONFIG ---
    creds = get_creds()
    USERNAME = creds['username']
    GRAPH_ID = creds["lastGraphID"]
    TOKEN = creds['tokenID']
    HEADERS = {"X-USER-TOKEN": TOKEN}
    weeks = 20
    days_per_week = 7

    # --- RETRY HELPER ---
    def fetch_with_retry(url, headers=None, max_retries=5, delay=1):
        """Fetch JSON with retries if 503 or Pixela 25% reject."""
        for attempt in range(max_retries):
            resp = requests.get(url, headers=headers)
            # Case 1: outright 503 (service unavailable)
            if resp.status_code == 503:
                time.sleep(delay)
                continue
            # Case 2: special Pixela reject message
            try:
                j = resp.json()
                if j.get("isRejected"):  # Pixela's 25% reject flag
                    time.sleep(delay)
                    continue
                return j
            except Exception:
                # not JSON (like 404 page) → don’t retry
                return None
        return None  # give up after retries

    # --- FETCH PIXEL DATA ---
    url = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}/pixels?withBody=true"
    data = fetch_with_retry(url, headers=HEADERS, max_retries=5, delay=2)

    if not data:
        print("Failed to fetch pixel data after retries.")
        return

    pixels = {}
    for entry in data.get("pixels", []):
        d = entry["date"]        # "20250817"
        q = int(entry["quantity"])
        pixels[d] = q

    # print("Fetched pixel data:", pixels)

    # --- DATES (compare .date() to avoid time-of-day gotchas) ---
    today = datetime.today().date()
    start_date = today - timedelta(days=weeks * days_per_week - 1)
    all_dates = [start_date + timedelta(days=i) for i in range(weeks * days_per_week)]

    # --- BUILD GRID AND FUTURE MASK ---
    grid = np.zeros((days_per_week, weeks), dtype=int)
    future_mask = np.zeros_like(grid, dtype=bool)

    for i, d in enumerate(all_dates):
        week = i // days_per_week
        day = i % days_per_week
        if d > today:
            future_mask[day, week] = True
        else:
            grid[day, week] = pixels.get(d.strftime("%Y%m%d"), 0)

    # --- NORMALIZE (avoid /0) ---
    max_val = grid.max() if grid.max() > 0 else 1
    grid_norm = grid / max_val

    mask_condition = (grid_norm == 0) & (~future_mask)
    masked_grid = np.ma.masked_where(mask_condition, grid_norm)

    # --- PLOT ---
    rows, cols = grid.shape
    cell_size = 0.3
    fig, ax = plt.subplots(figsize=(cols * cell_size, rows * cell_size))

    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    cmap = matplotlib.colormaps["Greens"].copy()
    cmap.set_bad(color="black")

    ax.imshow(masked_grid, cmap=cmap, aspect="equal")

    future_arr = np.zeros_like(grid_norm)
    future_arr[future_mask] = 1.0
    future_ma = np.ma.masked_where(~future_mask, future_arr)
    gray_cmap = mcolors.ListedColormap(["lightgray"])
    ax.imshow(future_ma, cmap=gray_cmap, alpha=0.6, aspect="equal")

    ax.axis("off")
    plt.tight_layout()
    folder = os.path.join(os.path.dirname(__file__), "assets")
    os.makedirs(folder, exist_ok=True)

    filepath = os.path.join(folder, "heatmap.png")
    plt.savefig(filepath, dpi=150, facecolor="black")
# To test:
if __name__ == "__main__":
    save_chart()