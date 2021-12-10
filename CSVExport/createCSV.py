#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of DRK Impfzentrum.


import sys
import csv
import logging
from os import path,makedirs
from utils.slot import get_slot_time

from datetime import datetime
sys.path.append("..")


logger = logging.getLogger('CSV Export')
logger.debug('Logger for createCSV was initialised')


def create_CSV(content, date):
    basedir = f'../../Reports/Impfzentrum/'
    filename = f'{basedir}../../Reports/Impfzentrum/export_{str(date)}.csv'
    if not path.exists(basedir):
        print("Directory does not excist, creating it.")
        makedirs(basedir)
    with open(filename, mode='w', newline='') as csvfile:
        writeEntry = csv.writer(csvfile, delimiter=';')
        writeEntry.writerow(["id",
                             "Nachname",
                             "Vorname",
                             "Telefonnummer",
                             "Mailadresse",
                             "Geburtsdatum",
                             "Alter",
                             "Impfstoff",
                             "Booster",
                             "Ort",
                             "Datum",
                             "Uhrzeit"
                             ])
        logger.debug('Writing entries!')
        for i in content:
            logger.debug(f'Writing the following entry: {str(i)}')
            j = list(i)
            slot = j[9]
            stunde = j[8]
            j.pop()
            j.pop()
            j.append(get_slot_time(slot,stunde))
            writeEntry.writerow(j)
    return filename

