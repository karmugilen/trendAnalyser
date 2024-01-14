from download_Stocks import stockDownload
from combaincsv import combine_csv_files
from outputFile import outputFiles
from deleteCsv import delete_all_csv_files
from download_StocksUs import stockDownloadUS
import time
from copyToDir import copy_file
from mergeFile import mergeFile
from deleteFiles import delete_file

value=input("Indian Stock 'Enter' / US Stock Press '1 And Enter' ")

if value == "1":
    stockDownloadUS()
else:
    stockDownload()
    
time.sleep(3)
combine_csv_files()
time.sleep(3)
# copy_file()
# mergeFile()
# delete_file()
outputFiles()
time.sleep(3)
delete_all_csv_files()
input("wait")