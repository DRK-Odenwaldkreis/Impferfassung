#!/bin/bash

# This file is part of DRK Impfterminerfassung.

echo "Starting Report"
cd /home/webservice/Testerfassung/TagesReport
python3 job.py $(date '+%Y-%m-%d') 1
chown www-data:www-data /home/webservice/Reports/Tagesreport_*
echo "Reporting complete"