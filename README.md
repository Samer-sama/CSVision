# 1. Created virtual environment and activated it
# --> python -m venv venv
# --> \venv\Scripts\activate
# 2. Directory Structure
CSVision/ 
├── venv/                       # Virtual environment directory 
├── src/                        # Source code for your application 
│ ├── __init__.py               # Makes src a Python package 
│ ├── main.py                   # Entry point of the application 
│ ├── csv_data_manager.py       # Module for CSV file operations 
│ ├── gui/                      # GUI package 
│ │ ├── __init__.py 
│ │ ├── main_window.py          # Main window class 
│ │ └── chart_view.py           # Chart-related UI components 
│ │ └── header_list_panel.py    # Header list-related UI components
│ │ └── header_panel.py         # Selected header panel-related UI components
│ └── utils/                    # Utility functions and classes 
│ └── __init__.py 
├── unittests/                  # Automated tests for your application 
│ ├── __init__.py 
│ └── csv_data_manager_test .py 
├── resources/                  # Data files, images, etc. 
│ └── data.csv                  # Example CSV file 
└── requirements.txt            # Project dependencies
└── README.md                   # README
# 3. In requirements.txt set up and then installed the dependencies
# --> pip install -r requirements.txt
