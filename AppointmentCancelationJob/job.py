#!/usr/bin/python3
# coding=utf-8

# This file is part of DRK Impfzentrum.

from os import path,makedirs
import logging
import sys
sys.path.append("..")
from utils.database import Database
from utils.sendmail import send_cancel_appointment
import datetime


try:
    basedir = '../../Logs/Impfzentrum/'
    logFile = f'{basedir}cancelJob.log'
    if not path.exists(basedir):
        print("Directory does not excist, creating it.")
        makedirs(basedir)
    if not path.exists(logFile):
        print("File for logging does not excist, creating it.")
        open(logFile, 'w+')
    logging.basicConfig(filename=logFile,level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
except Exception as e:
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(f'Cancel job for appointment cancelation started on: {datetime.datetime.now()}')
logger.info('Starting Cancelation of appointments')


if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        sql = "Select Voranmeldung.Vorname, Voranmeldung.Nachname, Voranmeldung.Mailadresse, Voranmeldung.Tag, Voranmeldung.id from Voranmeldung LEFT JOIN Termine ON Termine.id=Voranmeldung.Termin_id where Termine.Tag is NULL and Voranmeldung.Mailadresse is not NULL;"
        logger.debug('Cancel all appointments, using the following query: %s' % (sql))
        canceledAppointments = DatabaseConnect.read_all(sql)
        logger.debug('Received the following cancel objects: %s' %(str(canceledAppointments)))
        for i in canceledAppointments:
            try:
                logger.debug(f'Received the following entry: {str(i)}')
                vorname = i[0]
                nachname = i[1]
                mail = i[2]
                entry = i[4]
                date = i[3]
                logger.debug('Handing over to sendmail of reminder')
                if send_cancel_appointment(mail, date, vorname, nachname):
                    logger.debug('Mail was succesfully send, closing entry in db')
                    sql = f'Delete from Voranmeldung where id = {entry};'
                    DatabaseConnect.delete(sql)
            except Exception as e:
                logger.error(f'The following error occured in loop of cancel Appointments: {e}')
        logger.info('Done for all')
    except Exception as e:
        logger.error(f'The following error occured: {e}')
    finally:
        try:
            DatabaseConnect.close_connection()
        except Exception as e:
            logger.error(f'The following error occured within finally statement: {e}')
