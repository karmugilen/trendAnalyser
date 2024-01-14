import os

def delete_file():
    try:
        file_path=r'C:\Users\zesty\Downloads\newchw\combain\combined_output.csv'
        # Delete the file
        os.remove(file_path)
        print(f"File '{file_path}' successfully deleted.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied. Check if you have the necessary permissions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
