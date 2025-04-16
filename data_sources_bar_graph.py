import pandas as pd
import matplotlib.pyplot as plt
import os

def data_sources_bar_chart(month, year):
    # Load data
    apps = pd.read_csv(f'./App_Data/Sales-{month} {year} App Data.csv')

    # Filter out missing or empty sources
    apps = apps[apps['Data Source'].notna() & (apps['Data Source'].str.strip() != '')]

    # Count and calculate %
    source_counts = apps['Data Source'].value_counts()
    total = source_counts.sum()
    source_percent = source_counts / total * 100

    # Separate sources above the threshold
    filtered_sources = source_counts[source_percent >= 2]

    # Group the rest as "Other"
    other_total = source_counts[source_percent < 2].sum()
    if other_total > 0:
        filtered_sources = pd.concat([filtered_sources, pd.Series({'Other': other_total})])

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(filtered_sources.index, filtered_sources.values, color='#2196F3')

    # Add count and percentage labels on top of bars
    for bar in bars:
        height = bar.get_height()
        pct = (height / total) * 100
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{int(height)} apps\n{pct:.1f}%",
            ha='center',
            va='bottom',
            fontsize=8
        )


    # Style
    ax.set_title(f"Data Sources by App Volume – {month} {year}", fontsize=14)
    ax.set_ylabel("Number of Applications")
    ax.set_xlabel("Data Source")
    ax.set_xticks(range(len(filtered_sources)))
    ax.set_xticklabels(filtered_sources.index, rotation=45, ha='right', fontsize=9)
    plt.tight_layout()

    # Create save directory if needed
    os.makedirs(f'./Charts/{month} {year}', exist_ok=True)

    # Save
    fig_path = f"./Charts/{month} {year}/data_sources_bar_chart.png"
    plt.savefig(fig_path)
    plt.close()

    print(f"Saved {month} {year} data sources bar chart to: {fig_path}")
