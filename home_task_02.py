import os
import time
import argparse
from datetime import datetime

def setup_logging(log_file):
    def log(message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
    return log

def clean_trash(trash_folder, age_thr, log):
    current_time = time.time()
    deleted_files = False
    
    for root, dirs, files in os.walk(trash_folder, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_mtime = os.path.getmtime(file_path)
                if current_time - file_mtime > age_thr:
                    os.remove(file_path)
                    log(f"Removed file: {file_path}")
                    deleted_files = True
            except Exception as e:
                log(f"Error removing file {file_path}: {str(e)}")
        
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    log(f"Removed empty directory: {dir_path}")
                    deleted_files = True
            except Exception as e:
                log(f"Error removing directory {dir_path}: {str(e)}")
    
    return deleted_files

def main():
    parser = argparse.ArgumentParser(description='Smart trash cleaner')
    parser.add_argument('--trash_folder_path', required=True, help='Path to trash folder')
    parser.add_argument('--age_thr', type=int, required=True, help='Age threshold in seconds')
    args = parser.parse_args()
    
    if not os.path.exists(args.trash_folder_path):
        print(f"Error: Trash folder '{args.trash_folder_path}' does not exist")
        return
    
    log_file = os.path.join(args.trash_folder_path, 'clean_trash.log')
    log = setup_logging(log_file)
    
    log("=== Starting trash cleaner ===")
    log(f"Trash folder: {args.trash_folder_path}")
    log(f"Age threshold: {args.age_thr} seconds")
    
    try:
        while True:
            if clean_trash(args.trash_folder_path, args.age_thr, log):
                log("Cleanup cycle completed with changes")
            else:
                log("Cleanup cycle completed - no changes")
            time.sleep(1)
    except KeyboardInterrupt:
        log("=== Stopping trash cleaner ===")
        print("\nTrash cleaner stopped by user")

if __name__ == '__main__':
    main()