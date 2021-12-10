#!/usr/bin/python3
# coding=utf-8

# This file is part of DRK Impfzentrum.

from os import path,makedirs
import logging
import locale
import time
import datetime
import sys
sys.path.append("..")
from utils.database import Database
from createCSV import create_CSV
import pyexcel

try:
    basedir = '../../Logs/Impfzentrum/'
    logFile = f'{basedir}CSVExportJob.log'
    if not path.exists(basedir):
        makedirs(basedir)
    if not path.exists(logFile):
        open('logFile', 'w+')
    logging.basicConfig(filename=logFile,level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
except Exception as e:
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(f'CSV Exported Job started on: {datetime.datetime.now()}')
logger.info('Starting')


if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        if len(sys.argv) == 2:
            requestedDate = sys.argv[1]
            sql = f"Select Voranmeldung.id,Nachname,Vorname,Telefon,Mailadresse,Voranmeldung.Geburtsdatum,TIMESTAMPDIFF(year,Voranmeldung.Geburtsdatum,Termine.Tag),Impfstoff.Kurzbezeichnung,Voranmeldung.Booster,Station.Ort,Voranmeldung.Tag,Termine.Stunde,Termine.Slot from Voranmeldung LEFT JOIN Termine ON Termine.id=Voranmeldung.Termin_id LEFT JOIN Station ON Station.id=Termine.id_station LEFT JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id where Voranmeldung.Tag Between '{requestedDate.replace('-', '.')} 00:00:00' and '{requestedDate.replace('-', '.')} 23:59:59' ORDER BY Termine.Stunde,Termine.Slot;"
        else:
            logger.debug('Input parameters are not correct, date and/or gesundheitsamt needed')
            raise Exception
        logger.debug(f'Getting all Events for employee of the month and year with the following query: {sql}')
        exportEvents = DatabaseConnect.read_all(sql)
        logger.debug(f'Received the following entries: {str(exportEvents)}')
        filename = create_CSV(exportEvents, requestedDate)
        sheet = pyexcel.get_sheet(file_name=filename, delimiter=";")
        sheet.save_as(str(filename).replace('csv','xlsx')) 
        print(filename.replace('csv','xlsx').replace('../../Reports/Impfzentrum/', ''))
        logger.info('Done')
    except Exception as e:
        logging.error(f'The following error occured: {e}')
    finally:
        try:
            DatabaseConnect.close_connection()
        except Exception as e:
            logging.error(f'The following error occured in loop for unverified: {e}')
