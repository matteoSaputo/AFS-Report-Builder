from sub_status_pie_chart import master_apps_pie
from sub_status_by_location import apps_by_location_pie
from sub_status_by_location_bar import apps_by_location_bar
from offers_breakdown import offers_breakdown
from offers_breakdown_by_location import offers_breakdown_by_location
from data_sources_pie_chart import data_sources_pie_chart
from data_sources_bar_graph import data_sources_bar_chart
from dk_pie_charts import dk_submission_pie_charts

def main():
    # List of (month, year) tuples
    date_ranges = [
        ("All", "Time"),
        ("March", "2025"),
        ("February", "2025"),
        ("January", "2025"),
        ("December", "2024"),
        ("November", "2024"),
        ("October", "2024"),
        ("September", "2024"),
        ("August", "2024"),
        ("Funded-All", "Time"),
        ("Funded-March", "2025"),
        ("Funded-February", "2025"),
        ("Funded-January", "2025"),
        ("Funded-December", "2024"),
        ("Funded-November", "2024"),
        ("Funded-October", "2024"),
        ("Funded-September", "2024"),
        ("Funded-August", "2024")
    ]

    for month, year in date_ranges:
        dk_submission_pie_charts(month, year)
        if "Funded" not in month:
            master_apps_pie(month, year)
            apps_by_location_pie(month, year)
        apps_by_location_bar(month, year)
        offers_breakdown(month, year)
        offers_breakdown_by_location(month, year)
        data_sources_pie_chart(month, year)
        data_sources_bar_chart(month, year)

if __name__ == "__main__":
    main()
