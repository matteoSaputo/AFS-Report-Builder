import pandas as pd
import matplotlib.pyplot as plt
import re
import os

def offers_breakdown_by_location(month, year):
    # Load data
    apps = pd.read_csv(f'./App_Data/Sales-{month} {year} App Data.csv')

    # Filter out apps with no offers
    apps = apps[apps['Offers'].notna() & (apps['Offers'].str.strip() != '')]

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
    apps = apps[apps['Average Offer'] > 0]

    # Define ranges for grouping
    bins = [0, 10000, 20000, 30000, 40000, float('inf')]
    labels = ['0-10k', '10k-20k', '20k-30k', '30k-40k', '40k+']

    # Standardize location values
    apps['Location (from Rep)'] = apps['Location (from Rep)'].str.strip().str.upper()

    # Define target locations to loop through
    locations = ['RXR', 'MADRID', 'NYC', 'KOSOVO']

    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    # apply bins
    apps['Offer Range'] = pd.cut(
        apps['Average Offer'],
        bins=bins,
        labels=labels,
        right=False,
    )

    for i, location in enumerate(locations):
        # Filter by location
        loc_apps = apps[apps['Location (from Rep)'] == location]

        # Skip if theres no apps from current location
        if loc_apps.empty:
            axes[i].set_title(f"{location} - No Data")
            axes[i].axis('off')
            continue

        # Count apps in each range
        range_counts = loc_apps['Offer Range'].value_counts().sort_index()

        # Prepare labels
        total = range_counts.sum()
        pie_labels = [f"{count}" for count in range_counts]

        # Draw pie chart
        wedges, texts = axes[i].pie(
            range_counts,
            labels=pie_labels,
            startangle=140,
            textprops={'fontsize': 10}
        )

        # Add legend and title
        axes[i].set_title(f"{location} - {month} {year} Offers", fontsize=13)
        axes[i].text(0, 1.2, f"Total Offers: {total}", ha='center', fontsize=9, style='italic')

        # Add legend on the right, outside the chart
        axes[i].legend(
            wedges,
            labels,
            title="Average Offer Size",
            loc="center left",
            bbox_to_anchor=(1.05, 0.5),
            borderaxespad=0.
        )
    plt.tight_layout()

    # Create the folder if it doesn't exist
    os.makedirs(f'./Charts/{month} {year}', exist_ok=True)

    # Save individual chart
    fig_path = f"./Charts/{month} {year}/offers_pie_chart_by_location.png"
    fig.savefig(fig_path)
    plt.close(fig)  # closes the figure to prevent memory build-up

    print(f"Saved {month} {year} offers pie chart by locatiuon to Charts/{month} {year}/offers_pie_chart_by_location.png")

offers_breakdown_by_location("February", "2025")