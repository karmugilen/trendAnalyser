from pytrends.request import TrendReq
from datetime import datetime
import pytz
import time

def get_google_trends_data_batch(company_name, timeframe='now 7-d', geo='US'):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([company_name], timeframe=timeframe, geo=geo)
    interest_over_time_df = pytrends.interest_over_time()
    interest_over_time_df.index = interest_over_time_df.index.tz_localize('UTC').tz_convert('Asia/Kolkata')
    return interest_over_time_df

def companesloop_with_retry(company_name, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            # Fetch Google Trends data for the specified company
            data_company_7_days_india = get_google_trends_data_batch(company_name)

            # Specify the CSV file path dynamically
            csv_file_path = f'{company_name.lower().replace(" ", "_")}.csv'

            # Write to CSV in the specified format
            with open(csv_file_path, 'w', newline='') as csv_file:
                csv_file.write("Time,{}\n".format(company_name))
                for index, row in data_company_7_days_india.iterrows():
                    formatted_time = row.name.strftime("%Y-%m-%dT%H")
                    csv_file.write(f"{formatted_time},{row[company_name]}\n")

            print(f"{company_name} data written to {csv_file_path}")
            break  # Break out of the loop if successful

        except Exception as e:
            print(f"Error processing data for {company_name} (Attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                print("Retrying...")
                time.sleep(0)  # Wait for 5 seconds before retrying
            else:
                print(f"Maximum retries reached for {company_name}. Skipping.")

def stockDownloadUS():
    names = [
            "Amd",
            "Apple",
            "Microsoft",
            "Amazon",
            "Alphabet (Google)",
            "Facebook",
            "Tesla",
            "Johnson & Johnson",
            "Visa",
            "Procter & Gamble",
            "JPMorgan Chase",
            "Mastercard",
            "UnitedHealth Group",
            "Goldman Sachs",
            "Home Depot",
            "Verizon",
            "Coca-Cola",
            "Intel",
            "Walmart",
            "Cisco",
            "IBM",
            "Pfizer",
            "Walt Disney",
            "Boeing",
            "Exxon Mobil",
            "Chevron",
            "Caterpillar",
            "3M",
            "Walt Disney",
            "Adobe",
            "Salesforce",
            "Netflix",
            "Oracle",
            "Intel",
            "Coca-Cola",
            "PepsiCo",
            "General Electric",
            "General Motors",
            "Ford",
            "Bank of America",
            "Goldman Sachs",
            "Morgan Stanley",
            "American Express",
            "AT&T",
            "Comcast",
            "Wells Fargo",
            "Boeing",
            "Coca-Cola",
            "Walt Disney",
            "McDonald's",
            "NVIDIA",
            "Visa",
        ]

    # Use a simple loop to fetch data for each company
    for company_name in names:
        companesloop_with_retry(company_name)

# This code will run when the module is imported
