import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('GuttmacherInstituteAbortionDataByState.csv')

# Clean columns
col_travel = '% of residents obtaining abortions who traveled out of state for care, 2020'
col_deserts = '% of counties without a known clinic, 2020'
col_change = '% change in abortion rate, 2017-2020'
col_occ_rate = 'No. of abortions per 1,000 women aged 15–44, by state of occurrence, 2020'
col_res_rate = 'No. of abortions per 1,000 women aged 15–44, by state of residence, 2020'
col_occ_total = 'No. of abortions, by state of occurrence, 2020'

cols_to_num = [col_travel, col_deserts, col_change, col_occ_rate, col_res_rate, col_occ_total]
for c in cols_to_num:
    df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '', regex=False).str.replace('unavailable', 'NaN', regex=False), errors='coerce')

# --- VIZ 1A ---
top_12_travel = df[['U.S. State', col_travel]].dropna().sort_values(col_travel, ascending=True).tail(12)
plt.figure(figsize=(10, 6))
# Create red colormap based on value
norm = plt.Normalize(top_12_travel[col_travel].min(), top_12_travel[col_travel].max())
colors = plt.cm.Reds(norm(top_12_travel[col_travel]))
plt.barh(top_12_travel['U.S. State'], top_12_travel[col_travel], color=colors, edgecolor='darkred')
plt.title('Out-of-State Travel for Abortion Services', fontsize=14, fontweight='bold', color='darkred')
plt.xlabel('% of Residents Traveling Out of State (2020)', fontsize=12)
plt.xlim(0, 100)
for i, v in enumerate(top_12_travel[col_travel]):
    plt.text(v - 4, i, f"{int(v)}%", color='white', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('viz1a_travel.png', dpi=300)
plt.close()

# --- VIZ 1B ---
top_deserts = df[['U.S. State', col_deserts]].dropna().sort_values(col_deserts, ascending=False).head(20)
plt.figure(figsize=(12, 6))
plt.bar(top_deserts['U.S. State'], top_deserts[col_deserts], color='firebrick')
plt.ylim(85, 100)
plt.title('Abortion Clinic Deserts: Counties Without Clinics', fontsize=14, fontweight='bold', color='darkred')
plt.ylabel('% of Counties Without a Known Clinic (2020)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('viz1b_deserts.png', dpi=300)
plt.close()

# --- VIZ 2A ---
growth_states = df[df[col_change] > 0][['U.S. State', col_change]].sort_values(col_change, ascending=False).head(20)
plt.figure(figsize=(12, 6))
plt.bar(growth_states['U.S. State'], growth_states[col_change], color='teal')
plt.title('Growing Access: States with Increasing Abortion Rates (2017-2020)', fontsize=14, fontweight='bold', color='teal')
plt.ylabel('% Increase in Abortion Rate', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('viz2a_growth.png', dpi=300)
plt.close()

# --- VIZ 2B ---
top_10_providers = df.sort_values(col_occ_total, ascending=False).head(10)
x = np.arange(len(top_10_providers))
width = 0.35

plt.figure(figsize=(12, 6))
plt.bar(x - width/2, top_10_providers[col_occ_rate], width, label='State of Occurrence', color='teal')
plt.bar(x + width/2, top_10_providers[col_res_rate], width, label='State of Residence', color='mediumturquoise')
plt.title('Abortion Rates in Top 10 Provider States: Occurrence vs Residence', fontsize=14, fontweight='bold', color='teal')
plt.ylabel('Rate (per 1,000 women aged 15-44)', fontsize=12)
plt.xticks(x, top_10_providers['U.S. State'], rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.savefig('viz2b_rates.png', dpi=300)
plt.close()
