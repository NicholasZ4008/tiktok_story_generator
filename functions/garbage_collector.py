import os
import shutil

def clean_folder(folder_path):
    """
    Remove all files and subdirectories in the specified folder.
    If the folder doesn't exist, create it.
    """
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        os.makedirs(folder_path)
    
    print(f"Cleaned folder: {folder_path}")

def clean_file(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Successfully deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}. Reason: {e}")
    else:
        print(f"File not found: {file_path}")