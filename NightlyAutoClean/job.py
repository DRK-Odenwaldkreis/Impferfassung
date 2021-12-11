#!/usr/bin/python3
# coding=utf-8

# This file is part of DRK Impfzentrum.

from os import path,makedirs
import logging
import sys
sys.path.append("..")
from utils.database import Database
import datetime

try:
    basedir = '../../Logs/Impfzentrum/'
    logFile = f'{basedir}cleanJob.log'
    if not path.exists(basedir):
        print("Directory does not excist, creating it.")
        makedirs(basedir)
    if not path.exists(logFile):
        print("File for logging does not excist, creating it.")
        open(logFile, 'w+')
    logging.basicConfig(filename=logFile,level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
except Exception as e:
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(f'Nightly Auto Clean started on: {datetime.datetime.now()}')
logger.info('Starting nightly clean')


if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        sql = "Delete from Voranmeldung where Used = 1;"
        logger.debug(f'Cleaning all Voranmeldungen that were used, using the following query: {sql}')
        DatabaseConnect.delete(sql)
        sql = "Delete from Voranmeldung where Tag <= (NOW() - INTERVAL 1 DAY);"
        logger.debug(f'Cleaning all Voranmeldungen that are prior today, using the following query: {sql}')
        DatabaseConnect.delete(sql)
        sql = "Delete from Termine where Tag <= (NOW() - INTERVAL 1 DAY);"
        logger.debug(f'Cleaning all Termine that are prior today, using the following query: {sql}')
        DatabaseConnect.delete(sql)
        logger.info('Done')
    except Exception as e:
        logger.error(f'The following error occured: {e}')
    finally:
        try:
            DatabaseConnect.close_connection()
        except Exception as e:
            logger.error(f'The following error occured in loop for unverified: {e}')
