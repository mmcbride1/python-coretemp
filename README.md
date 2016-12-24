# python-coretemp

Application to monitor system CPU core temperature. This application is meant to run on Linux RedHat and Debian systems, though thus far IT HAS ONLY BEEN TESTED AND VALIDATED ON CentOS 5.6, 6.6 and 7-7.1 systems. 

# Overview 

The `python-coretemp` package provides `coretemp-monitor`, a very simple daemon that works with `lm_sensors` to monitor CPU core tempurature. The service performs two primary functions:

1. Check the CPU core temperature on a recurrent interval provided by the administrator and keep a log file of the collected results for hindsight analysis.    

2. Alert the administrator via email when ever the core temperature exceeds a given value, which is referred to as a 'threshold'. The context of the thresholds mimic that given by the `lm_sensors` package, that is, it defines a value that represents a *high* core temperature and a value that represents a *critical* core temperature. Any readings that are not deemed as *high* or *critical* are considered *normal*, though these values will still be collected and logged.   

# Dependencies    

`python-coretemp` requires two system packages to run normally:

1. `lm_sensors`

2. `sendmail`    

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
sudo pip install coretemp    
```
The process (when started) should run out of the box. The reason `python-coretemp` needs `sudo` is because it copies the `coretemp.properties` file to the `/etc` directory, and writes log files to `/var/log` and a pid file to `/var/run`.. as do conventional daemon processes that are meant to be invoked at lower levels of the system. The process performs NO other actions root, as it is a non-invasive process.  

# Usage

The application runs as a daemon, and polls on a configured schedule (with a default value of every 5 minutes). The general usage is:

```
sudo coretemp-monitor {start|stop|restart|status}
```
To start the daemon on boot, add the following to the `/etc/rc.d/rc.local` file:

```
coretemp-monitor start
```

# Logging

The following outlines the information kept by the monitoring process:

1. `/var/log/coretemp.log` - This is the polling log, recording sensor query information on an interval that is either the default (every 5 minutes), or on an interval configured by the administrator. On a two core processor, the entry would resemble the following (if on a 2 minute schedule):

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

2. `/var/log/coretemp_error.log` - Records any exception/error perpetuated by the coretemp polling/notification process. Examples may be bad confiuration, mail server connection issues, etc. This file must be manually recycled. 

3. `/tmp/coretemp-daemon` - Records any exception/error perpetuated on the level of the *daemon*.

# Alerts

The monitoring process alerts via email whenever CPU temperature exceeds a certain threshold. By default, the process sends this information using the local mail server on the host machine via the root user (similar to that of processes like yum-cron, or httpd), but may be configured to distribute from any user account via any server as long as the action is permissible. The reason for this approach is to keep the process simple and lightweight, but may of course have shortcomings due to the increasingly demanding traffic restrictions and authentication requirements of more popular mail servers.  The `coretemp-monitor` does not support the use of email servers that require authentication credentials in this version. However, such a feature will be provided in a future release. Therefore, it is important that the host running the monitoring process does so under a network allowing SMTP traffic over port 25 or, if outgoing traffic on port 25 is not supported, that the monitoring process works with a mail server that may accept incoming traffic over alternatively configured ports. This used to be a very simple procedure, but has become increasingly difficult with new authentication requirements.     

# Configuration

When updating the configuration, use:    

```
sudo coretemp-monitor restart
```

The process configuration file is called `coretemp.properties` and lives in the `/etc/` directory. This file may be editied by the administrator to define the behavior of three primary sets of attributes:

## alerts

This section handles the emailing specifics:

1. `fr_email` -> Default: `root@localhost`. The account from which to send the email alert.

2. `to_email` -> Default: `root@localhost`. A comma separated list of email addresses which to send the alert. (ex. me@gamil.com,you@gmail.com)

## threshold 

This section defines the what the administrator will consider *high* and *critical* CPU core temperature values. If these values are `<0` or absent, the process will use the recommended thresholds provided by `lm_sensors`. 

1. `high` -> Default: `-1`: The temperature (degrees celsius) at which the core temperature should be considered *high*.

2. `crit` -> Default: `-1`: The temperature (degrees celsius) at which the core temperature should be considered *critical*. 

## poll        

This section defines the polling interval at which the process should check and report the state of the CPU. 
1. `interval` -> Default `300`: The amount of time (in seconds) the process should yield between each poll.    

# Bug Reports

Issues and bugs are taken seriously and handled propmptly. Please send reports to switchnotifier@gmail.com.
