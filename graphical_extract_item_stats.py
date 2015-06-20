import os, sys, re, collections, csv, Tkinter, tkFileDialog, logging, time
from string import ascii_uppercase as ucase
from extract_item_stats import ItemAnalysis, analyse_and_write_file

# select the directory
root = Tkinter.Tk()
root.withdraw()
selected = tkFileDialog.askdirectory(initialdir = ".")

# get the files in the selected directory
path = selected

# create logging file name with a datetime stamp and the logging file
logging.basicConfig(filename = "extract.log", format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level = logging.INFO)

files_analysed = 0
for file in os.listdir(path):
    current = os.path.join(path, file)
    if os.path.isfile(current) and current.split(".")[1] == 'txt':
        files_analysed += 1
        logging.info(current + " : commencing analysis.")
        analyse_and_write_file(current)

logging.info(str(files_analysed) + " files analysed.")
