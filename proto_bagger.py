"""
Program that takes a directory of bags, makes sure each bag has the correct format,
 and creates an accession import file.

Code written by Caitlin Donahue (caitlindonahue95@gmail.com) 

parts adapted from data_accessioner.py by Liam Everett (liam.m.everett@gmail.com) and Sahree Kasper (sahreek@gmail.com).
"""
import os
import sys
import datetime
import time
import csv
import shutil
import codecs
import cStringIO
import errno

class ProtoBagger:
    def __init__(self, top_directory):
        #the base directory that contains the bags
        self.top_dir = top_directory
        #the base of what the import file will be named
        self.import_file_name = None
        #The actual path to the import file
        self.import_file = None
        self.import_writer = None
        self.import_header = ["Month", "Day", "Year", "Title", "Identifier", \
        "Inclusive Dates", "Received Extent", "Extent Unit", "Processed Extent", \
        "Extent Unit", "Material Type", "Processing Priority", "Ex. Comp. Mont", \
        "Ex. Comp. Day", "Ex. Comp. Year", "Record Series", "Content", "Location", \
        "Range", "Section", "Shelf", "Extent", "ExtentUnit", "CreatorName", "Donor", \
        "Donor Contact Info", "Donor Notes", "Physical Description", "Scope Content", \
        "Comments"]
        #Default, can be set in bagger_settings
        self.location = "Archives Network Drive"
        #Default, can be set in bagger_settings
        #options are 'Bytes', 'Kilobytes', 'Megabytes', 'Gigabytes', and 'Terabytes'
        self.unit = "Gigabytes"
        self.name = "AccessionImport"
        self.excludes = []
        
        # Will keep track of values for the current bag's row in the import file
        self.import_row = {val:"" for val in self.import_header}
        #Setting up time
        self.now = datetime.datetime.now()
        self.day = "{0:02d}".format(self.now.day)
        self.month = "{0:02d}".format(self.now.month)
        self.year = self.now.year
        self.identifier = str(self.year)+"-"+self.month+"-"+self.day
        self.time = "{0:02d}".format(self.now.hour)+"-"+"{0:02d}".format(self.now.minute)+"-"+"{0:02d}".format(self.now.second)
        # Fields that are consistent in every row of the import file
        self.import_row["Month"] = self.month
        self.import_row["Day"] = self.day
        self.import_row["Year"] = self.year
        self.import_row["Extent Unit"] = self.unit
        self.import_row["Location"] = self.location
        self.import_row["ExtentUnit"] = self.unit
        self.initializeSettings("bagger_settings.txt")
        self.initializeImportFile()
        

    def initializeSettings(self, settings_file):
        """ Pulls settings for location, unit, and file_name from bagger_settings.txt """
        with open(settings_file) as f:
            f_content = [line.rstrip() for line in f]
            parse_state = "none"
            for i in range(len(f_content)):
                line = f_content[i]
                if parse_state == "none":
                    if line == "LOCATION:":
                        parse_state = "location"
                    elif line == "UNIT:":
                        parse_state = "unit"
                    elif line == "FILE_NAME:":
                        parse_state = "name"
                    elif line == "EXCLUDES:":
                        parse_state = "excludes"
                elif parse_state == "location":
                    if line == "UNIT:":
                        parse_state = "unit"
                    elif line == "FILE_NAME:":
                        parse_state = "name"
                    elif line == "EXCLUDES:":
                        parse_state = "excludes"
                    elif line != "":
                        self.location = line
                    else:
                        parse_state = "none"
                elif parse_state == "unit":
                    if line == "LOCATION:":
                        parse_state = "location"
                    elif line == "FILE_NAME:":
                        parse_state = "name"
                    elif line == "EXCLUDES:":
                        parse_state = "excludes"
                    elif line != "":
                        self.unit = line
                    else:
                        parse_state = "none"
                elif parse_state == "name":
                    if line == "LOCATION:":
                        parse_state = "location"
                    elif line == "UNIT:":
                        parse_state = "unit"
                    elif line == "EXCLUDES:":
                        parse_state = "excludes"
                    elif line != "":
                        self.name = line
                    else:
                        parse_state = "none"
                elif parse_state == "excludes":
                    if line == "LOCATION:":
                        parse_state = "location"
                    elif line == "UNIT:":
                        parse_state = "unit"
                    elif line == "FILE_NAME:":
                        parse_state = "name"
                    elif line != "":
                        self.excludes.append(line)
                    else:
                        parse_state = "none"
        #Checks if the unit recieved was a valid option, changes to Gigabytes if not
        yes = True
        while self.unit not in ["Bytes", "Kilobytes", "Megabytes", "Gigabytes", "Terabytes"] and yes:
            print "Unit supplied by bagger_settings.txt not valid"
            print "Valid units are Bytes, Kilobytes, Megabytes, Gigabytes, and Terabytes"
            print "Would you like to re-enter your value? (Y/N): "
            yes_string = raw_input().strip()
            if "Y" in yes_string or "y" in yes_string:
                print "Please enter the unit you would like to use: "
                self.unit = raw_input().strip()
            else:
                yes = False
                print "Running with default unit"
                self.unit = "Gigabytes"

    def iterate(self):
        """ Iterates through the Bags in the initial directory
         and writes their information to import file """
        bag_list = os.listdir(self.top_dir)
        for folder in bag_list:
            if self.name not in folder and folder not in self.excludes and os.path.isdir(os.path.join(self.top_dir, folder)):
                folder_path = os.path.join(self.top_dir, folder)
                #checks file structure
                self.process(folder_path)
                #writing to import file
                size = self.getSize(folder_path)
                self.writeToImportFile(folder, size, folder_path)

    def process(self, path):
        """ Processes each bag, making sure it contains the correct file structure. 
        The correct file structire is a data file with subdirectories
        named meta, dips, and originals """
        data_path = os.path.join(path, "data")
        w_meta_path = os.path.join(path, "meta")
        meta_path = os.path.join(data_path, "meta")
        w_orig_path = os.path.join(path, "originals")
        orig_path = os.path.join(data_path, "originals")
        w_dips_path = os.path.join(path, "dips")
        dips_path = os.path.join(data_path, "dips")
        #try to make the data file
        try:
            os.makedirs(data_path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        #Check if dips, meta, and originals exist in the bag
        #if they do, move them to data
        if os.path.isdir(w_meta_path):
            shutil.move(w_meta_path, meta_path)
        else:
            try:
                os.makedirs(meta_path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
        if os.path.isdir(w_orig_path):
            shutil.move(w_orig_path, orig_path)
        else:
            try:
                os.makedirs(orig_path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
        if os.path.isdir(w_dips_path):
            shutil.move(w_dips_path, dips_path)
        else:
            try:
                os.makedirs(dips_path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
        #checks for items in data that are not the three basic folders
        #if one exists, move it to the originals file
        item_list = os.listdir(path)
        for item in item_list:
            if ("meta" not in item) and ("dips" not in item) and ("originals" not in item) and ("data" not in item):
                new_path = os.path.join(orig_path, item)
                item_path = os.path.join(path, item)
                shutil.move(item_path, new_path)
        
        data_list = os.listdir(data_path)
        for item in data_list:
            if ("meta" not in item) and ("dips" not in item) and ("originals" not in item):
                item_path = os.path.join(data_path, item)
                new_path = os.path.join(orig_path, item)
                shutil.move(item_path, new_path)

    def initializeImportFile(self):
        """ Initializes the import file, setting up the name as (importname)_YYYY-MM-DD_HH-MM-SS
         and initializing the writer and header """
        file_name = self.name+"_"+self.identifier+"_"+self.time+".csv"
        self.import_file_name = file_name
        self.import_file = open(os.path.join(self.top_dir,file_name),'wb')
        self.import_writer = csv.writer(self.import_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        self.import_writer.writerow(self.import_header)

    def writeToImportFile(self, name, size, path):
        """ Writes the data for this bag as a row in the import file """
        self.import_row["Title"] = name
        self.import_row["Content"] = name
        self.import_row["Scope Content"] = name + "SCOPE"
        self.import_row["Identifier"] = self.identifier
        file_size_string = ""
        if size < 0.01:
            file_size_string = "0.01"
        else:
            file_size_string = "{0:.2f}".format(size)
        self.import_row["Received Extent"] = file_size_string
        self.import_row["Processed Extent"] = file_size_string
        self.import_row["Extent"] = file_size_string
        # write the import template row
        new_row = []
        for item in self.import_header:
            new_row.append(self.import_row[item])
        self.import_writer.writerow(new_row)

    def convertSize(self, size):
        """ Converts the size from bytes to a unit based on the settings file. The default is Gigabytes """
        new_size = size
        if self.unit == "Bytes":
            new_size = size 
        elif self.unit == "Kilobytes":
            new_size = size / float(1024)
        elif self.unit == "Megabytes":
            new_size = size / float(1048576)
        elif self.unit == "Gigabytes":
            new_size = size / float(1073741824)
        elif self.unit == "Terabytes":
            new_size = size / float(1099511627776)
        return new_size

    def getSize(self, dir):
        """ finds the size of a bag """
        size = self.recurse(0, dir)
        size = self.convertSize(size)
        return size

    def recurse(self, cur_size, path):
        """ recurses through all of the files in a bag and returns the total size of the bag """
        dir_list = []
        try:
            dir_list = os.listdir(path)
        except:
            print "Could not access Directory:"
            try:
                print path
            except:
                print "error printing directory name"
        if len(dir_list)!= 0:
            for folder in dir_list:
                full_path = os.path.join(path, folder)
                if os.path.isdir(full_path):
                    cur_size = self.recurse(cur_size, full_path)
                else:
                    try:
                        cur_size += os.path.getsize(full_path)
                    except:
                        print "Could not access file size:"
                        try:
                            print full_path
                        except:
                            print "error printing file name"
        return cur_size

def main():
    path = ""
    if len(sys.argv) > 1:
        path = sys.argv[1]
    if not os.path.isdir(path):
        print "Not a valid path"
        path = ""
    while path == "":
        print "Please enter your Directory: "
        path = raw_input().strip().strip('"').strip("'")
        if not os.path.isdir(path):
            print "Not a valid path"
            path = ""
    PB = ProtoBagger(path)
    print "Processing..."
    PB.iterate()
    print "Done"
main()


