import os

DIR = os.path.dirname(os.path.realpath(__file__))
FOLDER_NAME = "target"
FOLDER_PATH = os.path.join(DIR, FOLDER_NAME)

# Create the directory
os.makedirs(FOLDER_PATH, exist_ok=True)

# Create a test file within the directory
with open(os.path.join(FOLDER_PATH, "testfile.txt"), "w") as file:
    file.write("This is a test file")