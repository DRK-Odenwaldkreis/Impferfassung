#!/bin/bash

# This file is part of DRK Testerfassung.

echo "Starting Report"
cd /home/webservice/Impfterminerfassung/TagesReport
python3 job.py $(date '+%Y-%m-%d') 1
chown www-data:www-data /home/webservice/Reports/Impfzentrum/Tagesreport_*
echo "Reporting complete"