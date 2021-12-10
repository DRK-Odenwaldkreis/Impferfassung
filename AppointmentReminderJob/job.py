#!/usr/bin/python3
# coding=utf-8

# This file is part of DRK Impfzentrum.

from os import path,makedirs
import logging
import sys
sys.path.append("..")
from utils.database import Database
from utils.sendmail import send_mail_reminder
from utils.slot import get_slot_time
import datetime

try:
    basedir = '../../Logs/Impfzentrum/'
    logFile = f'{basedir}reminderJob.log'
    if not path.exists(basedir):
        makedirs(basedir)
    if not path.exists(logFile):
        open('logFile', 'w+')
    logging.basicConfig(filename=logFile,level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
except Exception as e:
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(f'Reminder job for appointment started on: {datetime.datetime.now()}')
logger.info('Starting reminder of Appointments')


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            requestedDate = sys.argv[1]
        else:
            logger.debug('Input parameters are not correct, date needed')
            raise Exception
        DatabaseConnect = Database()
        sql = f"Select Voranmeldung.Vorname, Voranmeldung.Nachname, Voranmeldung.Mailadresse, Termine.Slot, Termine.Stunde, Voranmeldung.Tag, Voranmeldung.Token, Voranmeldung.id, Station.Ort, Station.Adresse, Termine.opt_station_adresse, Termine.opt_station, Impfstoff.Kurzbezeichnung from Voranmeldung JOIN Termine ON Termine.id=Voranmeldung.Termin_id JOIN Station ON Termine.id_station=Station.id JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id where Voranmeldung.Tag Between '{requestedDate} 00:00:00' and '{requestedDate} 23:59:59' and Reminded = 0 and Voranmeldung.Token is not NULL and Voranmeldung.Mailadresse is not NULL;"
        logger.debug(f'Getting all appointments for {requestedDate}, using the following query: {sql}')
        recipients = DatabaseConnect.read_all(sql)
        logger.debug(f'Received the following recipients: {str(recipients)}')
        for i in recipients:
            try:
                logger.debug(f'Received the following entry: {str(i)}')
                slot = i[3]
                vorname = i[0]
                nachname = i[1]
                stunde = i[4]
                mail = i[2]
                entry = i[7]
                token = i[6]
                date = i[5]
                ort = i[8]
                adress = i[9]
                opt_ort = i[10]
                opt_adress = i[11]
                impfstoff = i[12]
                if slot:
                    appointment = f'um {get_slot_time(slot,stunde)} Uhr'
                else:
                    appointment = ''
                if len(opt_ort) == 0 and len(opt_adress) == 0:
                    location = f'{str(ort)}, {str(adress)}'
                else:
                    location = f'{str(opt_ort)}, {str(opt_adress)}'
                logger.debug('Handing over to sendmail of reminder')
                url = f'https://impfzentrum-odw.de/registration/index.php?cancel=cancel&t={token}&i={entry}'
                if send_mail_reminder(mail, date, vorname, nachname, appointment, impfstoff, url, location):
                    logger.debug('Mail was succesfully send, closing entry in db')
                    sql = f'Update Voranmeldung SET Reminded = 1 WHERE id = {entry};'
                    DatabaseConnect.update(sql)
            except Exception as e:
                logger.error(f'The following error occured in loop of recipients: {e}')
        logger.info('Done for all')
    except Exception as e:
        logger.error(f'The following error occured: {e}')
    finally:
        try:
            DatabaseConnect.close_connection()
        except Exception as e:
            logger.error(f'The following error occured in loop for unverified: {e}')
