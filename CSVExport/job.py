#!/usr/bin/python3
# coding=utf-8

# This file is part of DRK Impfzentrum.


import logging
import locale
import time
import datetime
import sys
sys.path.append("..")
from utils.database import Database
from createCSV import create_CSV
import pyexcel

logFile = '../../Logs/Impfzentrum/CSVExportJob.log'
logging.basicConfig(filename=logFile,level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('CSV Export')
logger.info('Starting')


if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        if len(sys.argv) == 2:
            requestedDate = sys.argv[1]
            sql = "Select Voranmeldung.id,Nachname,Vorname,Telefon,Mailadresse,Impfstoff.Kurzbezeichnung,Voranmeldung.Tag from Voranmeldung LEFT JOIN Termine ON Termine.id=Voranmeldung.Termin_id LEFT JOIN Station ON Station.id=Termine.id_station LEFT JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id where Voranmeldung.Used= 1 and Voranmeldung.Tag Between '%s 00:00:00' and '%s 23:59:59';" % (requestedDate.replace('-', '.'), requestedDate.replace('-', '.'))
        else:
            logger.debug('Input parameters are not correct, date and/or gesundheitsamt needed')
            raise Exception
        logger.debug('Getting all Events for employee of the month and year with the following query: %s' % (sql))
        exportEvents = DatabaseConnect.read_all(sql)
        logger.debug('Received the following entries: %s' %(str(exportEvents)))
        filename = create_CSV(exportEvents, requestedDate)
        sheet = pyexcel.get_sheet(file_name=filename, delimiter=";")
        sheet.save_as(str(filename).replace('csv','xlsx')) 
        print(filename.replace('csv','xlsx').replace('../../Reports/Impfzentrum/', ''))
        logger.info('Done')
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
    finally:
        DatabaseConnect.close_connection()
