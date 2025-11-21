#
# CSV SPLITTER
# Break up a CSV into smaller files with desired row count OR split by column values
# 
# Usage
# Mode 1 - Split by row count:
# - python3 ./csvSplit.py [INPUT_PATH] [BATCH_SIZE] [OUTPUT_PATH]
# 
# Mode 2 - Split by column value:
# - python3 ./csvSplit.py [INPUT_PATH] --column [COLUMN_NAME] [OUTPUT_PATH]
# 
# Examples 
# - python3 ./csvSplit.py ./sample.csv 100
# - python3 ./csvSplit.py ./sample.csv --column Status ./output/
# - python3 ./csvSplit.py ./sample.csv --column Category
# 

import sys
import csv
import time
import pathlib
from collections import defaultdict

#
# Variables
#
input = ""
outputDir = "./"
chunkSize = 100
csvData = []
splitByColumn = None

#
# Arguments
# 
try:
    input = sys.argv[1]
except:
    print("Usage:")
    print("  Mode 1: python3 ./csvSplit.py [INPUT_PATH] [BATCH_SIZE] [OUTPUT_PATH]")
    print("  Mode 2: python3 ./csvSplit.py [INPUT_PATH] --column [COLUMN_NAME] [OUTPUT_PATH]")
    sys.exit(1)

# Check if using column-based splitting
if len(sys.argv) > 2 and sys.argv[2] == "--column":
    try:
        splitByColumn = sys.argv[3]
        if len(sys.argv) > 4:
            outputDir = sys.argv[4]
    except IndexError:
        print("Error: --column requires a column name")
        print("Usage: python3 ./csvSplit.py [INPUT_PATH] --column [COLUMN_NAME] [OUTPUT_PATH]")
        sys.exit(1)
else:
    # Row-based splitting
    try:
        chunkSize = sys.argv[2]
        outputDir = sys.argv[3]
    except IndexError:
        pass
    except Exception as e:
        print(e)
        sys.exit(1)

# Process input file
try:
    with open(input, 'r', newline="") as inputFile:
        reader = csv.reader(inputFile, delimiter=",")
        for (i, line) in enumerate(reader):
            csvData.append(line)
except FileNotFoundError: 
    print(f"Error trying to read input file from path {input}")
    sys.exit(1)
except Exception as e:
    print(e)
    sys.exit(1)

# CSV headers
headers = csvData.pop(0)
timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(int(time.time())))
filename = pathlib.PurePath(input)
filename = filename.name.replace('.csv', '')

# Mode 2: Split by column value
if splitByColumn:
    try:
        columnIndex = headers.index(splitByColumn)
    except ValueError:
        print(f"Error: Column '{splitByColumn}' not found in CSV headers")
        print(f"Available columns: {', '.join(headers)}")
        sys.exit(1)
    
    # Group rows by column value
    groupedData = defaultdict(list)
    for row in csvData:
        if columnIndex < len(row):
            columnValue = row[columnIndex]
            # Sanitize filename
            safeValue = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in columnValue)
            groupedData[safeValue].append(row)
    
    # Write a file for each unique value
    print(f"Splitting by column '{splitByColumn}'...")
    for value, rows in groupedData.items():
        outputFilename = f"{timestamp}-{filename}-{splitByColumn}-{value}.csv"
        try:
            with open(outputDir + outputFilename, 'w', newline='') as outputFile:
                writer = csv.writer(outputFile)
                writer.writerow(headers)
                writer.writerows(rows)
            print(f"Created: {outputFilename} ({len(rows)} rows)")
        except FileNotFoundError:
            print(f"Error trying to save output file, no directory for {outputDir}")
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
    
    print(f"Split complete: {len(groupedData)} files created")

# Mode 1: Split by row count
else:
    print(f"Splitting into chunks of {chunkSize} rows...")
    fileCount = 0
    for i in range(len(csvData)):
        if i % int(chunkSize) == 0:
            try:
                with open(outputDir + (f"{timestamp}-{filename}-{i}.csv"), 'w', newline='') as outputFile:
                    writer = csv.writer(outputFile)
                    writer.writerow(headers)
                    writer.writerows(csvData[i:i+int(chunkSize)])
                    fileCount += 1
            except FileNotFoundError:
                print(f"Error trying to save output file, no directory for {outputDir}")
                sys.exit(1)
            except Exception as e:
                print(e)
                sys.exit(1)
    
    print(f"Split complete: {fileCount} files created")