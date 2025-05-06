import os

def merge_py_files(directory, output_file='merged.txt'):
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for root, dirs, files in os.walk(directory):
            # Exclude __pycache__ and migrations directories
            dirs[:] = [d for d in dirs if d not in ('__pycache__', 'migrations')]
            for file in files:
                # Process only .py files, excluding __init__.py and test files.
                if file.endswith('.py') and file != '__init__.py' and not (file.lower().startswith("test") or file.lower().endswith("_test.py")):
                    file_path = os.path.join(root, file)
                    # Write a header indicating the source file.
                    out_f.write(f"\n# --- Contents of: {file_path} ---\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as in_f:
                            out_f.write(in_f.read())
                    except Exception as e:
                        out_f.write(f"# Error reading {file_path}: {e}\n")
                    out_f.write("\n" + "="*80 + "\n")

if __name__ == '__main__':
    path = input("Enter the path to search for .py files: ").strip()
    if os.path.isdir(path):
        merge_py_files(path)
        print("Merging complete. The output is saved in 'merged.txt'.")
    else:
        print("The provided path is not a valid directory.")
