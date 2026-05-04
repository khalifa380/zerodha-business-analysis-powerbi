import pandas as pd
import numpy as np

np.random.seed(42)

# ================================================================
# TABLE 1 — MONTHLY BUSINESS METRICS (42 months: Jan 2022 - Jun 2025)
# REAL ANCHOR POINTS:
# Jan 2022 → Active Clients: 60 lakh, Market Share: 15%
# Jan 2023 → Active Clients: 66 lakh, Market Share: 22%
# Dec 2024 → Active Clients: 81.2 lakh, Market Share: 16.41%
# Jun 2025 → Active Clients: 72.6 lakh, Market Share: 16%
# FY23 Revenue: 6875 Cr | FY24: 8320 Cr | FY25: 7000 Cr
# ================================================================

months = pd.date_range(start="2022-01-01", end="2025-06-01", freq="MS")

active_clients_anchors = {
    "2022-01": 6000000, "2022-12": 6589285,
    "2023-01": 6642857, "2023-06": 7017857, "2023-12": 7232142,
    "2024-01": 7285714, "2024-05": 7500000, "2024-12": 8120000,
    "2025-01": 8040000, "2025-02": 7960000, "2025-03": 7843333,
    "2025-04": 7726666, "2025-05": 7610000, "2025-06": 7260000,
}

active_clients_list = []
for i, month in enumerate(months):
    key = month.strftime("%Y-%m")
    if key in active_clients_anchors:
        active_clients_list.append(active_clients_anchors[key])
    else:
        if i < 12:
            val = 6000000 + (i * 53571)
        elif i < 24:
            val = 6642857 + ((i - 12) * 49107)
        else:
            val = 7285714 + ((i - 24) * 88571)
        active_clients_list.append(int(val))

market_share_anchors = {
    "2022-01": 15.0, "2022-12": 21.41,
    "2023-01": 22.0, "2023-06": 20.29, "2023-12": 19.32,
    "2024-01": 19.08, "2024-05": 18.11, "2024-12": 16.41,
    "2025-01": 16.35, "2025-02": 16.30, "2025-06": 16.00,
}

market_share_list = []
for i, month in enumerate(months):
    key = month.strftime("%Y-%m")
    if key in market_share_anchors:
        market_share_list.append(market_share_anchors[key])
    else:
        if i < 12:
            val = 15.0 + (i * 0.535)
        elif i < 24:
            val = 22.0 - ((i - 12) * 0.222)
        else:
            val = 19.08 - ((i - 24) * 0.257)
        market_share_list.append(round(val, 2))

def get_monthly_revenue(month):
    year = month.year
    m = month.month
    if year == 2022:
        return round(6875 / 12 + np.random.uniform(-30, 30), 2)
    elif year == 2023:
        base = 6875 / 12 if m <= 3 else 8320 / 12
        return round(base + np.random.uniform(-30, 30), 2)
    elif year == 2024:
        base = 8320 / 12 if m <= 3 else 7000 / 12
        return round(base + np.random.uniform(-30, 30), 2)
    else:
        return round(7000 / 12 * 0.60 + np.random.uniform(-20, 20), 2)

revenue_list = [get_monthly_revenue(m) for m in months]

def get_arpu(month):
    year = month.year
    m = month.month
    if year == 2022: return 82
    elif year == 2023: return 82 if m <= 3 else 92
    elif year == 2024: return 92 if m <= 3 else 73
    else: return 70

arpu_list = [get_arpu(m) for m in months]

def get_avg_trades(month):
    year = month.year
    m = month.month
    if year == 2022: return round(np.random.uniform(22, 25), 2)
    elif year == 2023: return round(np.random.uniform(27, 30), 2)
    elif year == 2024:
        return round(np.random.uniform(22, 26), 2) if m <= 9 else round(np.random.uniform(17, 20), 2)
    else: return round(np.random.uniform(12, 15), 2)

avg_trades_list = [get_avg_trades(m) for m in months]

def get_fno_pct(month):
    year = month.year
    m = month.month
    if year == 2022: return round(np.random.uniform(0.62, 0.68), 3)
    elif year == 2023: return round(np.random.uniform(0.64, 0.70), 3)
    elif year == 2024:
        return round(np.random.uniform(0.62, 0.68), 3) if m <= 9 else round(np.random.uniform(0.55, 0.60), 3)
    else: return round(np.random.uniform(0.50, 0.56), 3)

fno_pct_list = [get_fno_pct(m) for m in months]
fno_revenue_list = [round(r * p, 2) for r, p in zip(revenue_list, fno_pct_list)]
non_fno_revenue_list = [round(r - f, 2) for r, f in zip(revenue_list, fno_revenue_list)]

churned_list = []
new_signups_list = []
for i, month in enumerate(months):
    if i == 0:
        churned_list.append(0)
        new_signups_list.append(0)
    else:
        diff = active_clients_list[i] - active_clients_list[i-1]
        year = month.year
        if year == 2022:
            churned = int(np.random.uniform(50000, 80000))
            new_signups = churned + max(diff, 0) + int(np.random.uniform(0, 10000))
        elif year == 2023:
            churned = int(np.random.uniform(60000, 90000))
            new_signups = churned + max(diff, 0) + int(np.random.uniform(0, 10000))
        elif year == 2024 and month.month <= 9:
            churned = int(np.random.uniform(70000, 100000))
            new_signups = churned + max(diff, 0) + int(np.random.uniform(0, 10000))
        else:
            churned = int(abs(diff) + np.random.uniform(80000, 130000))
            new_signups = max(0, churned + diff)
        churned_list.append(churned)
        new_signups_list.append(new_signups)

churn_rate_list = [
    round((c / a) * 100, 4) if a > 0 and c > 0 else 0
    for c, a in zip(churned_list, active_clients_list)
]

referral_list = [round(np.random.uniform(25, 30), 2) for _ in months]
complaint_list = [0.0137] * len(months)
groww_share_list = [min(round(14.0 + (i * 0.30), 2), 26.59) for i in range(len(months))]

def get_user_status(m):
    y = m.year
    if y == 2022: return 58, 28, 14
    elif y == 2023: return 56, 29, 15
    elif y == 2024: return 55, 30, 15
    else: return 53, 31, 16

active_pct_list, inactive_pct_list, dormant_pct_list = [], [], []
for m in months:
    a, i, d = get_user_status(m)
    active_pct_list.append(a)
    inactive_pct_list.append(i)
    dormant_pct_list.append(d)

def get_new_user_pct(m):
    y = m.year
    if y == 2022: return 35, 65
    elif y == 2023: return 30, 70
    elif y == 2024: return 18, 82
    else: return 12, 88

new_user_list, existing_user_list = [], []
for m in months:
    n, e = get_new_user_pct(m)
    new_user_list.append(n)
    existing_user_list.append(e)

def get_tier_split(m):
    y = m.year
    if y == 2022: return 65, 25, 10
    elif y == 2023: return 60, 28, 12
    elif y == 2024: return 55, 30, 15
    else: return 50, 32, 18

tier1_list, tier2_list, tier3_list = [], [], []
for m in months:
    t1, t2, t3 = get_tier_split(m)
    tier1_list.append(t1)
    tier2_list.append(t2)
    tier3_list.append(t3)

df1 = pd.DataFrame({
    "Month": [m.strftime("%b-%Y") for m in months],
    "Active_Clients": active_clients_list,
    "New_Signups": new_signups_list,
    "Churned_Clients": churned_list,
    "Churn_Rate_%": churn_rate_list,
    "Revenue_Cr": revenue_list,
    "FnO_Revenue_Cr": fno_revenue_list,
    "Non_FnO_Revenue_Cr": non_fno_revenue_list,
    "ARPU_Monthly_Rs": arpu_list,
    "Avg_Trades_Per_User": avg_trades_list,
    "Market_Share_%": market_share_list,
    "Groww_Share_%": groww_share_list,
    "Referral_%": referral_list,
    "Complaint_Rate_%": complaint_list,
    "Active_%": active_pct_list,
    "Inactive_%": inactive_pct_list,
    "Dormant_%": dormant_pct_list,
    "New_User_%": new_user_list,
    "Existing_User_%": existing_user_list,
    "Tier1_%": tier1_list,
    "Tier2_%": tier2_list,
    "Tier3_%": tier3_list,
})

# ================================================================
# TABLE 2 — CUSTOMER SEGMENTS (500 rows)
# ================================================================

customer_data = []
for i in range(500):
    city_tier = np.random.choice(["Tier 1","Tier 2","Tier 3"], p=[0.55,0.30,0.15])
    age_group = np.random.choice(["18-25","26-35","36-50","50+"], p=[0.30,0.40,0.20,0.10])
    account_type = np.random.choice(["Trading Only","Investing Only","Both"], p=[0.25,0.35,0.40])
    monthly_trades = np.random.randint(10,50) if account_type=="Trading Only" else (np.random.randint(0,5) if account_type=="Investing Only" else np.random.randint(3,25))
    primary_product = np.random.choice(["Equity","F&O","Mutual Fund","SIP"], p=[0.35,0.30,0.20,0.15])
    active_status = np.random.choice(["Active","Inactive","Dormant"], p=[0.55,0.30,0.15])
    tenure_months = np.random.randint(1, 60)
    complaint_flag = np.random.choice([1,0], p=[0.000137, 0.999863])
    complaints_filed = np.random.randint(1,3) if complaint_flag else 0
    referred_by = np.random.choice(["Referral","Social Media","Organic Search","Ads","Zerodha Varsity"], p=[0.27,0.25,0.20,0.18,0.10])
    referral_flag = 1 if referred_by == "Referral" else 0
    monthly_revenue = round(np.random.uniform(60,120),2) if active_status=="Active" else (round(np.random.uniform(0,20),2) if active_status=="Inactive" else 0)
    customer_data.append([i+1, city_tier, age_group, account_type, monthly_trades, primary_product, active_status, tenure_months, complaints_filed, referred_by, referral_flag, complaint_flag, monthly_revenue])

df2 = pd.DataFrame(customer_data, columns=[
    "Customer_ID","City_Tier","Age_Group","Account_Type","Monthly_Trades",
    "Primary_Product","Active_Status","Tenure_Months","Complaints_Filed",
    "Referred_By","Referral_Flag","Complaint_Flag","Monthly_Revenue_Rs"
])

# ================================================================
# TABLE 3 — COMPETITOR COMPARISON (42 months)
# ================================================================

comp_data = []
z, g, u, a = 6000000, 3800000, 1800000, 2500000
for i, month in enumerate(months):
    z += np.random.randint(30000,90000) if i < 35 else -np.random.randint(60000,130000)
    g += np.random.randint(100000, 180000)
    u += np.random.randint(20000, 60000)
    a += np.random.randint(30000, 80000)
    total = z + g + u + a
    comp_data.append([month.strftime("%b-%Y"), z, g, u, a,
        round(z/total*100,2), round(g/total*100,2),
        round(u/total*100,2), round(a/total*100,2)])

df3 = pd.DataFrame(comp_data, columns=[
    "Month","Zerodha_Clients","Groww_Clients","Upstox_Clients","AngelOne_Clients",
    "Zerodha_Share_%","Groww_Share_%","Upstox_Share_%","AngelOne_Share_%"
])
df3.loc[df3["Month"]=="Dec-2024", ["Zerodha_Share_%","Groww_Share_%","AngelOne_Share_%","Upstox_Share_%"]] = [16.41, 26.59, 15.67, 5.83]

# ================================================================
# TABLE 4 — FEATURE IMPROVEMENT TRACKER
# ================================================================

df4 = pd.DataFrame([
    {"Feature":"Zero AMC Demat Account","Priority":1,"Impact":"Stop losing users to Groww immediately","Est_Users_Affected_Lakh":15,"Est_Revenue_Impact_Cr":-300,"Competitor_Has_It":"Groww ✅","Implementation_Ease":"Medium","Category":"Pricing"},
    {"Feature":"Live Chat Support","Priority":2,"Impact":"Fix #1 complaint","Est_Users_Affected_Lakh":20,"Est_Revenue_Impact_Cr":200,"Competitor_Has_It":"Groww ✅","Implementation_Ease":"Medium","Category":"Support"},
    {"Feature":"Beginner Mode in Kite App","Priority":3,"Impact":"Capture first-time investors","Est_Users_Affected_Lakh":25,"Est_Revenue_Impact_Cr":400,"Competitor_Has_It":"Groww ✅","Implementation_Ease":"Hard","Category":"Product"},
    {"Feature":"Regional Language Support","Priority":4,"Impact":"Win Tier 2 and Tier 3 cities","Est_Users_Affected_Lakh":30,"Est_Revenue_Impact_Cr":500,"Competitor_Has_It":"Partial","Implementation_Ease":"Medium","Category":"Product"},
    {"Feature":"AI Personal Finance Assistant","Priority":5,"Impact":"Future-proof the platform","Est_Users_Affected_Lakh":40,"Est_Revenue_Impact_Cr":600,"Competitor_Has_It":"Neither ❌","Implementation_Ease":"Hard","Category":"AI/Tech"},
    {"Feature":"External Portfolio Tracker","Priority":6,"Impact":"Increase user stickiness","Est_Users_Affected_Lakh":20,"Est_Revenue_Impact_Cr":250,"Competitor_Has_It":"Groww ✅","Implementation_Ease":"Medium","Category":"Product"},
    {"Feature":"Rebuild Referral Program","Priority":7,"Impact":"Restore organic user acquisition","Est_Users_Affected_Lakh":10,"Est_Revenue_Impact_Cr":300,"Competitor_Has_It":"Both ✅","Implementation_Ease":"Easy","Category":"Growth"},
    {"Feature":"Goal-Based SIP Automation","Priority":8,"Impact":"Retain passive investors","Est_Users_Affected_Lakh":18,"Est_Revenue_Impact_Cr":350,"Competitor_Has_It":"Groww ","Implementation_Ease":"Medium","Category":"Product"},
    {"Feature":"Better NRI Experience","Priority":9,"Impact":"Capture high-value NRI accounts","Est_Users_Affected_Lakh":5,"Est_Revenue_Impact_Cr":400,"Competitor_Has_It":"Neither ","Implementation_Ease":"Hard","Category":"Expansion"},
    {"Feature":"Loyalty & Gamification Program","Priority":10,"Impact":"Reduce long-term churn","Est_Users_Affected_Lakh":35,"Est_Revenue_Impact_Cr":450,"Competitor_Has_It":"Neither ","Implementation_Ease":"Easy","Category":"Retention"},
])

# ================================================================
# SAVE TO EXCEL — 4 SHEETS
# ================================================================

with pd.ExcelWriter("Zerodha_Complete_Dataset.xlsx", engine="openpyxl") as writer:
    df1.to_excel(writer, sheet_name="Monthly_Business_Metrics", index=False)
    df2.to_excel(writer, sheet_name="Customer_Segments", index=False)
    df3.to_excel(writer, sheet_name="Competitor_Comparison", index=False)
    df4.to_excel(writer, sheet_name="Feature_Improvement_Tracker", index=False)

print("✅ Zerodha_Complete_Dataset.xlsx generated successfully!")
print(f"📊 Sheet 1 — Monthly Business Metrics : {len(df1)} rows x {len(df1.columns)} columns")
print(f"👥 Sheet 2 — Customer Segments        : {len(df2)} rows x {len(df2.columns)} columns")
print(f"🏆 Sheet 3 — Competitor Comparison    : {len(df3)} rows x {len(df3.columns)} columns")
print(f"💡 Sheet 4 — Feature Improvement      : {len(df4)} rows x {len(df4.columns)} columns")
print("\n✅ File saved in your current folder — ready to import into Power BI!")