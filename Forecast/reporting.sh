#!/bin/bash

# This file is part of DRK Testerfassung.

echo "Starting Report"
cd /home/webservice/Impfterminerfassung/TagesReport
python3 job.py $(date '+%Y-%m-%d') 1
echo "Reporting complete"