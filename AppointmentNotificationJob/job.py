# This file is part of DRK Testfassung.

from os import path,makedirs
import pyqrcode
import png
import sys
sys.path.append("..")
from utils.database import Database
from utils.sendmail import send_notification
from utils.slot import get_slot_time
import datetime
import time
import locale
import logging


try:
    basedir = '../../Logs/Impfzentrum/'
    logFile = f'{basedir}appointmentNotification.log'
    if not path.exists(basedir):
        print("Directory does not excist, creating it.")
        makedirs(basedir)
    if not path.exists(logFile):
        print("File for logging does not excist, creating it.")
        open('logFile', 'w+')
    logging.basicConfig(filename=logFile,level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
except Exception as e:
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(f'Cleaning for not verified appointments started on: {datetime.datetime.now()}')
logger.info('Starting Ticketgeneration')



if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        sql = "Select Voranmeldung.Vorname, Voranmeldung.Nachname, Voranmeldung.Mailadresse, Termine.Slot, Termine.Stunde, Voranmeldung.Tag, Voranmeldung.Token, Voranmeldung.id, Station.Ort, Station.Adresse, Termine.opt_station_adresse, Termine.opt_station, Impfstoff.Kurzbezeichnung from Voranmeldung JOIN Termine ON Termine.id=Voranmeldung.Termin_id JOIN Station ON Termine.id_station=Station.id JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id where Voranmeldung.Token is not NULL and Voranmeldung.Mailsend = 0 and Voranmeldung.Mailadresse is not NULL;"
        content = DatabaseConnect.read_all(sql)
        logger.debug(f'Received the following recipients: {str(content)}')
        for i in content:
            try:
                logger.debug(f'Received the following entry: {str(i)}')
                vorname = i[0]
                nachname = i[1]
                mail = i[2]
                slot = i[3]
                stunde = i[4]
                date = i[5]
                token = i[6]
                entry = i[7]
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
                url = f'https://impfzentrum-odw.de/registration/index.php?cancel=cancel&t={token}&i={entry}'
                if send_notification(mail,date,vorname,nachname,appointment,impfstoff,url,location): 
                    logger.debug('Mail was succesfully send, closing entry in db')
                    sql = f'Update Voranmeldung SET Mailsend = 1 WHERE id = {entry};'
                    DatabaseConnect.update(sql)
            except Exception as e:
                logger.error(f'The following error occured in loop of content: {e}')
        logger.info("Done")
    except Exception as e:
        logger.error(f'The following error occured: {e}')
    finally:
        try:
            DatabaseConnect.close_connection()
        except Exception as e:
            logger.error(f'The following error occured in loop for unverified: {e}')
