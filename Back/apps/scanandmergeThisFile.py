import os

def concatenate_files(search_folder, target_filename, output_filename):
    """
    Recursively searches for files with the name `target_filename` in `search_folder`
    and writes their contents to `output_filename`.
    """
    # Open the output file in write mode (overwrites any existing file)
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        # Walk through the directory tree
        for root, dirs, files in os.walk(search_folder):
            if target_filename in files:
                filepath = os.path.join(root, target_filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        # Write a header for clarity
                        outfile.write(f"# Contents of: {filepath}\n")
                        outfile.write(infile.read())
                        outfile.write("\n\n")  # Extra spacing between files
                    print(f"Added: {filepath}")
                except Exception as e:
                    print(f"Failed to read {filepath}: {e}")

if __name__ == "__main__":
    # Prompt the user for required inputs
    folder = input("Enter the folder location to search: ").strip()
    target_file = input("Enter the file name to search for (e.g., models.py): ").strip()
    output_file = input("Enter the output file name (e.g., concatenated_models.txt): ").strip()

    # Check if the provided folder exists and is a directory
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a valid directory.")
    else:
        concatenate_files(folder, target_file, output_file)
        print(f"\nConcatenation complete. Output written to '{output_file}'.")
