import pandas as pd
import matplotlib.pyplot as plt
import re
import os

def offers_breakdown(month, year):
    # Load data
    apps = pd.read_csv(f'./App_Data/Sales-{month} {year} App Data.csv')

    # Define function to extract array of numeric amounts of all offers for an app
    def extract_offer_amounts(offers_str):
        if pd.isna(offers_str):
            return []
        
        offer_lines = re.split(r'\n|;', offers_str)
        amounts = []
        for line in offer_lines:
            match = re.search(r'\$?\s*([\d\,\.]+)\s*[kK]?', line)
            if match:
                raw = match.group(1).replace(',', '').strip()
                if raw == "":
                    continue
                try:
                    value = float(raw)
                    if value < 1000: value *= 1000
                    amounts.append(value)
                except ValueError:
                    continue
        return amounts

    # Extract offer amounts and comute average offer per app
    apps['Offer Amounts'] = apps['Offers'].apply(extract_offer_amounts)
    apps['Average Offer'] = apps['Offer Amounts'].apply(lambda x: sum(x)/len(x) if x else 0)

    # Filter out apps with no offers
    apps = apps[apps['Offers'].notna() & (apps['Offers'].str.strip() != '')]

    #Define ranges for grouping
    bins = [0, 10000, 20000, 30000, 40000, float('inf')]
    labels = ['0-10k', '10k-20k', '20k-30k', '30k-40k', '40k+']

    # apply bins
    apps['Offer Range'] = pd.cut(apps['Average Offer'], bins=bins, labels=labels, right=False)

    # Count apps in each range
    range_counts = apps['Offer Range'].value_counts().sort_index()

    # Prepare labels: "24 apps (18.2%)"
    total = range_counts.sum()
    pie_labels = [f"{count} apps ({count/total:.1%})" for count in range_counts]

    # Plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw pie chart
    wedges, texts = ax.pie(
        range_counts,
        labels=pie_labels,
        startangle=140,
        textprops={'fontsize': 11}
    )

    # Add legend on the right, outside the chart
    ax.legend(
        wedges,
        labels,
        title="Average Offer Size",
        bbox_to_anchor=(1.05, 0.5),
        borderaxespad=0.
    )

    # Title and better spacing
    plt.title(f"{month} {year} Average Offer Amounts", fontsize=14)
    plt.text(0, 1.2, f"Total Offers: {total}", ha='center', fontsize=9, style='italic')

    plt.subplots_adjust(left=0.1, right=0.75)  # Leave room for legend
    # plt.show()

    # Create the folder if it doesn't exist
    os.makedirs(f'./Charts/{month} {year}', exist_ok=True)

    # Save individual chart
    fig_path = f"./Charts/{month} {year}/offers_pie_chart.png"
    fig.savefig(fig_path)
    plt.close(fig)  # closes the figure to prevent memory build-up


    print(f"Saved {month} {year} offers pie chart to Charts/{month} {year}/offers_pie_chart.png")