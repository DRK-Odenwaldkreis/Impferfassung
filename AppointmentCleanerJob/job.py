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
    logFile = f'{basedir}clean.log'
    if not path.exists(basedir):
        print("Directory does not excist, creating it.")
        makedirs(basedir)
    if not path.exists(logFile):
        print("File for logging does not excist, creating it.")
        open(logFile, 'w+')
    logging.basicConfig(filename=logFile,level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
except Exception as e:
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(f'Cleaning for not verified appointments started on: {datetime.datetime.now()}')
logger.info('Starting cleaner of unverified appointments')

if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        sql = "Select Voranmeldung_Verif.id, Voranmeldung.id, Voranmeldung.Termin_id FROM Voranmeldung_Verif JOIN Voranmeldung ON Voranmeldung_Verif.id_preregistration = Voranmeldung.id  WHERE Voranmeldung_Verif.updated < (NOW() - INTERVAL 15 MINUTE);"
        logger.debug('Finding all unverified appointments using the following query: %s' % (sql))
        unverified = DatabaseConnect.read_all(sql)
        logger.debug('Finding the following entries: %s' % (unverified))
        for i in unverified:
            try:
                termine_id = i[2]
                sql = f'Update Termine SET Used = NULL where id={termine_id};'
                logger.debug(f'Finding used Termin setting back to NULL using the following query: {sql}')
                DatabaseConnect.update(sql)
                voranmeldung_id = i[1]
                sql = f'Delete from Voranmeldung where id={voranmeldung_id};'
                logger.debug(f'Deleting Voranmeldung using the following query: {sql}')
                DatabaseConnect.delete(sql)
                verif_id=i[0]
                sql = f'Delete from Voranmeldung_Verif where id={verif_id};'
                logger.debug(f'Deleting Verif entry using the following query: {sql}')
                DatabaseConnect.delete(sql)
            except Exception as e:
                logger.error(f'The following error occured in loop for unverified: {e}')
        logger.info('Done for all')
    except Exception as e:
        logger.error(f'The following error occured in loop for unverified: {e}')
    finally:
        try:
            DatabaseConnect.close_connection()
        except Exception as e:
            logger.error(f'The following error occured in loop for unverified: {e}')
