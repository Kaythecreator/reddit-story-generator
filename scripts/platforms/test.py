import os

folder_path = "C:\\Users\\Kavin Seralathan\\Reddit-Story-Generator\\outputVideos"

print(os.listdir(folder_path))

for file in os.listdir(folder_path):
    print(file)