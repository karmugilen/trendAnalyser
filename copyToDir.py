import shutil

def copy_file():
    src_path = r'C:\Users\zesty\Downloads\newchw\combined_output.csv'
    dest_dir = r'C:\Users\zesty\Downloads\newchw\combain'

    try:
        # Copy the file from source path to destination directory
        shutil.copy(src_path, dest_dir)
        print(f"File '{src_path}' successfully copied to '{dest_dir}'.")
    except FileNotFoundError:
        print(f"Error: File '{src_path}' not found.")
    except IsADirectoryError:
        print(f"Error: '{dest_dir}' is a directory. Please provide the full destination file path.")
    except PermissionError:
        print(f"Error: Permission denied. Check if you have the necessary permissions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage

