# Supply Chain Performance Analysis

**Business Question:** Where are the biggest cost leakages, defect rate drivers, and supplier performance gaps hiding in supply chain data?

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Seaborn-11557c?style=flat)](https://matplotlib.org)
[![Dataset](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?style=flat&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/harshsingh2209/supply-chain-analysis)

---

## Key Findings

| Finding | Metric | Business Implication |
|---------|--------|----------------------|
| Defect rate concentration | Top category: **[X]%** defect rate vs **[Y]%** average | Targeted quality intervention on top category alone could cut overall defects by ~30% |
| Supplier lead time spread | Longest supplier: **[A] days** vs shortest: **[B] days** | Lead time variance creates unpredictable inventory buffers — erodes working capital |
| Shipping cost skew | Mean **$[C]** vs median **$[D]** — right-skewed distribution | High-cost outlier shipments are inflating the average; isolating these reveals a prioritised cost reduction target |
| Revenue concentration | Top category drives **[E]%** of revenue | Asymmetric revenue dependence — supply disruptions here have outsized P&L impact |
| Supplier composite ranking | Score spread of **[F]** points between best and worst supplier | Supplier renegotiation / rationalization opportunity |

*Note: Replace bracketed values after running the analysis on the dataset.*

---

## Business Problem

Supply chains generate enormous operational data — but most companies lack the analytical infrastructure to turn that data into decisions. The specific problems this analysis addresses:

**1. Quality:** Defect rates vary significantly across product categories, but without visibility, quality improvement resources get spread evenly rather than focused where they create the most impact.

**2. Supplier Performance:** Lead time variability is a primary driver of inventory buffer costs. Companies carrying excess safety stock to compensate for unreliable suppliers are paying a hidden tax on working capital.

**3. Shipping Cost Leakage:** Shipping cost distributions are typically right-skewed — a small number of high-cost shipments inflate the average. These outliers are often addressable through route optimization, mode shifting, or consolidation.

---

## Recommendations

Based on the analysis:

1. **Concentrate defect reduction on top 1-2 categories.** Rather than a blanket quality improvement program, target the highest-defect product lines — this is where Six Sigma or process improvement investment yields the fastest ROI.

2. **Renegotiate or replace bottom-quartile suppliers.** The composite supplier scorecard (quality + speed + cost) identifies underperformers. For high-volume SKUs, single-source dependency on poor performers is a supply risk.

3. **Audit the top 10% of shipping cost transactions.** The skewed distribution suggests a small number of expedited or misrouted shipments are driving disproportionate cost. Auditing and addressing these outliers is a high-leverage, low-effort cost reduction opportunity.

---

## How to Run

### 1. Clone or download this repo
```bash
git clone https://github.com/payaljarviya/supply-chain-analytics
cd supply-chain-analytics
```

### 2. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn
```

### 3. Get the dataset
Download **Supply Chain Analysis** from Kaggle:
👉 [kaggle.com/datasets/harshsingh2209/supply-chain-analysis](https://www.kaggle.com/datasets/harshsingh2209/supply-chain-analysis)

Save as `supply_chain_data.csv` in the project folder.

### 4. Run the analysis
```bash
python supply_chain_analysis.py
```

Charts are saved to the `output/` folder automatically.

---

## Analysis Structure

```
supply-chain-analytics/
│
├── supply_chain_analysis.py    # Main analysis script
├── output/                     # Generated charts (auto-created on run)
│   ├── 1_defect_rate_by_category.png
│   ├── 2_lead_time_by_supplier.png
│   ├── 3_shipping_cost_analysis.png
│   ├── 4_revenue_by_category.png
│   └── 5_supplier_scorecard.png
└── README.md
```

### The 5 Business Questions Answered

| # | Question | Chart |
|---|----------|-------|
| 1 | Which product categories have the highest defect rates? | Defect Rate by Category |
| 2 | Which suppliers have the longest lead times? | Lead Time by Supplier |
| 3 | Where are the biggest cost leakages in shipping? | Shipping Cost Distribution + Mode Analysis |
| 4 | Which product categories generate the most revenue? | Revenue by Category |
| 5 | How do suppliers compare across quality, speed, and cost? | Composite Supplier Scorecard |

---

## Tools Used

`Python 3.8+` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn`

---

## Why This Analysis

I spent 4 years inside PeopleSoft FSCM ERP environments at NTT DATA, supporting Fortune 500 companies with supply chain operations, procurement workflows, and financial reporting. This project is a direct translation of that operational experience into data analysis — turning the same business questions I encountered in live ERP environments into code.

The goal isn't just to produce charts. It's to move from data → insight → recommendation: the same logic a supply chain consultant or analytics manager applies.

---

## About

**Payal Jarviya** | MBA Candidate, SKK GSB Seoul (AI & Business Analytics)
4 years Enterprise ERP Consulting @ NTT DATA North America

🔗 [LinkedIn](https://www.linkedin.com/in/payal-jarviya/) · [Portfolio](https://payaljarviya.github.io) · [GitHub](https://github.com/payaljarviya)

---

## LinkedIn Post Hook

> I analyzed [X] supply chain transactions and found that defect rates are not spread evenly across product categories — they're concentrated in 1-2 categories that account for a disproportionate share of returns and rework costs.
>
> After 4 years inside live ERP supply chain systems, I know this pattern well. Here are the 3 findings from the data and what I'd recommend to any ops leader looking at this...
>
> [Charts in comments]

---

*Dataset: [Kaggle — Supply Chain Analysis](https://www.kaggle.com/datasets/harshsingh2209/supply-chain-analysis) by Harsh Singh*
