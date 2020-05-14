# Raspberry Pi Vessel Azan 
This projects uses a python script which automatically calculates [adhan](https://en.wikipedia.org/wiki/Adhan) times every day and plays all five adhans at their scheduled time using cron. 
Azan Sound will be public via Public Address on the vessel 

## Prerequisites
1. Raspberry Pi running Raspbian
  1. I would stay away from Raspberry Pi zero esp if you're new to this stuff since it doesn't come with a built in audio out port.
  2. Also, if you haven't worked with raspberry pi before, I would highly recommend using [these](https://www.raspberrypi.org/documentation/installation/noobs.md) instructions to get it up and running: https://www.raspberrypi.org/documentation/installation/noobs.md
2. Speakers
3. Auxiliary audio cable

## Instructions
1. Install git: Go to raspberry pi terminal (command line interface) and install `git`
  * `$ sudo apt-get install git`
2. Clone repo: Clone this repository on your raspberry pi in your `home` directory. (Tip: run `$ cd ~` to go to your home directory)
  * `$ git clone https://github.com/mahmoudse/vesselazan.git`
  * After doing that you should see an `adhan` direcotry in your `home` directory. 
3. Go into `vesselazan` directory: `$cd vesselazan`
4. Open `updateAzaanTimers.py` in your favorite editor. For instance, `nano` is a simple one: `$ nano updateAzaanTimers.py`

## Configuration
The original python script is super configurable. Please see the [manual](http://praytimes.org/manual) for advanced instructions. However, below are the three basic things you'll need to change to get it up and running.

* Set the latitude and longitude so it can calculate accurate prayer times for that location. Modify the following lines:
```
#Set latitude and longitude here
#--------------------
lat = 31.261531
long = 32.305913
```
* Set adhan time [calculation method](http://praytimes.org/manual#Set_Calculation_Method). Modify the following line:
```
PT.setMethod('Egypt')
```
Save your changes by pressing `Control X` and then `Y`.

## Run it for the first time
Run this command `$ python /home/pi/vesselazan/updateAzaanTimers.py`. If everythig worked, your output will look something like this:
```
03:14
11:47
15:26
18:39
20:09
14 3 * * * omxplayer -o local /home/pi/vesselazan/audio/Adhan-fajr.mp3 > /dev/null 2>&1 # VesselAzanClockJob
47 11 * * * sudo python /home/pi/vesselazan/play/azan.py # VesselAzanClockJob
26 15 * * * sudo python /home/pi/vesselazan/play/azan.py # VesselAzanClockJob
39 18 * * * sudo python /home/pi/vesselazan/play/azan.py # VesselAzanClockJob
9 20 * * * sudo python /home/pi/vesselazan/play/azan.py # VesselAzanClockJob
15 3 * * * python /home/pi/vesselazan/updateAzaanTimers.py >> /home/pi/vesselazan/adhan.log 2>&1 # VesselAzanClockJob
@monthly truncate -s 0 /home/pi/vesselazan/adhan.log 2>&1 # VesselAzanClockJob
Script execution finished at: 2020-05-14 23:05:58.833252
```

If you look at the last few lines, you'll see that 5 adhan times have been scheduled. Then there is another line at the end which makes sure that at 1am every day the same script will run and calculate adhan times for that day. And lastly, there is a line to clear logs on a monthly basis so that your log file doesn't grow too big.

VOILA! You're done!! Plug in your speakers and enjoy!

## Tips:
* 'crontab -e' to modify cornjob file
1. You can see your currently scheduled jobs by running `crontab -l`
2. The output of the job that runs at 1am every night is being captured in `/home/pi/adhan/adhan.log`. This way you can keep track of all successful runs and any potential issues. This file will be truncated at midnight on the forst day of each month. To view the output type `$ cat /home/pi/vesselazan/adhan.log`

### Credits
I have made modifications / bug fixes but I've used the following as starting point:
* Python code to calculate adhan times: http://praytimes.org/code/ 
* Basic code to turn the above into an adhan clock: http://randomconsultant.blogspot.co.uk/2013/07/turn-your-raspberry-pi-into-azaanprayer.html
* Cron scheduler: https://pypi.python.org/pypi/python-crontab/ 

