import numpy as np
import pandas as pd
from scipy.stats import ttest_rel
from scipy.signal import find_peaks
from scipy.special import expit
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# --- 0) Constants & Configuration ---
part_ids = list(range(1, 28))  # [1, 2, …, 27]

# Engagement‐to‐binary parameters (a, b, c)
a = 10
b = 0.05
c = 0.50
binary_col = f'Engagement_logsig_a{int(a*10):02d}_b{int(b*100):02d}_c{int(c*100):02d}'

# Tolerance for nearest‐timestamp merge (in seconds)
# If engagement is 30 Hz, GSR is 128 Hz, you might only need ~0.02 or 0.05s as tolerance.
merge_tolerance = 0.05  

# Precompute which IDs use skiprows=30 vs skiprows=31
skip30 = {1, 4, 5, 7, 9, 12, 13}
skip31 = set(part_ids) - skip30

# Storage for results
mean_gsr_engaged = []
mean_gsr_not     = []
peak_counts      = []
valid_part_ids   = []

# --- 1) Loop over participants ---
for pid in part_ids:
    # 1.1) Read CSV with correct skiprows
    skip = 30 if pid in skip30 else 31
    df_raw = pd.read_csv(f'participant_files/{pid}.csv', skiprows=skip)

    # 1.2) Extract/clean engagement and GSR columns, convert Timestamp to seconds
    df_raw['Timestamp'] = df_raw['Timestamp'].astype(float) / 1000.0  # ms→s

    # Engagement DataFrame
    engagement_df = df_raw[['Timestamp', 'Engagement']].dropna(subset=['Timestamp', 'Engagement']).copy()

    # GSR DataFrame
    gsr_df = df_raw[['Timestamp', 'GSR Conductance CAL']].dropna(subset=['Timestamp', 'GSR Conductance CAL']).copy()

    # 1.3) Sort both by timestamp
    engagement_df.sort_values('Timestamp', inplace=True)
    engagement_df.reset_index(drop=True, inplace=True)

    gsr_df.sort_values('Timestamp', inplace=True)
    gsr_df.reset_index(drop=True, inplace=True)

    # 1.4) Merge each engagement row to nearest GSR row (within tolerance)
    merged = pd.merge_asof(
        engagement_df,
        gsr_df,
        on='Timestamp',
        direction='nearest',
        tolerance=merge_tolerance
    )

    # 1.5) Drop rows where we didn’t find any close‐enough GSR
    merged = merged.dropna(subset=['GSR Conductance CAL'])
    if merged.empty:
        # If after merging there's no valid GSR, skip this participant
        continue

    # 1.6) Scale Engagement → [0,1] and create binary engaged column
    mm = MinMaxScaler(feature_range=(0, 1))
    merged['Engagement_MinMaxScaled'] = mm.fit_transform(merged[['Engagement']])

    x = merged['Engagement_MinMaxScaled'].values
    scores = expit(a * (x - b))
    merged[binary_col] = (scores > c).astype(int)

    early_eng = merged[merged['Timestamp'] <= 300]['Engagement_MinMaxScaled'].mean()
    late_eng  = merged[(merged['Timestamp'] >= 660) & 
                      (merged['Timestamp'] <= 900)]['Engagement_MinMaxScaled'].mean()

    # 1.7) Split GSR by engaged vs not engaged
    gsr_vals     = merged['GSR Conductance CAL'].values
    engaged_mask = merged[binary_col].values == 1
    not_mask     = merged[binary_col].values == 0

    gsr_engaged = gsr_vals[engaged_mask]
    gsr_not     = gsr_vals[not_mask]

    # Compute means (with correct length check)
    mean_e = gsr_engaged.mean() if (len(gsr_engaged) > 0) else np.nan
    mean_n = gsr_not.mean()     if (len(gsr_not)     > 0) else np.nan

    # If either is NaN, skip this participant’s GSR‐comparison
    if np.isnan(mean_e) or np.isnan(mean_n):
        continue

    mean_gsr_engaged.append(mean_e)
    mean_gsr_not.append(mean_n)
    valid_part_ids.append(pid)

    # 1.8) Peak detection on the merged GSR array
    # Use a threshold slightly above the mean GSR, or whatever your logic demands
    threshold = np.mean(gsr_vals) + 0.05
    peaks, _ = find_peaks(gsr_vals, height=threshold)
    peak_counts.append(len(peaks))

# --- 2) Paired t-test on GSR means ---
eng_means = np.array(mean_gsr_engaged)
not_means = np.array(mean_gsr_not)

t_stat_gsr, p_val_gsr = ttest_rel(eng_means, not_means)

print("Per‐participant mean GSR during engaged vs not engaged:")
for pid, e_mean, n_mean in zip(valid_part_ids, eng_means, not_means):
    print(f"  P{pid:02d}: GSR_eng = {e_mean:.3f}, GSR_not = {n_mean:.3f}")

print(f"\nPaired t-test (GSR_eng vs GSR_not): t = {t_stat_gsr:.3f}, p = {p_val_gsr:.4f}")

# --- 3) Average GSR peak count ---
if peak_counts:
    print(f"\nAverage GSR peak count per participant: {np.mean(peak_counts):.2f}")
else:
    print("\nNo peak counts were recorded (all participants had invalid data).")