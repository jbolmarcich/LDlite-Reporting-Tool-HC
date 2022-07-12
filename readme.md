# This Document is SIGNIFICANTLY out of date

# FOLIO Voucher Export

An Interface for running simple sql queries without an IDE

## Requirements


* Python 3.x
* json
* tkinter
* sys
* psycopg2



## Instructions

* Create json config file in the following format:
>{\
        "dbname": "",\
    "user": "",\
    "host": "",\
    "password": "",\
    "query_file": ""\
}
* Create folders **jsonBatchVouchers** and **xmlBatchVouchers** with subfolders for
  the names of each Batch Group you plan to export files from inside your working directory.
  
* Run main_gui.py using the command line 
  
* Using the menu, input a config file name or select the default option: "Default config.json" 
* Using the selection buttons navigate to the voucher batch export that you would like to save. Alternatively select "Run New Batch Export" to create a new export
* Select "Save Selected Batch (json)"
* Select "convert Saved Batches to XML" and either input a file name, or select: "Convert Most Recently Created File"

## Notes

* JSON Files are saved to 'jsonBatchVouchers/[Batch Group Name]'
* XML Files are saved to 'xmlBatchVouchers/[Batch Group Name]'
* Voucher Identifier lists from created xml files are saved to 'voucherIdentifiers/[Batch Group Name]'

## Contributors


* Aaron Neslin
* Amelia Sutton


## Version History
* 0.5
  * Filled XML Output Data.
  * Added Invoice Date Data to the export
* 0.2
	* Implemented GUI
	* Added Logging for better bug tracking.

* 0.1
    * Initial Release
    
## Known Issues
* 
## Planned Features
* Revamp of back-end to improve simplicity for maintenance

