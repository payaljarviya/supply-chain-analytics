"""
Supply Chain Performance Analysis
==================================
Author: Payal Jarviya
MBA Candidate | SKK GSB Seoul | AI & Business Analytics

Business Problem:
    Supply chains generate enormous amounts of operational data — but most companies
    lack the analytical infrastructure to turn that data into actionable decisions.
    This analysis identifies the top cost leakages, defect rate drivers, and
    supplier performance gaps hidden inside supply chain transaction data.

Dataset: Supply Chain Analysis (Kaggle)
    https://www.kaggle.com/datasets/harshsingh2209/supply-chain-analysis

Instructions:
    1. Download the dataset from the link above
    2. Save as 'supply_chain_data.csv' in the same folder as this script
    3. Run: python supply_chain_analysis.py
    4. Charts will be saved to an 'output/' folder
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# ─── CONFIG ────────────────────────────────────────────────────────────────────
NAVY     = "#1a3a5c"
BLUE     = "#2E75B6"
LIGHT    = "#D5E8F0"
RED      = "#C0392B"
GREEN    = "#27AE60"
ORANGE   = "#E67E22"
GRAY     = "#666666"
BG       = "#f8f9fa"

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.facecolor': BG,
    'figure.facecolor': 'white',
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.titlepad': 12,
})

os.makedirs('output', exist_ok=True)


# ─── LOAD & CLEAN DATA ─────────────────────────────────────────────────────────
def load_and_clean(path='supply_chain_data.csv'):
    df = pd.read_csv(path)
    print(f"\n{'='*60}")
    print(f"  Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"{'='*60}")
    print(f"\nColumns: {list(df.columns)}\n")

    # Standardise column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('/', '_')

    # Drop fully-empty rows
    df.dropna(how='all', inplace=True)

    # Show missing data summary
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if len(missing):
        print("Missing values detected:")
        print(missing.to_string())
    else:
        print("No missing values detected.")

    return df


# ─── HELPER ───────────────────────────────────────────────────────────────────
def save(fig, filename, title=None):
    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold', color=NAVY, y=1.02)
    fig.tight_layout()
    path = f'output/{filename}'
    fig.savefig(path, dpi=150, bbox_inches='tight')
    print(f"  Saved: {path}")
    plt.close(fig)


def add_value_labels(ax, fmt='{:.0f}', fontsize=9, color='white', offset=0.3):
    for bar in ax.patches:
        h = bar.get_height()
        if h > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h - offset,
                fmt.format(h),
                ha='center', va='top',
                fontsize=fontsize, color=color, fontweight='bold'
            )


# ─── ANALYSIS 1: Defect Rate by Product Category ──────────────────────────────
def chart_defect_by_category(df):
    """Which product categories have the highest defect rates?"""
    print("\n[1] Defect Rate by Product Category")

    # Try multiple possible column name patterns
    cat_col   = next((c for c in df.columns if 'product' in c and 'type' in c), None) or \
                next((c for c in df.columns if 'product' in c), None)
    defect_col = next((c for c in df.columns if 'defect' in c), None)

    if not cat_col or not defect_col:
        print(f"  Columns available: {list(df.columns)}")
        print("  Could not find required columns — skipping this chart.")
        return

    grp = df.groupby(cat_col)[defect_col].mean().sort_values(ascending=False)
    avg = grp.mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = [RED if v > avg * 1.2 else BLUE if v > avg else LIGHT for v in grp.values]
    bars = ax.bar(grp.index, grp.values * 100, color=colors, edgecolor='white', linewidth=0.5)

    ax.axhline(avg * 100, color=ORANGE, linestyle='--', linewidth=1.5, label=f'Average: {avg*100:.1f}%')
    ax.set_ylabel('Defect Rate (%)', color=GRAY)
    ax.set_xlabel('')
    ax.set_title('Defect Rate by Product Category')
    ax.legend(fontsize=9)

    for bar, val in zip(bars, grp.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                f'{val*100:.1f}%', ha='center', va='bottom', fontsize=9, color=NAVY, fontweight='bold')

    # Add insight annotation
    worst = grp.index[0]
    ax.annotate(
        f'Highest defect: {worst}\n({grp.iloc[0]*100:.1f}%)',
        xy=(0, grp.iloc[0]*100), xytext=(len(grp)-1.5, grp.iloc[0]*100*0.85),
        arrowprops=dict(arrowstyle='->', color=RED),
        fontsize=9, color=RED, fontweight='bold'
    )

    save(fig, '1_defect_rate_by_category.png')

    print(f"  Key finding: '{worst}' has the highest defect rate at {grp.iloc[0]*100:.1f}%")
    print(f"  Average defect rate: {avg*100:.1f}%")


# ─── ANALYSIS 2: Lead Time by Supplier ────────────────────────────────────────
def chart_lead_time_by_supplier(df):
    """Which suppliers have the longest lead times?"""
    print("\n[2] Lead Time by Supplier")

    sup_col  = next((c for c in df.columns if 'supplier' in c), None)
    lead_col = next((c for c in df.columns if 'lead' in c), None)

    if not sup_col or not lead_col:
        print(f"  Columns: {list(df.columns)}")
        print("  Could not find required columns — skipping.")
        return

    grp = df.groupby(sup_col)[lead_col].mean().sort_values(ascending=False)
    avg = grp.mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = [RED if v > avg * 1.3 else ORANGE if v > avg else GREEN for v in grp.values]
    ax.barh(grp.index[::-1], grp.values[::-1], color=colors[::-1], edgecolor='white')
    ax.axvline(avg, color=NAVY, linestyle='--', linewidth=1.5, label=f'Average: {avg:.1f} days')
    ax.set_xlabel('Average Lead Time (days)', color=GRAY)
    ax.set_title('Average Lead Time by Supplier')
    ax.legend(fontsize=9)

    for i, val in enumerate(grp.values[::-1]):
        ax.text(val + 0.1, i, f'{val:.1f}d', va='center', fontsize=9, color=NAVY)

    red_patch   = mpatches.Patch(color=RED,    label='>30% above average (critical)')
    orange_patch = mpatches.Patch(color=ORANGE, label='Above average')
    green_patch  = mpatches.Patch(color=GREEN,  label='At or below average')
    ax.legend(handles=[red_patch, orange_patch, green_patch], fontsize=8, loc='lower right')

    save(fig, '2_lead_time_by_supplier.png')
    print(f"  Key finding: '{grp.index[0]}' has the longest avg lead time at {grp.iloc[0]:.1f} days")
    print(f"  Average across all suppliers: {avg:.1f} days")


# ─── ANALYSIS 3: Revenue Leakage — Shipping Cost vs Order Quantity ─────────────
def chart_shipping_cost_analysis(df):
    """Where are the biggest cost leakages in shipping?"""
    print("\n[3] Shipping Cost Analysis")

    ship_col = next((c for c in df.columns if 'shipping' in c and 'cost' in c), None)
    qty_col  = next((c for c in df.columns if 'order' in c and 'quant' in c) or
                    (c for c in df.columns if 'quant' in c), None)
    mode_col = next((c for c in df.columns if 'transport' in c or 'ship' in c and 'mode' in c), None)

    if not ship_col:
        print(f"  Columns: {list(df.columns)}")
        print("  Could not find shipping cost column — skipping.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Chart A: Shipping cost distribution
    ax = axes[0]
    df[ship_col].hist(bins=30, ax=ax, color=BLUE, edgecolor='white', alpha=0.85)
    ax.axvline(df[ship_col].mean(), color=RED, linestyle='--', linewidth=1.5,
               label=f'Mean: ${df[ship_col].mean():,.0f}')
    ax.axvline(df[ship_col].median(), color=ORANGE, linestyle='--', linewidth=1.5,
               label=f'Median: ${df[ship_col].median():,.0f}')
    ax.set_title('Shipping Cost Distribution')
    ax.set_xlabel('Shipping Cost ($)', color=GRAY)
    ax.set_ylabel('Frequency', color=GRAY)
    ax.legend(fontsize=9)

    # Chart B: By transport mode if available
    if mode_col:
        ax = axes[1]
        mode_grp = df.groupby(mode_col)[ship_col].mean().sort_values(ascending=False)
        colors = [NAVY, BLUE, LIGHT, ORANGE][:len(mode_grp)]
        bars = ax.bar(mode_grp.index, mode_grp.values, color=colors, edgecolor='white')
        ax.set_title('Avg Shipping Cost by Transport Mode')
        ax.set_xlabel('')
        ax.set_ylabel('Avg Shipping Cost ($)', color=GRAY)
        for bar, val in zip(bars, mode_grp.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'${val:,.0f}', ha='center', va='bottom', fontsize=9, color=NAVY, fontweight='bold')
    else:
        axes[1].axis('off')

    save(fig, '3_shipping_cost_analysis.png')
    print(f"  Mean shipping cost: ${df[ship_col].mean():,.2f}")
    print(f"  Median shipping cost: ${df[ship_col].median():,.2f}")


# ─── ANALYSIS 4: Revenue by Product Category ──────────────────────────────────
def chart_revenue_by_category(df):
    """Which product categories generate the most revenue?"""
    print("\n[4] Revenue by Product Category")

    cat_col = next((c for c in df.columns if 'product' in c and 'type' in c), None) or \
              next((c for c in df.columns if 'product' in c), None)
    rev_col = next((c for c in df.columns if 'revenue' in c or 'sales' in c or 'price' in c), None)

    if not cat_col or not rev_col:
        print(f"  Columns: {list(df.columns)}")
        print("  Could not find required columns — skipping.")
        return

    grp = df.groupby(cat_col)[rev_col].sum().sort_values(ascending=False)
    total = grp.sum()
    grp_pct = (grp / total * 100).round(1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Bar chart
    colors = [NAVY, BLUE, LIGHT, ORANGE, GREEN][:len(grp)]
    bars = ax1.bar(grp.index, grp.values / 1000, color=colors, edgecolor='white')
    ax1.set_title('Total Revenue by Product Category')
    ax1.set_ylabel('Revenue ($000s)', color=GRAY)
    for bar, val in zip(bars, grp.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                 f'${val/1000:,.0f}K', ha='center', va='bottom', fontsize=9, color=NAVY, fontweight='bold')

    # Pie chart
    wedge_colors = [NAVY, BLUE, LIGHT, ORANGE, GREEN][:len(grp)]
    wedges, texts, autotexts = ax2.pie(
        grp.values, labels=grp.index, autopct='%1.1f%%',
        colors=wedge_colors, startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
    )
    for t in autotexts:
        t.set_fontsize(9)
        t.set_color('white')
        t.set_fontweight('bold')
    ax2.set_title('Revenue Share by Category')

    save(fig, '4_revenue_by_category.png')
    print(f"  Top revenue category: '{grp.index[0]}' ({grp_pct.iloc[0]}% of total)")
    print(f"  Total revenue in dataset: ${total:,.0f}")


# ─── ANALYSIS 5: Supplier Scorecard (Multi-Metric) ────────────────────────────
def chart_supplier_scorecard(df):
    """Composite supplier performance across quality, cost, and speed."""
    print("\n[5] Supplier Performance Scorecard")

    sup_col    = next((c for c in df.columns if 'supplier' in c), None)
    defect_col = next((c for c in df.columns if 'defect' in c), None)
    lead_col   = next((c for c in df.columns if 'lead' in c), None)
    cost_col   = next((c for c in df.columns if 'cost' in c), None)

    if not sup_col:
        print("  Cannot build scorecard without supplier column — skipping.")
        return

    metrics = {}
    if defect_col:
        metrics['Defect Rate (%)'] = df.groupby(sup_col)[defect_col].mean() * 100
    if lead_col:
        metrics['Lead Time (days)'] = df.groupby(sup_col)[lead_col].mean()
    if cost_col:
        metrics['Avg Cost ($)'] = df.groupby(sup_col)[cost_col].mean()

    if len(metrics) < 2:
        print("  Not enough metric columns for scorecard — skipping.")
        return

    scorecard = pd.DataFrame(metrics)

    # Normalize each metric 0-100 (lower is better for all three)
    normalized = scorecard.copy()
    for col in scorecard.columns:
        max_v = scorecard[col].max()
        min_v = scorecard[col].min()
        if max_v > min_v:
            normalized[col] = 100 - (scorecard[col] - min_v) / (max_v - min_v) * 100
        else:
            normalized[col] = 50
    normalized['Composite Score'] = normalized.mean(axis=1)
    normalized = normalized.sort_values('Composite Score', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [GREEN if v >= 60 else ORANGE if v >= 40 else RED for v in normalized['Composite Score']]
    bars = ax.barh(normalized.index[::-1], normalized['Composite Score'][::-1],
                   color=colors[::-1], edgecolor='white')
    ax.set_xlabel('Composite Performance Score (100 = best)', color=GRAY)
    ax.set_title('Supplier Performance Scorecard\n(Normalized: Quality + Speed + Cost)')
    ax.axvline(60, color=GREEN, linestyle=':', linewidth=1, alpha=0.7, label='Good threshold (60)')
    ax.axvline(40, color=RED, linestyle=':', linewidth=1, alpha=0.7, label='Risk threshold (40)')

    for bar, val in zip(bars, normalized['Composite Score'][::-1]):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f'{val:.0f}', va='center', fontsize=9, color=NAVY, fontweight='bold')

    green_p  = mpatches.Patch(color=GREEN,  label='Strong (>60)')
    orange_p = mpatches.Patch(color=ORANGE, label='Moderate (40-60)')
    red_p    = mpatches.Patch(color=RED,    label='At Risk (<40)')
    ax.legend(handles=[green_p, orange_p, red_p], fontsize=8)

    save(fig, '5_supplier_scorecard.png')

    best  = normalized.index[0]
    worst = normalized.index[-1]
    print(f"  Best supplier: {best} (score: {normalized.loc[best,'Composite Score']:.0f}/100)")
    print(f"  Worst supplier: {worst} (score: {normalized.loc[worst,'Composite Score']:.0f}/100)")


# ─── SUMMARY REPORT ───────────────────────────────────────────────────────────
def print_summary(df):
    print(f"\n{'='*60}")
    print("  ANALYSIS SUMMARY — KEY FINDINGS")
    print(f"{'='*60}")
    print(f"  Dataset: {df.shape[0]:,} transactions")
    print(f"  Columns analyzed: {df.shape[1]}")
    print(f"\n  Charts saved to: ./output/")
    print(f"\n  Next steps:")
    print("  1. Review output/ charts")
    print("  2. Add findings to GitHub README")
    print("  3. Select 3-4 best charts for LinkedIn post")
    print(f"{'='*60}\n")


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    df = load_and_clean()

    chart_defect_by_category(df)
    chart_lead_time_by_supplier(df)
    chart_shipping_cost_analysis(df)
    chart_revenue_by_category(df)
    chart_supplier_scorecard(df)

    print_summary(df)
