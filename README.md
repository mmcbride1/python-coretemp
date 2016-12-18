# python-coretemp
Application to monitor system CPU core temperature. This application is meant to run on Linux RedHat and Debian systems, though thus far IT HAS ONLY BEEN TESTED AND VALIDATED ON CentOS 5.6, 6.6 and 7-7.1 systems. 

# Overview 
The `python-coretemp` package provides `coretemp-monitor`, a very simple, lightweight daemon that works with `lm_sensors` to monitor CPU core tempurature. The service performs two primary functions:

1.) Check the CPU core temperature on a recurrent interval provided by the administrator and keep a log file of the collected results for hindsight analysis.    

2.) Alert the administrator via email when ever the core temperature exceeds a given value, which is referred to as a 'threshold'. The context of the thresholds mimic that given by the `lm_sensors` package, that is, it defines a value that represents a *high* core temperature and a value that represents a *critical* core temperature. Any readings that are not deemed as *high* or *critical* are considered *normal*, though these values will still be collected and logged.   

# Dependencies    
`python-coretemp` requires two system packages to run normally:

1.) lm_sensors
2.) sendmail

Please ensure these dependencies are present on the system before installing `python-coretemp`. You may install them via:

RedHat
```
sudo yum install lm_sensors
sudo yum install sendmail
```
Debain
```
sudo apt-get install lm-sensors
sudo apt-get install sendmail
```

# Installation

`python-coretemp` may be installed via pip. Specifically:

```
sudo pip install python-coretemp
```
The process (when started) should run out of the box. The reason `python-coretemp` needs `sudo` is because it copies the `coretemp.properties` file to the `/etc` directory, and writes log files to `/var/log` and a pid file to `/var/run`.. as do conventional daemon processes that are meant to be separated from the context of individual user. The process performs NO other actions root, as it is a non-invasive process.  

# Usage

The application runs as a daemon, and polls on a configured schedule (but does include a default). The general usage is:

```
sudo coretemp-monitor {start|stop|restart|status}
```

# Logging

The following outlines the information kept by the monitoring process:

1.) `/var/log/coretemp.log` - This is the polling log, recording sensor query information on an interval that is either the default (every 5 minutes), or on an interval configured by the administrator. On a two core processor, the entry would resemble the following (if on a 2 minute schedule):

```
2016-12-17 22:13:37.966300 - coretemp-reading :
Core 0 : 35.0 -> NORMAL
Core 1 : 35.0 -> NORMAL

Core Mean: 35.0
===============================================
2016-12-17 22:11:37.864308 - coretemp-reading :
Core 0 : 72.0 -> CRITICAL!
Core 1 : 73.0 -> CRITICAL!

Core Mean: 72.5
===============================================
```
This file will be recycled when reaching a size of 1 MB. The ability to choose an expanded recycle interval and also archive coretemp log files will be available in the next release.    

2.) `/var/log/coretemp_error.log` - Records any exception/error perpetuated by the coretemp polling/notification process. Examples may be bad confiuration, mail server connection issues, etc. This file must be manually recycled. 

3.) `/tmp/coretemp-daemon` - Records any exception/error perpetuated by the *daemon*
