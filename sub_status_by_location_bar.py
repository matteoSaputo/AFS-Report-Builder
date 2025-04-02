import pandas as pd
import matplotlib.pyplot as plt
import os

def apps_by_location_bar(month, year):
    # Load CSV
    apps = pd.read_csv(f'./App_Data/Sales-{month} {year} App Data.csv')

    # Clean and normalize 'Submission Status' and 'Location' columns
    apps['Submission Status'] = apps['Submission Status'].str.strip().str.title()
    apps['Location (from Rep)'] = apps['Location (from Rep)'].str.strip().str.upper()

    # Grouping logic for submission status
    def group_status(status):
        if status in ['Submitted', 'Declined']:
            return 'Declined/\nUnresponsive'
        elif status in ['Contracts', 'Killed']:
            return 'Offers'
        else:
            return status

    apps['Grouped Status'] = apps['Submission Status'].apply(group_status)

    # Filter by location
    locations = ['RXR', 'MADRID', 'NYC', 'KOSOVO']
    apps = apps[apps['Location (from Rep)'].isin(locations)]

    # Pivot table, location y-axis, status x-axis
    pivot = apps.pivot_table(index='Location (from Rep)', columns='Grouped Status', aggfunc='size')

    # Ensure all expexted statuses are included
    status_order = ['Declined/\nUnresponsive', 'Offers', 'Funded']
    for status in status_order:
        if status not in pivot.columns:
            pivot[status] = 0
    pivot = pivot[status_order]

    # Totals per status
    status_totals = apps['Grouped Status'].value_counts()
    legend_labels = [f"{status} ({status_totals.get(status, 0)})" for status in status_order]

    # Plot stacked bar graph
    colors = ['#FFC107', '#2196F3', '#4CAF50']
    fig, graph = plt.subplots(figsize=(10, 6))
    pivot.plot(kind='bar', stacked=True, ax=graph, color=colors)


    # Add totals to the top of each bar
    bar_totals = pivot.sum(axis=1)
    for i, total in enumerate(bar_totals):
        graph.text(i, total+1, str(total), ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Add totals to each stack for each bar
    for bar_index, location in enumerate(pivot.index):
        y_offset = 0
        for status_index, status in enumerate(status_order):
            value = pivot.loc[location, status]
            if value == 0: continue
            y_offset += value/2 # Position text in middle of segment
            graph.text(
                bar_index,
                y_offset,
                f"{value}", 
                ha='center',
                va='center',
                fontsize=9,
            )
            y_offset += value/2

    plt.title(f"{month} {year}  App Analysis", fontsize = 15)
    plt.xlabel("Location")
    plt.ylabel("Number of Full Applications")
    plt.legend(title="Submission Status", labels=legend_labels)
    plt.xticks(rotation=0)
    plt.tight_layout()
    # plt.show()

    # Create the folder if it doesn't exist
    os.makedirs(f'./Charts/{month} {year}', exist_ok=True)

    # Save individual chart
    fig_path = f"./Charts/{month} {year}/office_breakdown_bar_graph.png"
    fig.savefig(fig_path)

    print(f"Saved {month} {year} office breakdown bar graph to Charts/{month} {year}/office_breakdown_bar_graph.png")