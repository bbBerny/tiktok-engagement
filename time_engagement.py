import numpy as np
import pandas as pd

# List of all participants ids:
part_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]

# Binary column to represent engagement
# Most promising parameters: (a = 10, b = 0.05, c = 0.50)
binary_col = 'Engagement_logsig_a10_b05_c50'

r_values = []

for pid in part_ids:
    # --- 1) Read participants csv (skprows vary in respect to the file)
    if pid in [1,4,5,7,9,12,13]:
        df_p = pd.read_csv(f'participant_files/{pid}.csv', skiprows=30)
    else:
        df_p = pd.read_csv(f'participant_files/{pid}.csv', skiprows=31)
    
    # --- 2) Drop any NaNs in Timestamp or Engagement columns...
    df_p = df_p[['Timestamp', 'Engagement', 'GSR Conductance CAL']].dropna(subset=['Timestamp', 'Engagement'])

    # --- 3) Min-Max scale the Engagement column to [0, 1]
    from sklearn.preprocessing import MinMaxScaler
    mm = MinMaxScaler(feature_range=(0, 1))
    df_p['Engagement_MinMaxScaled'] = mm.fit_transform(df_p[['Engagement']])

    # --- 4) Recompute binary columns from Analysis.ipynb
    from scipy.special import expit
    x = df_p['Engagement_MinMaxScaled'].values
    a = 10      # a = 10    in logsig
    b = 0.05    # b = 0.05  in logsig
    scores = expit(a * (x - b))
    c = 0.50    # c = 0.50  in logsig
    df_p[binary_col] = (scores > c).astype(int)

    # --- 5) Compute Pearson correlation between time and continuous engagement
    time_arr = df_p['Timestamp'].values.astype(float)
    eng_arr  = df_p['Engagement_MinMaxScaled'].values.astype(float)

    # Convert timestamp into seconds
    time_arr = time_arr / 1000

    # Pearson's r:
    if len(time_arr) >= 2 and np.std(eng_arr) > 0:
        r = np.corrcoef(time_arr, eng_arr)[0,1]
    else:
        r = np.nan

    r_values.append(r)

# Convert to NumPy, drop any Nan
r_arr = np.array(r_values, dtype=float)
valid_r = r_arr[~np.isnan(r_arr)]

print('Per-participant Pearson r-values:')
for pid, rval in zip(part_ids, r_values):
    print(f'Participant {pid}: r = {rval:.3f}')


# --- 6) Group level inference: FIsher-transform then one sample t-test
from scipy.stats import ttest_1samp

# Fisher transform: z = atanh(r)
z_vals = np.arctanh(valid_r)

# Test H0: mean(z) = 0 (i.e., mean correlation = 0)
t_stat, p_val = ttest_1samp(z_vals, 0.0)
mean_r = np.mean(valid_r)

print(f'\nGroup-level results:')
print(f'    Mean r across participants          = {mean_r:.3f}')
print(f'    One-sample t-test on Fisher-z:    t = {t_stat:.3f}, p = {p_val:.4f}')

