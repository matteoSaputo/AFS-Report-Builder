from sub_status_pie_chart import master_apps_pie
from sub_status_by_location import apps_by_location_pie
from sub_status_by_location_bar import apps_by_location_bar
from offers_breakdown import offers_breakdown

def main():
    # List of (month, year) tuples
    date_ranges = [
        ("March", "2025"),
        ("February", "2025"),
        ("January", "2025"),
        ("December", "2024"),
        ("November", "2024"),
        ("October", "2024"),
        ("September", "2024"),
        ("August", "2024")
    ]

    for month, year in date_ranges:
        master_apps_pie(month, year)
        apps_by_location_pie(month, year)
        apps_by_location_bar(month, year)
        offers_breakdown(month, year)

if __name__ == "__main__":
    main()
