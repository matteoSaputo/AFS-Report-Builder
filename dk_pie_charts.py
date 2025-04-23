import pandas as pd
import matplotlib.pyplot as plt
import os

def dk_submission_pie_charts(month, year):
    # Load data
    df = pd.read_csv(f'./App_Data/Sales-{month} {year} App Data.csv')
    
    # Clean up submission status for grouping
    df['Submission Status'] = df['Submission Status'].str.strip().str.title()

    # Optional: group statuses into simplified categories
    def group_status(status):
        if status in ['Submitted', 'Declined']:
            return 'No Offers'
        elif status in ['Contracts', 'Killed']:
            return 'Offers'
        else:
            return status

    df['Grouped Status'] = df['Submission Status'].apply(group_status)

    # Filter for DK24–DK31
    dk_mask = df['Data Source'].str.contains(r'DK(?:2[4-9]|3[0-1])', case=False, na=False)
    dk_sources = df[dk_mask]['Data Source'].unique()

    for dk in dk_sources:
        subset = df[df['Data Source'] == dk]
        if subset.empty:
            continue

        counts = subset['Grouped Status'].value_counts()
        total = counts.sum()

        # Colors for statuses (customize if needed)
        colors = ['#2196F3', '#FFC107', '#4CAF50', '#8a2d2d']

        fig, ax = plt.subplots(figsize=(6, 6))
        # Pie chart with percentages outside, labels removed (we'll use a legend)
        wedges, texts, autotexts = ax.pie(
            counts,
            labels=None,
            autopct=lambda pct: f"{pct:.1f}%\n({int(pct * total / 100)})",
            startangle=140,
            pctdistance=1.15,
            labeldistance=1.4,
            textprops={'fontsize': 9},
            colors=colors[:len(counts)]
        )

        # Add legend for statuses
        ax.legend(
            wedges,
            counts.index,
            title="Status",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=8
        )

        # Main title
        ax.set_title(f"{dk} ({month} {year})– Submission Breakdown", fontsize=12)

        # Subtitle: total applications
        fig.text(0.5, 0.95, f"Total Applications: {total}", ha='center', fontsize=9, style='italic')

        plt.tight_layout()

        # Create the folder if it doesn't exist
        os.makedirs(f'./Charts/By Month/{month} {year}', exist_ok=True)
        os.makedirs(f'./Charts/By Chart/{dk} submission_pie', exist_ok=True)
        os.makedirs(f'./Charts/By Chart/DK_submission_pie', exist_ok=True)

        # Save
        fig_path = f"./Charts/By Month/{month} {year}/{month} {year} {dk} submission_pie.png"
        fig.savefig(fig_path)
        fig_path = f"./Charts/By Chart/{dk} submission_pie/{month} {year} {dk} submission_pie.png"
        fig.savefig(fig_path)
        fig_path = f"./Charts/By Chart/DK_submission_pie/{month} {year} {dk} submission_pie.png"
        fig.savefig(fig_path)
        plt.close(fig)  # closes the figure to prevent memory build-up    
        print(f"Saved {month} {year} {dk} pie chart")
