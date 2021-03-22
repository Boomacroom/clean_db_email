import pandas as pd

# Set the project name and read in the CSV file
# It's nice to use this in Jupyter for the tab completion

project_name = ""
input_csv = 'input.csv'
number_lines = sum(1 for row in (open(input_csv)))
# Set the amount of rows you need
max_rows = 600
for i in range(1,number_lines,max_rows):
    df = pd.read_csv(input_csv,
          header=None,
          nrows = max_rows,
          skiprows = i)

    # Use the project_name to name the output files
    output_csv = f'{project_name}' + str(i) + '.csv'
    df.to_csv(output_csv,
          index=False,
          header=False,
          mode='a', # This is append rows
          chunksize=max_rows) # The chosen amount of rows per file from earlier