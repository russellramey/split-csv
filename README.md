# CSV Splitter

A Python utility to split large CSV files into smaller, manageable files using two different methods: by row count or by column values.

## Features

- **Row-based splitting**: Break large CSV files into smaller chunks with a specified number of rows
- **Column-based splitting**: Automatically create separate files for each unique value in a specified column
- **Preserves headers**: All output files include the original CSV headers
- **Timestamped outputs**: Files are named with timestamps to prevent overwrites
- **Error handling**: Validates inputs and provides helpful error messages

## Requirements

- Python 3.x
- No external dependencies (uses only standard library)

## Installation

1. Download `csvSplit.py` to your project directory
2. Make it executable (optional):
   ```bash
   chmod +x csvSplit.py
   ```

## Usage

### Mode 1: Split by Row Count

Split a CSV file into smaller files with a specified number of rows per file.

**Syntax:**
```bash
python3 csvSplit.py [INPUT_PATH] [BATCH_SIZE] [OUTPUT_PATH]
```

**Parameters:**
- `INPUT_PATH`: Path to the source CSV file (required)
- `BATCH_SIZE`: Number of rows per output file (optional, default: 100)
- `OUTPUT_PATH`: Directory for output files (optional, default: current directory)

**Examples:**
```bash
# Split into files with 100 rows each (default)
python3 csvSplit.py ./data.csv

# Split into files with 500 rows each
python3 csvSplit.py ./data.csv 500

# Split with custom batch size and output directory
python3 csvSplit.py ./data.csv 250 ./output/
```

**Output:**
```
20241121-143052-data-0.csv
20241121-143052-data-250.csv
20241121-143052-data-500.csv
...
```

### Mode 2: Split by Column Value

Create separate files for each unique value in a specified column.

**Syntax:**
```bash
python3 csvSplit.py [INPUT_PATH] --column [COLUMN_NAME] [OUTPUT_PATH]
```

**Parameters:**
- `INPUT_PATH`: Path to the source CSV file (required)
- `--column`: Flag to indicate column-based splitting (required for this mode)
- `COLUMN_NAME`: Name of the column to split by (required)
- `OUTPUT_PATH`: Directory for output files (optional, default: current directory)

**Examples:**
```bash
# Split by Status column
python3 csvSplit.py ./orders.csv --column Status

# Split by Category with custom output directory
python3 csvSplit.py ./products.csv --column Category ./output/

# Split by Region
python3 csvSplit.py ./sales.csv --column Region ./reports/
```

**Output:**
```
20241121-143052-orders-Status-Active.csv
20241121-143052-orders-Status-Pending.csv
20241121-143052-orders-Status-Completed.csv
...
```

## Use Cases

### Row-based Splitting
- Break down large datasets for easier processing
- Create batches for API uploads
- Split files to meet size restrictions
- Distribute data across multiple processes

### Column-based Splitting
- Separate records by category, status, or type
- Create department-specific reports
- Split multi-region data into regional files
- Organize data by date, customer, or any other grouping

## Example Scenarios

### Scenario 1: E-commerce Orders
Split orders by status to create separate files for processing:
```bash
python3 csvSplit.py ./orders.csv --column OrderStatus ./processing/
```
Creates: `orders-OrderStatus-Pending.csv`, `orders-OrderStatus-Shipped.csv`, etc.

### Scenario 2: Large Dataset Processing
Break a 100,000 row dataset into manageable 10,000 row chunks:
```bash
python3 csvSplit.py ./large_dataset.csv 10000 ./chunks/
```

### Scenario 3: Regional Sales Reports
Split sales data by region for regional managers:
```bash
python3 csvSplit.py ./sales_data.csv --column Region ./reports/
```

## Error Handling

The script provides helpful error messages for common issues:

- **File not found**: Verifies the input file exists
- **Invalid column**: Lists available columns if the specified column doesn't exist
- **Invalid directory**: Checks that the output directory exists
- **Missing arguments**: Shows usage information

## Output File Naming

### Row-based mode:
`[TIMESTAMP]-[ORIGINAL_FILENAME]-[ROW_NUMBER].csv`

Example: `20241121-143052-customers-0.csv`

### Column-based mode:
`[TIMESTAMP]-[ORIGINAL_FILENAME]-[COLUMN_NAME]-[VALUE].csv`

Example: `20241121-143052-orders-Status-Active.csv`

## Notes

- The timestamp format is `YYYYMMDD-HHMMSS`
- Column values are sanitized to create valid filenames (special characters replaced with underscores)
- Original CSV headers are preserved in all output files
- Empty values in the split column will create a file with an empty or underscore filename

## Troubleshooting

**Problem**: "Column not found" error  
**Solution**: Check the exact column name (case-sensitive) in your CSV headers

**Problem**: No output directory error  
**Solution**: Ensure the output directory exists or use `./` for current directory

**Problem**: Permission denied  
**Solution**: Check file/directory permissions or run with appropriate privileges

## License

This script is provided as-is for general use.

## Contributing

Feel free to modify and enhance this script for your specific needs.