import pandas as pd
import matplotlib.pyplot as plt
import os

def apps_by_location_pie(month, year):
    # Load CSV
    df = pd.read_csv(f'./App_Data/Sales-{month} {year} App Data.csv')

    # Clean and normalize 'Submission Status' and 'Location' columns
    df['Submission Status'] = df['Submission Status'].str.strip().str.title()
    df['Location (from Rep)'] = df['Location (from Rep)'].str.strip().str.upper()

    # Grouping logic for submission status
    def group_status(status):
        if status in ['Submitted', 'Declined']:
            return 'Declined/\nUnresponsive'
        elif status in ['Contracts', 'Killed']:
            return 'Offers'
        else:
            return status

    df['Grouped Status'] = df['Submission Status'].apply(group_status)

    # Define target locations (standardized to match cleaned values)
    target_locations = ['RXR', 'MADRID', 'NYC', 'KOSOVO']

    # Define colors for consistent styling
    colors = ['#2196F3', '#FFC107', '#4CAF50']

    # Set up 2x2 grid
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()  # Flatten to easily index into

    for i, location in enumerate(target_locations):
        loc_df = df[df['Location (from Rep)'] == location]
        
        if loc_df.empty:
            axes[i].set_title(f"{location} - No Data")
            axes[i].axis('off')  # Hide empty plot
            continue

        status_counts = loc_df['Grouped Status'].value_counts()

        wedges, texts, autotexts = axes[i].pie(
            status_counts,
            startangle=140,
            autopct='%1.1f%%',
            pctdistance=1.15,
            labeldistance=1.4,
            textprops={'fontsize': 10},
            colors=colors[:len(status_counts)]
        )

        for text in texts:
            text.set_text("")  # Remove inside labels

        # Total count
        total = status_counts.sum()

        # Main title and subtitle
        axes[i].set_title(f"{location} - {month} {year} Submission Breakdown", fontsize=13)
        axes[i].text(0, 1.1, f"Total Applications: {total}", ha='center', fontsize=9, style='italic')

        # Legend with per-status counts
        legend_labels = [f"{status} ({count})" for status, count in status_counts.items()]
        axes[i].legend(
            wedges,
            legend_labels,
            title="Submission Status",
            loc="center left",
            bbox_to_anchor=(1, 0.5)
        )
    plt.tight_layout()

    # Create the folder if it doesn't exist
    os.makedirs(f'./Charts/{month} {year}', exist_ok=True)

    # Save individual chart
    fig_path = f"./Charts/{month} {year}/office_breakdown_pie_chart.png"
    fig.savefig(fig_path)
    plt.close(fig)
    print(f"Saved {month} {year} office breakdown pie chart to Charts/{month} {year}/office_breakdown_pie_chart.png")