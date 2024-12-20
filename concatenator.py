import os
from pathlib import Path
import argparse

def concatenate_code(directory, output_file, extensions=None, exclude_dirs=None):
    """
    Concatenate all code files in a directory into a single file.
    
    Args:
        directory (str): Root directory to start searching from
        output_file (str): Path to output file
        extensions (list): List of file extensions to include (e.g. ['.py', '.js'])
        exclude_dirs (list): List of directory names to exclude (e.g. ['node_modules', 'venv'])
    """
    if extensions is None:
        extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp']
    
    if exclude_dirs is None:
        exclude_dirs = ['node_modules', 'venv', '.git', '__pycache__', 'build', 'dist']

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(directory):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(directory)
                    
                    outfile.write(f"\n{'='*80}\n")
                    outfile.write(f"File: {rel_path}\n")
                    outfile.write(f"{'='*80}\n\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"Error reading file: {e}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Concatenate code files in a project')
    parser.add_argument('directory', help='Root directory of the project')
    parser.add_argument('--output', default='concatenated_code.txt', help='Output file path')
    parser.add_argument('--extensions', nargs='+', help='File extensions to include (e.g. .py .js)')
    parser.add_argument('--exclude-dirs', nargs='+', help='Directories to exclude')
    
    args = parser.parse_args()
    
    concatenate_code(
        args.directory,
        args.output,
        extensions=args.extensions,
        exclude_dirs=args.exclude_dirs
    )