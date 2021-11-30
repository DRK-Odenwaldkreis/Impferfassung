#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of DRK Impfzentrum.


import sys
import csv
import logging
from utils.slot import get_slot_time

from datetime import datetime
sys.path.append("..")


logger = logging.getLogger('CSV Export')
logger.debug('Logger for createCSV was initialised')


def create_CSV(content, date):
    filename = "../../Reports/Impfzentrum/export_" + str(date) + ".csv"
    with open(filename, mode='w', newline='') as csvfile:
        writeEntry = csv.writer(csvfile, delimiter=';')
        writeEntry.writerow(["id",
                             "Nachname",
                             "Vorname",
                             "Telefonnummer",
                             "Mailadresse",
                             "Impfstoff",
                             "Ort",
                             "Datum",
                             "Uhrzeit"
                             ])
        for i in content:
            j = list(i)
            slot = j[8]
            stunde = j[7]
            j.pop()
            j.pop()
            j.append(get_slot_time(slot,stunde))
            writeEntry.writerow(j)
    return filename

