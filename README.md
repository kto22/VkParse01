# VK Message Parser

A Python application for parsing and exporting VK (VKontakte) messages from conversations. This tool allows you to extract messages from VK conversations and export them in various formats (CSV and TXT).

## Features

- Parse messages from VK conversations using the VK API
- Multi-process message parsing for improved performance
- Export messages to CSV format
- Convert messages to TXT format
- User-friendly GUI interface
- Support for both Linux and Windows systems

## Prerequisites

- Python 3.x
- VK API access token
- Required Python packages (install via pip):
  - vk_api
  - tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kto22/VkParse01.git
cd VkParse01
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

3. Install required packages:
```bash
pip install vk_api
```

## Usage

1. Run the main script:
```bash
python main.py
```

2. In the GUI interface, provide:
   - VK API token
   - User ID of the conversation
   - Start message number
   - Number of messages to parse
   - Output directory

3. The program will:
   - Parse the specified messages
   - Create CSV and TXT files in the Output directory
   - Automatically open the Output directory when complete

## Project Structure

- `main.py` - Main entry point and GUI interface
- `VkApiFunc.py` - VK API interaction and message parsing logic
- `CSVFunctions.py` - CSV file manipulation functions
- `UI.py` - User interface implementation
- `Output/` - Directory for exported files
- `CSV_temp/` - Temporary directory for CSV processing
- `JSON/` - Directory for JSON data storage

## Output Files

The program generates the following files in the Output directory:
- `final.csv` - Final CSV file containing parsed messages

## Notes

- Make sure you have a valid VK API token with appropriate permissions
- The program uses multi-processing for better performance
- Temporary files are automatically cleaned up after processing
- The output directory will be automatically opened after completion

