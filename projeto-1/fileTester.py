import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "res/datasetA.txt"
abs_file_path = os.path.join(script_dir, rel_path)
print(abs_file_path)
