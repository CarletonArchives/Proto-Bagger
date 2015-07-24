# Proto-Bagger
Creates basic directory structure for bags of archival records, in preparation for processing and running Bagit.

Code written by Caitlin Donahue (caitlindonahue95@gmail.com) 
parts adapted from data_accessioner.py by Liam Everett (liam.m.everett@gmail.com) and Sahree Kasper (sahreek@gmail.com).

##Installing Python:
You will need Python 2.7 installed on your computer to run this program.
Python can be found here: https://www.python.org/download/releases/2.7.5/

Instructions on setting up Pyton on your computer can be found here: https://apps.carleton.edu/curricular/cs/resources/source/python_install/

##Usage:
(Mac) Open a terminal window by navigating to "Applications -> Utilities -> Terminal" and clicking on the Terminal icon
(PC) Open a command prompt by selecting Start/Run and typing cmd and Enter or Start/Programs/Accessories/Command Prompt.

First navigate in your terminal to the folder in which proto_bagger.py is contained, then type the following (replacing PATH with the location of proto_bagger.

```cd PATH```

There are two options for running proto_bagger.py:

``` python proto_bagger.py ```

- This will prompt you for the path to your directory.


``` python proto_bagger.py PATH```
        
- Replace PATH with the path to your directory.
- This will automatically run proto_bagger.


###Input:
- A directory containing bags that you would like to format.

###Output:
- AccessionImport file.
- Each Bag will have the contain a data folder, which contains meta, dips, and originals folders.

###bagger_settings.txt:
For the program to run properly you need to have bagger_settings.txt in the same folder as proto_bagger.py
There are three fields you can modify in the bagger_settings.txt file: LOCATION, UNIT, and FILE_NAME
- LOCATION defines what will be entered in the field "location" in the AccessionImport file
- UNIT defines what unit will be listed in the AccessionImport file, and how the file sizes will be calculated.
    - Valid inputs for unit are "Bytes", "Kilobytes", "Megabytes", "Gigabytes", and "Terabytes".
    - This is case sensitive. 
    - the default is Gigabytes
- FILE_NAME defines what your AccessionImport file will be named.
    - The default is AccessionImport.
- EXCLUDES defines what files to ignore in the top directory.

###AccessionImport file: 
You can define the name of the accession import file in bagger_settings.txt.
The file will be saved alongside the bags in the top directory, and will have the date and time included in the format:
            <name>_YYYY-MM-DD_HH-MM-SS
The accession import file is a file containing information on the bags according to the following chart:
```
 ================================================================================
|Field               |  Value                                                    |
|================================================================================| 
|Month               | Current month (MM)                                        |
|--------------------+-----------------------------------------------------------|
|Day                 | Current day (DD)                                          |
|--------------------+-----------------------------------------------------------|
|Year                | Current Year (YYYY)                                       |
|--------------------+-----------------------------------------------------------|
|Title               | BAGNAME                                                   |
|--------------------+-----------------------------------------------------------|
|Identifier          | Current YYYY-MM-DD                                        |
|--------------------+-----------------------------------------------------------|
|Inclusive Dates     |                                                           |
|--------------------+-----------------------------------------------------------|
|Received Extent     | Size of bag rounded up to the nearest 100th of a gigabyte |
|--------------------+-----------------------------------------------------------|
|Extent Unit         | value of extentUnit in settings file                      |
|--------------------+-----------------------------------------------------------|
|Processed Extent    | Size of bag rounded up to the nearest 100th of a gigabyte |
|--------------------+-----------------------------------------------------------|
|Extent Unit         | value of extentUnit in settings file                      |
|--------------------+-----------------------------------------------------------|
|Material Type       |                                                           |
|--------------------+-----------------------------------------------------------|
|Processing Priority |                                                           |
|--------------------+-----------------------------------------------------------|
|Ex. Comp. Mont      |                                                           |
|--------------------+-----------------------------------------------------------|
|Ex. Comp. Day       |                                                           |
|--------------------+-----------------------------------------------------------|
|Ex. Comp. Year      |                                                           |
|--------------------+-----------------------------------------------------------|
|Record Series       |                                                           |
|--------------------+-----------------------------------------------------------|
|Content BAGNAME     |                                                           |
|--------------------+-----------------------------------------------------------|
|Location            | location variable in settings file                        |
|--------------------+-----------------------------------------------------------|
|Range               |                                                           |
|--------------------+-----------------------------------------------------------|
|Section             |                                                           |
|--------------------+-----------------------------------------------------------|
|Shelf               |                                                           |
|--------------------+-----------------------------------------------------------|  
|Extent              | Size of bag rounded up to the nearest 100th of a gigabyte |
|--------------------+-----------------------------------------------------------|
|ExtentUnit          | value of extentUnit in settings file                      |
|--------------------+-----------------------------------------------------------|
|CreatorName         |                                                           |
|--------------------+-----------------------------------------------------------|
|Donor               |                                                           |
|--------------------+-----------------------------------------------------------|
|Donor Contact Info  |                                                           |
|--------------------+-----------------------------------------------------------|
|Donor Notes         |                                                           |
|--------------------+-----------------------------------------------------------|
|Physical Description|                                                           |
|--------------------+-----------------------------------------------------------|    
|Scope Content       | BAGNAME + "SCOPE"                                         |
|--------------------+-----------------------------------------------------------|
|Comments            |                                                           |
 ================================================================================
```

