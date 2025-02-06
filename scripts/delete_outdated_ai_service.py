import os
import time
import argparse

def delete_outdated_files(directory, days):
    """
    Deletes files in the specified directory that haven't been modified in the last 'days' days.

    Args:
        directory (str): The path to the directory to clean.
        days (int): The number of days after which a file is considered outdated.
    """
    seconds = time.time() - (days * 24 * 60 * 60)
    deleted_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getmtime(file_path) < seconds:
                try:
                    os.remove(file_path)
                    deleted_files.append(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
    return deleted_files

def main():
    """
    Main function to parse arguments and call the delete_outdated_files function.
    """
    parser = argparse.ArgumentParser(description="Deletes outdated files in a directory.")
    parser.add_argument("directory", help="The directory to clean.")
    parser.add_argument("days", type=int, help="Number of days after which a file is considered outdated.")

    args = parser.parse_args()

    deleted_files = delete_outdated_files(args.directory, args.days)

    if deleted_files:
        print(f"\nSuccessfully deleted {len(deleted_files)} outdated files.")
    else:
        print("No outdated files found.")

if __name__ == "__main__":
    main()
