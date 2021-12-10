import logging
import locale
import time
import datetime
import sys
import csv
import numpy as np 
from pdfcreator.pdf import PDFgenerator
sys.path.append("..")
from utils.database import Database
from utils.sendmail import send_mail_report
from utils.getRequesterMail import get_Leitung_from_StationID


logFile = '../../Logs/Impfzentrum/TagesreportJob.log'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Tagesreport')
logger.info('Starting Tagesreporting')


if __name__ == "__main__":
    try:
        if len(sys.argv)  == 2:
            requestedDate = sys.argv[1]
            send=False
        elif len(sys.argv) == 3:
            requestedDate = sys.argv[1]
            send=True
        else:
            logger.debug('Input parameters are not correct, date and/or requested needed')
            raise Exception
        DatabaseConnect = Database()
        sql = "Select Impfstoff.id,Impfstoff.Kurzbezeichnung from Termine LEFT JOIN Station ON Station.id=Termine.id_station LEFT JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id  where Termine.Tag Between '%s 00:00:00' and '%s 23:59:59' group by Impfstoff.id';"% (requestedDate.replace('-', '.'), requestedDate.replace('-', '.'))
        vaccine = DatabaseConnect.read_all(sql)
        for i in vaccine:
            sql = "Select Voranmeldung.Geburtsdatum from Voranmeldung LEFT JOIN Termine ON Termine.id=Voranmeldung.Termin_id LEFT JOIN Station ON Station.id=Termine.id_station LEFT JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id where Voranmeldung.Used = 1 and Station.Impfstoff_id = %s and Voranmeldung.Tag Between '%s 00:00:00' and '%s 23:59:59';" % (i[0],requestedDate.replace('-', '.'), requestedDate.replace('-', '.'))
            ages = []
            result = DatabaseConnect.read_all(sql)
            for j in result:
                try:
                    today = datetime.date.today()
                    diff = (today - datetime.date.fromisoformat(j[0])).days/365
                    ages.append(diff)
                except:
                    pass
            logger.debug('Preped age: %s' %(str(ages)))
            try:
                sql = "Select Count(Voranmeldung.id), Station.Ort from Voranmeldung LEFT JOIN Termine ON Termine.id=Voranmeldung.Termin_id LEFT JOIN Station ON Station.id=Termine.id_station LEFT JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id where Voranmeldung.Used = 1 and Station.Impfstoff_id = %s and Voranmeldung.Tag Between '%s 00:00:00' and '%s 23:59:59' group by Station.id;" % (i[0],requestedDate.replace('-', '.'), requestedDate.replace('-', '.'))
                doses = DatabaseConnect.read_all(sql)
                logger.debug('Received doses entries: %s' %(str(doses)))
            except:
                logger.error('Sql read_all error, setting doses fix')
                doses = [(0,0)]
            try:
                sql = "Select Count(Voranmeldung.id) from Voranmeldung LEFT JOIN Termine ON Termine.id=Voranmeldung.Termin_id LEFT JOIN Station ON Station.id=Termine.id_station LEFT JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id where Voranmeldung.Used = 1 and Voranmeldung.Booster is not NULL and Station.Impfstoff_id = %s and Voranmeldung.Tag Between '%s 00:00:00' and '%s 23:59:59' group by Voranmeldung.Booster;" % (i[0],requestedDate.replace('-', '.'), requestedDate.replace('-', '.'))
                booster = DatabaseConnect.read_all(sql)
                logger.debug('Received booster entries: %s' %(str(booster)))
            except:
                logger.error('Sql read_all error, setting booster fix')
                booster = [(0,0),(0,1)]
            try:
                sql = "Select Count(Voranmeldung.id),Station.Ort from Voranmeldung LEFT JOIN Termine ON Termine.id=Voranmeldung.Termin_id LEFT JOIN Station ON Station.id=Termine.id_station LEFT JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id where Voranmeldung.Used = 1 and Datediff(Termine.Tag,Termine.Eintragungszeitpunkt) = 0 and Station.Impfstoff_id = %s and Voranmeldung.Tag Between '%s 00:00:00' and '%s 23:59:59' group by Station.Ort;" % (i[0],requestedDate.replace('-', '.'), requestedDate.replace('-', '.'))
                extra = DatabaseConnect.read_all(sql)
                logger.debug('Received extra entries: %s' %(str(extra)))
            except:
                logger.error('Sql read_all error, setting extra fix')
                extra = [(0,0)]
            try:
                sql = "Select Datediff(Termine.Tag,Voranmeldung.Anmeldezeitpunkt) from Voranmeldung LEFT JOIN Termine ON Termine.id=Voranmeldung.Termin_id LEFT JOIN Station ON Station.id=Termine.id_station LEFT JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id where Voranmeldung.Used = 1 and Station.Impfstoff_id = %s and Voranmeldung.Tag Between '%s 00:00:00' and '%s 23:59:59';" % (i[0],requestedDate.replace('-', '.'), requestedDate.replace('-', '.'))
                waiting = DatabaseConnect.read_all(sql)
                logger.debug('Received waiting entries: %s' %(str(waiting)))
            except:
                logger.error('Sql read_all error, setting waiting fix')
                waiting = [(0)]
            try:
                sql = "Select Count(Voranmeldung.id),Station.Ort from Voranmeldung LEFT JOIN Termine ON Termine.id=Voranmeldung.Termin_id LEFT JOIN Station ON Station.id=Termine.id_station LEFT JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id where Voranmeldung.Used = 0 and Station.Impfstoff_id = %s and Voranmeldung.Tag Between '%s 00:00:00' and '%s 23:59:59' group by Station.Ort;" % (i[0],requestedDate.replace('-', '.'), requestedDate.replace('-', '.'))
                noshow = DatabaseConnect.read_all(sql)
                logger.debug('Received no show entries: %s' %(str(noshow)))
            except:
                logger.error('Sql read_all error, setting noshow fix')
                noshow = [(0,0)]
            logger.debug('Getting all Events for a date with the following query: %s' % (sql))
            PDF = PDFgenerator(doses,booster,ages,waiting,noshow,extra,i[1], requestedDate)
            filename = PDF.generate()
            if send:
                logger.debug('Sending Mail')
                send_mail_report(filename,requestedDate,get_Leitung_from_StationID(0))
        logger.info('Done')
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
    finally:
        DatabaseConnect.close_connection()
