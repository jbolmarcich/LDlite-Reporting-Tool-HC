# FOLIO Voucher Export

An Interface for running simple sql queries without a SQL IDE

## Requirements


* Python 3.x
* json
* tkinter
* sys
* psycopg2
* os

## Optional Requirements
* pyinstaller
  

## Instructions

* Create json config file in the following format:
>{\
    "dbname": " ",\
    "user": " ",\
    "host": " ",\
    "password": " ",\
    "query_filepath" : " ",\
    "output_filepath" : " "\
}
* **query_filepath** and **output_filepath** should point to existing folders that you have read/write permissons for.
* Run the program either with an .exe created with PyInstaller or by running LDliteSingleSelect.bat
* Using the dropdown select the **Query Name** for the .sql file you wish to excecute.
* If desired modify the **Output File Name**.
* Select **Run Query**
* When finished use **File>Exit** to close the program
  
## Notes
* It is recommended that you use PyInstaller to generate an executable version of LDliteSingleSelect.py to run instead 
of running it through LDliteSingleSelect.bat
* See https://github.com/5-C-Folio/LDlite-Queries for a collection of pre-created .sql files

## Contributors


* Amelia Sutton


## Version History

* 0.1
    * Initial Release
* 1.0
    * Full Release
    * Removed **query_file** parameter from the config file in favor of checking for query options in the folder specified by **query_filepath** simplifying the process of adding new queries and removing the need for additional config files.
    * Added **output_filepath** parameter to config
    
## Known Issues
* 
## Planned Features
*

