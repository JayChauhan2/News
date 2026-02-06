import os
import shutil
import glob

def reset():
    print("Resetting News Agent Data...")
    
    # Files to remove
    files_to_remove = [
        "public/news_data.json",
        "public/articles.json",
        "public/assignments.json",
        "journalist_memory.json",
        "backend/watchtower/journalist_memory.json"
    ]
    
    # Directories to clear (content only)
    dirs_to_clear = [
        "public/dossiers"
    ]
    
    # Base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Remove specific files
    for file_rel_path in files_to_remove:
        file_path = os.path.join(base_dir, file_rel_path)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_rel_path}")
            except Exception as e:
                print(f"Error deleting {file_rel_path}: {e}")
        else:
            print(f"Not found: {file_rel_path}")
            
    # Clear directory contents
    for dir_rel_path in dirs_to_clear:
        dir_path = os.path.join(base_dir, dir_rel_path)
        if os.path.exists(dir_path):
            # Get all files in the directory
            files = glob.glob(os.path.join(dir_path, '*'))
            for f in files:
                try:
                    os.remove(f)
                    print(f"Deleted in {dir_rel_path}: {os.path.basename(f)}")
                except Exception as e:
                    print(f"Error deleting {f}: {e}")
                    
    print("\nReset complete. Restart the backend to fetch fresh news.")

if __name__ == "__main__":
    confirmation = input("This will delete all news data and memory. Type 'yes' to continue: ")
    if confirmation.lower() == 'yes':
        reset()
    else:
        print("Operation cancelled.")
