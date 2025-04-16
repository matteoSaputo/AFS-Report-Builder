import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os

def data_sources_pie_chart(month, year):
    # Load data
    apps = pd.read_csv(f'./App_Data/Sales-{month} {year} App Data.csv')

    # Filter out missing or empty sources
    apps = apps[apps['Data Source'].notna() & (apps['Data Source'].str.strip() != '')]

    # Count all data sources
    source_counts = apps['Data Source'].value_counts()
    total = source_counts.sum()

    # Convert counts to percentage
    source_percent = source_counts / total * 100

    # Identify large contributors (≥ threshold)
    mask = source_percent >= 3
    top_sources = source_counts[mask]

    # Lump all others into "Other"
    others_total = source_counts[~mask].sum()
    if others_total > 0:
        top_sources = pd.concat([top_sources, pd.Series({'Other': others_total})])

    # Prepare colors
    cmap = cm.get_cmap('tab20')
    colors = [cmap(i) for i in range(len(top_sources))]
    if 'Other' in top_sources.index:
        other_index = list(top_sources.index).index('Other')
        colors[other_index] = '#9E9E9E'

    # Plot pie chart with source names inside slices
    fig, ax = plt.subplots(figsize=(12, 8))
    wedges, texts = ax.pie(
        top_sources,
        labels=top_sources.index, 
        startangle=140,
        textprops={'fontsize': 9},
        colors=colors
    )

    # Custom legend with counts and percentages
    legend_labels = [
        f"{label} ({count} apps, {count / total:.1%})"
        for label, count in top_sources.items()
    ]
    ax.legend(
        wedges,
        legend_labels,
        title="Data Source",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=9
    )

    plt.title(f"Data Source Breakdown – {month} {year}", fontsize=14)
    plt.tight_layout()

    # Save
    os.makedirs(f'./Charts/{month} {year}', exist_ok=True)
    fig_path = f"./Charts/{month} {year}/data_sources_pie_chart.png"
    plt.savefig(fig_path)
    plt.close()

    print(f"✅ Saved {month} {year} data sources pie chart to: {fig_path}")