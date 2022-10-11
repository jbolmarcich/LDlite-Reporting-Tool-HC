# This Document is SIGNIFICANTLY out of date

# FOLIO Voucher Export

An Interface for running simple sql queries without a SQL IDE

## Requirements


* Python 3.x
* json
* tkinter
* sys
* psycopg2
* os



## Instructions

* Create json config file in the following format:
>{\
        "dbname": "",\
    "user": "",\
    "host": "",\
    "password": "",\
    "query_file": ""\
}
* query_file should be the filepath for the .sql file you would like to run.
* Run the program either with an .exe created with PyInstaller or by running LDliteSingleSelect.bat
* Verify that the file path shown in the text field is correct and Select 'Run Query'
* 
## Notes
* It is recommended that you use PyInstaller to generate an executable version of LDliteSingleSelect.py to run instead 
of running it through LDliteSingleSelect.bat

## Contributors


* Amelia Sutton


## Version History

* 0.1
    * Initial Release
    
## Known Issues
* 
## Planned Features
*

