#!/bin/bash

# This file is part of DRK Impfterminerfassung.

echo "Starting Reminding"
cd /home/webservice/Impfterminerfassung/AppointmentReminderJob
python3 job.py $(date '+%Y-%m-%d')
echo "Reminding complete"