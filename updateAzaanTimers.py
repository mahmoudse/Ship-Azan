#!/usr/bin/env python

import datetime
import time
import sys
sys.path.insert(0, '/home/pi/Ship-Azan/crontab')

from praytimes import PrayTimes
PT = PrayTimes() 

from crontab import CronTab
system_cron = CronTab(user='pi')

now = datetime.datetime.now()
strPlayFajrAzaanMP3Command = 'omxplayer -o local /home/pi/Ship-Azan/Adhan-fajr.mp3 > /dev/null 2>&1'
strPlayAzaanMP3Command = 'sudo python /home/pi/Ship-Azan/play/azan.py'
strUpdateCommand = 'python /home/pi/Ship-Azan/updateAzaanTimers.py >> /home/pi/adhan/adhan.log 2>&1'
strClearLogsCommand = 'truncate -s 0 /home/pi/Ship-Azan/adhan.log 2>&1'
strJobComment = 'ShipAzanClockJob'

#Set latitude and longitude here
#--------------------
lat = 31.261531
long = 32.305913


#Set calculation method, utcOffset and dst here
#By default system timezone will be used
#--------------------
PT.setMethod('Egypt')
utcOffset = -(time.timezone/3600)
isDst = time.localtime().tm_isdst


#HELPER FUNCTIONS
#---------------------------------
#---------------------------------
#Function to add azaan time to cron
def addAzaanTime (strPrayerName, strPrayerTime, objCronTab, strCommand):
  job = objCronTab.new(command=strCommand,comment=strPrayerName)  
  timeArr = strPrayerTime.split(':')
  hour = timeArr[0]
  min = timeArr[1]
  job.minute.on(int(min))
  job.hour.on(int(hour))
  job.set_comment(strJobComment)
  print job
  return

def addUpdateCronJob (objCronTab, strCommand):
  job = objCronTab.new(command=strCommand)
  job.minute.on(15)
  job.hour.on(3)
  job.set_comment(strJobComment)
  print job
  return

def addClearLogsCronJob (objCronTab, strCommand):
  job = objCronTab.new(command=strCommand)
  job.day.on(1)
  job.minute.on(0)
  job.hour.on(0)
  job.set_comment(strJobComment)
  print job
  return
#---------------------------------
#---------------------------------
#HELPER FUNCTIONS END

# Remove existing jobs created by this script
system_cron.remove_all(comment=strJobComment)

# Calculate prayer times
times = PT.getTimes((now.year,now.month,now.day), (lat, long), utcOffset, isDst) 
print times['fajr']
print times['dhuhr']
print times['asr']
print times['maghrib']
print times['isha']

# Add times to crontab
addAzaanTime('fajr',times['fajr'],system_cron,strPlayFajrAzaanMP3Command)
addAzaanTime('dhuhr',times['dhuhr'],system_cron,strPlayAzaanMP3Command)
addAzaanTime('asr',times['asr'],system_cron,strPlayAzaanMP3Command)
addAzaanTime('maghrib',times['maghrib'],system_cron,strPlayAzaanMP3Command)
addAzaanTime('isha',times['isha'],system_cron,strPlayAzaanMP3Command)

# Run this script again overnight
addUpdateCronJob(system_cron, strUpdateCommand)

# Clear the logs every month
addClearLogsCronJob(system_cron,strClearLogsCommand)

system_cron.write_to_user(user='pi')
print 'Script execution finished at: ' + str(now)
