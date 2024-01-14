import csv
from collections import defaultdict
from datetime import datetime
import sys
from datetime import datetime

def outputFiles():
    # Get the current date and time
    current_date_time = datetime.now()

    # Format the date as a string
    formatted_date = current_date_time.strftime("%Y-%m-%d-%H-%M-%S")

    # Dictionary to store data for each hour for each company
    company_hour_data = defaultdict(lambda: defaultdict(list))
    skipped_dates = set()

    # Read the CSV file for overall average data
    with open("combined_output.csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)  # Read the header row

        # Get the indices for Time and all company names
        time_index = header.index('Time')
        company_indices = {header[i]: i for i in range(len(header)) if i != time_index}

        for row in reader:
            if len(row) >= max(time_index, *company_indices.values()) + 1:
                time = row[time_index]

                # Parse timestamp to get the day of the week
                timestamp = datetime.fromisoformat(time)
                day_of_week = timestamp.weekday()

                # Skip Saturdays (5) and Sundays (6) for overall average data
                if day_of_week in {5, 6}:
                    skipped_dates.add(timestamp.date())
                    continue

                for company, index in company_indices.items():
                    value = int(row[index])

                    # Extract the hour from the timestamp and format it
                    hour = timestamp.strftime("%I %p")

                    # Store data for each hour and each company
                    company_hour_data[f"{index + 1}. {company}"][hour].append(value)

    # Read the CSV file for the latest date data (without skipping Saturdays and Sundays)
    latest_date_data = defaultdict(lambda: defaultdict(int))
    with open("combined_output.csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)  # Read the header row

        # Get the indices for Time and all company names
        time_index = header.index('Time')
        company_indices = {header[i]: i for i in range(len(header)) if i != time_index}

        for row in reader:
            if len(row) >= max(time_index, *company_indices.values()) + 1:
                time = row[time_index]

                for company, index in company_indices.items():
                    value = int(row[index])

                    # Extract the hour from the timestamp and format it
                    timestamp = datetime.fromisoformat(time)
                    hour = timestamp.strftime("%I %p")

                    # Store the latest data for each hour and each company
                    latest_date_data[f"{index + 1}. {company}"][hour] = value
    # Calculate the overall average for each hour for each company, skipping Saturdays and Sundays
    overall_average_data = {}
    for company, hour_data in company_hour_data.items():
        company_average_data = {}
        for hour, values in sorted(hour_data.items(), key=lambda x: datetime.strptime(x[0], "%I %p").strftime("%H")):
            average_value = sum(values) / len(values) if len(values) > 0 else 0
            company_average_data[hour] = average_value
        overall_average_data[company] = company_average_data

    # Set a threshold for comparison (adjust as needed)
    threshold = 1

    # Specify the output file name
    output_file = "output"+str(formatted_date)+".txt"

    # ...

    # Open the output file in write mode
    # ...

    # ...

    # Open the output file in write mode
    # ...

    # Open the output file in write mode
    with open(output_file, 'w') as output:
        # Redirect the standard output to the file
        original_stdout = sys.stdout
        sys.stdout = output

        # Get the date of the latest data
        latest_date = max(skipped_dates)

        # Write a header with general information
        print(f"Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Latest Data Date: {latest_date}")
        print(f"Excluded Dates (Saturdays and Sundays): {', '.join(str(date) for date in sorted(skipped_dates))}")
        print("\n" + "=" * 80 + "\n")

        # Compare latest date data with overall average for each company
        rankings_crossings = []
        rankings_percent_difference = []

        for company in overall_average_data.keys():
            total_difference = 0
            total_percent_difference = 0
            total_crossings = 0
            print(f"\nCompany: {company}")
            print(f"{'Hour': <8} {'Latest': <8} {'Average': <8} {'Difference': <12} {'% Difference': <15}")
            print("-" * 80)

            for hour in sorted(overall_average_data[company].keys(), key=lambda x: datetime.strptime(x, "%I %p").strftime("%H")):
                average_value = overall_average_data[company][hour]
                latest_value = latest_date_data[company][hour]
                difference = latest_value - average_value
                percent_difference = (difference / average_value) * 100 if average_value != 0 else 0

                if latest_value > threshold * average_value:
                    print(f"{hour: <8} {latest_value: <8} {average_value: <8} {difference: <12} {percent_difference:.2f}%")
                    total_difference += difference
                    total_percent_difference += percent_difference
                    total_crossings += 1

            rankings_crossings.append((company, total_crossings))
            rankings_percent_difference.append((company, total_percent_difference))

            print("-" * 80)
            print(f"Total Crossings for {company}: {total_crossings}")
            print(f"Total Difference: {total_difference}  Total % Difference: {total_percent_difference:.2f}%\n")

        # Rank companies based on Total Crossings
        print("\nRankings based on Total Crossings:")
        for rank, (company, total_crossings) in enumerate(sorted(rankings_crossings, key=lambda x: x[1], reverse=True), 1):
            print(f"{rank}. {company}: {total_crossings}")

        # Rank companies based on Total % Difference
        print("\nRankings based on Total % Difference:")
        for rank, (company, total_percent_difference) in enumerate(sorted(rankings_percent_difference, key=lambda x: x[1], reverse=True), 1):
            print(f"{rank}. {company}: {total_percent_difference:.2f}%")

        # Calculate combined rankings based on both Total Crossings and Total % Difference
        combined_rankings = []
        for company in overall_average_data.keys():
            total_crossings_rank = next(rank for rank, (comp, _) in enumerate(sorted(rankings_crossings, key=lambda x: x[1], reverse=True), 1) if comp == company)
            total_percent_difference_rank = next(rank for rank, (comp, _) in enumerate(sorted(rankings_percent_difference, key=lambda x: x[1], reverse=True), 1) if comp == company)
            combined_rank = total_crossings_rank + total_percent_difference_rank
            combined_rankings.append((company, total_crossings, total_percent_difference, combined_rank))

        # Rank companies based on the combined ranking
        sorted_combined_rankings = sorted(combined_rankings, key=lambda x: x[3])

        print("\nRankings based on Combined Ranking (Total Crossings + Total Difference):")
        for rank, (company, total_crossings, total_percent_difference, combined_rank) in enumerate(sorted_combined_rankings, 1):
            print(f"{rank}. {company}: Total Crossings={total_crossings}, Total Difference={total_percent_difference}, Combined Rank={combined_rank}")
        # Reset the standard output to the console
        sys.stdout = original_stdout

    # Inform the user about the successful write
    print(f"Output data has been written to {output_file}")

