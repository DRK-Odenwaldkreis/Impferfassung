# This file is part of DRK Testfassung.


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


logFile = '../../Logs/Impfzentrum/appointmentNotification.log'
logging.basicConfig(filename=logFile,level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Generating Tickets')
logger.info('Starting Ticketgeneration')


if __name__ == "__main__":
    try:
        DatabaseConnect = Database()
        sql = "Select Voranmeldung.Vorname, Voranmeldung.Nachname, Voranmeldung.Mailadresse, Termine.Slot, Termine.Stunde, Voranmeldung.Tag, Voranmeldung.Token, Voranmeldung.id, Station.Ort, Station.Adresse, Termine.opt_station_adresse, Termine.opt_station, Impfstoff.Kurzbezeichnung from Voranmeldung JOIN Termine ON Termine.id=Voranmeldung.Termin_id JOIN Station ON Termine.id_station=Station.id JOIN Impfstoff ON Impfstoff.id=Station.Impfstoff_id where Voranmeldung.Token is not NULL and Voranmeldung.Mailsend = 0 and Voranmeldung.Mailadresse is not NULL;"
        content = DatabaseConnect.read_all(sql)
        logger.debug('Received the following recipients: %s' %(str(content)))
        for i in content:
            try:
                logger.debug('Received the following entry: %s' %(str(i)))
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
                    appointment = 'um ' + get_slot_time(slot,stunde) + ' Uhr'
                else:
                    appointment = ''
                if len(opt_ort) == 0 and len(opt_adress) == 0:
                    location = str(ort) + ", " + str(adress)
                else:
                    location = str(opt_ort) + "," + str(opt_adress)
                url = "https://impfzentrum-odw.de/registration/index.php?cancel=cancel&t=%s&i=%s" % (token,entry)
                if send_notification(mail,date,vorname,nachname,appointment,impfstoff,url,location): 
                    logger.debug('Mail was succesfully send, closing entry in db')
                    sql = "Update Voranmeldung SET Mailsend = 1 WHERE id = %s;" % (entry)
                    DatabaseConnect.update(sql)
            except Exception as e:
                logging.error("The following error occured in loop of content: %s" % (e))
        logger.info("Done")
    except Exception as e:
        logging.error("The following error occured: %s" % (e))
    finally:
        DatabaseConnect.close_connection()
