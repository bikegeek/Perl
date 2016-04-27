import os
import re
import sys
import errno


def process(dir_root, log_file_dir):
    """ Invoke the parsePirep.pl perl script, providing the
        input data, YYYYMMDDhh, log file directory, output csv file name 
    
        Args:
            dir_root (string): Directory root where input data resides.
                               Will traverse this and subdirectories for PIREP
                               data files.
            log_file_dir (string): Directory where log files will be saved.
  
    """

    perl_cmd = "/usr/bin/perl "
    parsePirep_cmd = "/home/minnawin/pirep/apps/scripts/src/ingest/parsePirep.pl "
 
    # Get a listing of all the directories and for each one, process the PIREP files
    # that reside in the subdirectory.
    full_files = get_filepaths(dir_root)
    for file in full_files:
        # Derive the YYYYMMDDhh from the file name, this is needed to indicate a timestamp
        # for processing via the parsePirep.py decoder.
        match = re.match(r'.*([0-9]{10}).(PIREP|pirep)',file)
        if match:
            YYYYMMDDhh = match.group(1)
            #Build the arguments for parsePirep.pl 
            arguments = (perl_cmd, parsePirep_cmd, " -i -v -L ", log_file_dir, " -t ", YYYYMMDDhh, "<", file,">/tmp/",YYYYMMDDhh,".csv")
            parsePirepcmd = "".join(arguments) 
            print parsePirepcmd 
        else:
            print "no match, can't create correct timestamp for parsePirep"


def get_filepaths(dir):
    """Generates the file names in a directory tree
       by walking the tree either top-down or bottom-up.
       For each directory in the tree rooted at
       the directory top (including top itself), it
       produces a 3-tuple: (dirpath, dirnames, filenames).

    Args:
        dir (string): The base directory from which we
                      begin the search for filenames.
    Returns:
        file_paths (list): A list of the full filepaths
                           of the data to be processed.


    """

    # Create an empty list which will eventually store
    # all the full filenames
    file_paths = []

    # Walk the tree
    for root, directories, files in os.walk(dir):
        for filename in files:
            # add it to the list only if it is a .PIREP file
            match = re.match(r'.*(PIREP|pirep)',filename)
            if match:
                # Join the two strings to form the full
                # filepath.
                filepath = os.path.join(root,filename)
                file_paths.append(filepath)
            else:
                continue
    return file_paths




def mkdir_p(dir):
    """Provide mkdir -p funtionality
    Args:
        dir (string): Full directory path to create if it doesn't exist
    Returns:
        None
    """

    try:
       os.makedirs(dir)
    except OSError as ose:
       if ose.errno == errno.EEXIST and os.path.isdir(dir):
           pass
       else:
           raise




if __name__ == "__main__":
    dir_root = "/home/minnawin/PIREP_Data"
    log_file_dir = "/tmp/pirepLogs"
    mkdir_p(log_file_dir)
    process(dir_root, log_file_dir)






