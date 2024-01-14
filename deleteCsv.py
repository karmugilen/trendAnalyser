import os

def delete_all_csv_files():
    try:
        # Get the current directory
        current_dir = os.getcwd()

        # List all files in the current directory
        all_files = os.listdir(current_dir)

        # Filter out only CSV files
        csv_files = [file for file in all_files if file.lower().endswith('.csv')]

        if not csv_files:
            print("No CSV files found in the current directory.")
            return

        # Delete each CSV file
        for csv_file in csv_files:
            file_path = os.path.join(current_dir, csv_file)
            os.remove(file_path)
            print(f"The file '{csv_file}' has been deleted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to delete all CSV files in the current directory
