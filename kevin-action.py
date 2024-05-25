import os
import glob

def count_lines_in_file(file_path):
   
    with open(file_path, 'r', encoding='utf-8') as file:
        return len(file.readlines())

def count_lines_in_directory(directory):
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        for file in glob.glob(os.path.join(root, '*.py')):
            total_lines += count_lines_in_file(file)
    return total_lines

# Remplacez 'chemin_vers_votre_dossier' par le chemin réel de votre dossier
directory_path = 'src/'
total_lines = count_lines_in_directory(directory_path)
print(f"Le nombre total de lignes dans tous les fichiers .py du dossier est : {total_lines}")
