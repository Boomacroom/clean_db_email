# Set working directory if the files are in a different folder and project name.
os.chdir(".")
project_name = ""
extension = 'csv' # The extension we will be looking for.
all_filenames = [i for i in glob.glob(f'*.{extension}'] # Create a list of all matches

# Combine all of the file in the list all_filenames
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# Export at the project_name.csv
combined_csv.to_csv(f".processed/{project_name}.csv", index=False, encoding='utf-8-sig')