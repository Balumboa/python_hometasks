import os
import argparse
import re
from pathlib import Path

def parse_gitignore(gitignore_path):
    patterns = []
    with open(gitignore_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            patterns.append(line)
    return patterns

def is_ignored(file_path, project_dir, patterns):
    relative_path = os.path.relpath(file_path, project_dir)
    for pattern in patterns:
        if pattern.startswith('*'):
            regex = re.compile(pattern.replace('.', r'\.').replace('*', '.*'))
            if regex.search(relative_path):
                return pattern
        else:
            if relative_path == pattern:
                return pattern
            if pattern.endswith('/') and relative_path.startswith(pattern):
                return pattern
    return None

def find_ignored_files(project_dir):
    gitignore_path = os.path.join(project_dir, '.gitignore')
    if not os.path.exists(gitignore_path):
        return []
    
    patterns = parse_gitignore(gitignore_path)
    ignored_files = []
    
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if '.git' in file_path.split(os.sep):
                continue
            ignore_pattern = is_ignored(file_path, project_dir, patterns)
            if ignore_pattern is not None:
                ignored_files.append((file_path, ignore_pattern))
    
    return ignored_files

def main():
    parser = argparse.ArgumentParser(description='Check which files are ignored by .gitignore')
    parser.add_argument('--project_dir', required=True, help='Path to the project directory')
    args = parser.parse_args()
    
    project_dir = os.path.abspath(args.project_dir)
    if not os.path.exists(project_dir):
        print(f"Error: Directory '{project_dir}' does not exist")
        return
    
    ignored_files = find_ignored_files(project_dir)
    
    print("Ignored files:")
    for file_path, pattern in ignored_files:
        print(f"{file_path} ignored by expression {pattern}")

if __name__ == '__main__':
    main()