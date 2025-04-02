import pandas as pd
import matplotlib.pyplot as plt
import os 

def master_apps_pie(month, year):
    # Load CSV
    df = pd.read_csv(f'./App_Data/Sales-{month} {year} App Data.csv')

    # Normalize the Submission Status values (strip spaces and make consistent casing)
    df['Submission Status'] = df['Submission Status'].str.strip().str.title()

    # Custom grouping of submission statuses
    def group_status(status):
        if status in ['Submitted', 'Declined']:
            return 'Declined/\nUnresponsive'
        if status in ['Contracts', 'Killed']:
            return 'Offers'
        return status  # Keep 'Offers' and 'Funded' as-is

    # Apply grouping
    df['Grouped Status'] = df['Submission Status'].apply(group_status)

    # Count grouped statuses
    status_counts = df['Grouped Status'].value_counts()

    # Define colors for consistent styling
    colors = ['#2196F3', '#FFC107', '#4CAF50']

    # Create the pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        status_counts,
        startangle=140,
        autopct='%1.1f%%',
        pctdistance=1.15,         # Push percentages outside
        labeldistance=1.4,        # Remove default labels inside
        textprops={'fontsize': 12},
        colors=colors
    )

    # Remove text labels (we'll use a legend instead)
    for text in texts:
        text.set_text("")

    # Add a total line at the end
    total_apps = status_counts.sum()

    # Create custom labels with counts
    legend_labels = [f"{status} ({count})" for status, count in status_counts.items()]

    # Use them in the legend
    ax.legend(wedges, legend_labels, title="Submission Status", loc="center left", bbox_to_anchor=(1, 0.5))

    # Main title
    ax.set_title(f'{month} {year} App Analysis', fontsize=16)

    # Add total apps as a smaller subtitle just below the title
    ax.text(0, 1.15, f"Total Applications: {total_apps}", ha="center", fontsize=11, style="italic")

    plt.tight_layout()

    # Create the folder if it doesn't exist
    os.makedirs(f'./Charts/{month} {year}', exist_ok=True)

    # Save individual chart
    fig_path = f"./Charts/{month} {year}/master_submission_pie.png"
    fig.savefig(fig_path)
    plt.close(fig)
    print(f"Saved {month} {year} master pie chart to Charts/{month} {year}/master_submission_pie.png")
