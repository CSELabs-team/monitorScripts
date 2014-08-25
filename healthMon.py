#!/usr/bin/python

#1. Write a python script to detect system disk, cpu, memory usage in Linux OS.
#2. When it reachs 90% warn, 95% critical, and the script will send an email alert to cselabs-team-group mailing list.

#I plan to pair this with a healthMon.cfg file which will hold the following configuration:
#server name (to be read into serverName variable)
#list of disk devices (to be read into devices variable)
#more to be added later if needed

import subprocess
#to run commands

from email.mime.text import MIMEText
import email.utils
import smtplib
#for email

serverName = "test.local"
devices = ["/dev/sda1", "BLOOD"]
#these two lines are temporary.

def sendAlert(alertLevel = "info", addr = "cselabs-team-group@nyu.edu", sender = "healthMon@"+serverName, subject = "default subject", content = "default content"):
    msg = MIMEText(content)
    msg["Subject"] = "***" + alertLevel + "*** " + serverName + ": " + subject  #example: ***info*** test.local: default subject
    msg["Message-id"] = email.utils.make_msgid()
    msg["From"] = sender
    msg["To"] = addr
    print "Connecting"###
    server = smtplib.SMTP("smtp.gmail.com")
    print "Initializing send"###
    server.sendmail(sender, addr, msg.as_string())
    print "Sent"###
    server.quit()
    print "Server quit"###

#sendAlert(subject = "test", content = "Test email, please ignore")

def checkDisk(device): ###device variable validation code should be before this function is called###
    df = subprocess.Popen(["df", device], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
    if int(percent.replace("%", "")) >= 95:
        sendAlert(alertLevel = "critical", \
                    subject = "disk usage above 95%", \
                    content = "Alert: disk usage in " + serverName + " is now " + percent)
    elif int(percent.replace("%", "")) >= 90:
        sendAlert(alertLevel = "warning", \
                    subject = "disk usage above 90%", \
                    content = "Alert: disk usage in " + serverName + " is now " + percent)
    #print "disk size is ", size

def checkCpuRam():
    top = subprocess.Popen(["top", "-b", "-p 1", "-n 1"], stdout=subprocess.PIPE)
    output = top.communicate()[0]
    _, _, cpuLine, memLine, swpLine, _ = output.split('\n', 5)
    cpuUsedPercent = str(100.0 - float(cpuLine.split()[7]))    #cpuLine.split()[7] contains the %idle value
    if float(cpuUsedPercent) >= 95:
        sendAlert(alertLevel = "critical", \
                    subject = "CPU usage above 95%", \
                    content = "Alert: CPU usage in " + serverName + " is now " + cpuUsedPercent + "%")
    elif float(cpuUsedPercent) >= 90:
        sendAlert(alertLevel = "warning", \
                    subject = "CPU usage above 90%", \
                    content = "Alert: CPU usage in " + serverName + " is now " + cpuUsedPercent + "%")
        
    _, _, memTotal, _, memUsed, _, memFree, _, _, _ = memLine.split()
    memUsedPercent = str(float(memUsed)*100/float(memTotal))
    if float(memUsedPercent) >= 95:
        sendAlert(alertLevel = "critical", \
                    subject = "Memory usage above 95%", \
                    content = "Alert: memory usage in " + serverName + " is now " + memUsedPercent + "%")
    elif float(memUsedPercent) >= 90:
        sendAlert(alertLevel = "warning", \
                    subject = "Memory usage above 90%", \
                    content = "Alert: memory usage in " + serverName + " is now " + memUsedPercent + "%")
    ###not worried about swap, so not using swpLine for now###
