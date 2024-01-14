import pandas as pd
def mergeFile():
    # Read CSV files
    csv1 = pd.read_csv(r"C:\Users\zesty\Downloads\newchw\combain\combined_output.csv")
    csv2 = pd.read_csv(r"C:\Users\zesty\Downloads\newchw\combain\your_file1.csv")

    # Concatenate the two DataFrames
    combined_csv = pd.concat([csv1, csv2], ignore_index=True)

    # Remove duplicate rows based on 'Time'
    combined_csv = combined_csv.drop_duplicates(subset='Time', keep='first')

    # Write the combined DataFrame to a new CSV file
    combined_csv.to_csv(r'C:\Users\zesty\Downloads\newchw\combain\your_file1.csv', index=False)
