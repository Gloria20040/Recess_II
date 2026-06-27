import os
import shutil
source_folder= "files"

folders={
    "Images":[".jpg", ".png", ".jpeg"],
    "Documents":[".pdf",".docx",".txt"],
    "Videos":[".mp4",".avi"],
}

for folder in folders:
    os.makedirs(os.path.join(source_folder, folder), exist_ok=True)

for file in os.listdir(source_folder):
    file_path = os.path.join(source_folder, file)
    if os.path.isfile(file_path):
        extension = os.path.splitext(file)[1].lower()
        
        for folder, extensions in folders.items():
            if extension in extensions:
                destination = os.path.join(source_folder, folder, file)
                shutil.move(file_path, destination)
                print(f"Moved {file} to {folder}")
                break
print("File organisation complete")
