#!/usr/bin/env python3

# SCAN script
# Author: Yufan Chen
# Please modify the according parameters_COMMAND-TYPE.txt file for the parameters as you need
# In the terminal, type in "chmod +x scan.py" 
# Then execute with "./scan.py"

import sys
import tkinter as tk
import time
import utils as u
import subprocess
from ctypes import cdll

beam = 'pcrexHallA_beam_current' #'hac_bcm_average'
RHWP_set = 'psub_pl_ipos'
RHWP_read = 'psub_pl_pos'
PITA1_set = 'RTPPITA1CNTSET' 
PITA1_read = 'RTPPITA1CNT'
PITA2_set = 'RTPPITA2CNTSET' 
PITA2_read = 'RTPPITA2CNT'
DAC03_set = 'C1068_QDAC03'
DAC03_read = 'C1068_QDAC03r.RVAL'
DAC04_set = 'C1068_QDAC04'
DAC04_read = 'C1068_QDAC04r.RVAL'
DAC05_set = 'C1068_QDAC05'
DAC05_read = 'C1068_QDAC05r.RVAL'
DAC06_set = 'C1068_QDAC06'
DAC06_read = 'C1068_QDAC06r.RVAL'
DAC11_set = 'C1068_QDAC11'
DAC11_read = 'C1068_QDAC11r.RVAL'
DAC12_set = 'C1068_QDAC12'
DAC12_read = 'C1068_QDAC12r.RVAL'
DAC13_set = 'C1068_QDAC13'
DAC13_read = 'C1068_QDAC13r.RVAL'
DAC14_set = 'C1068_QDAC14'
DAC14_read = 'C1068_QDAC14r.RVAL'
aposu_set = 'RTPAPOSUCNTSET'
aposu_read = 'RTPAPOSUCNT'
aposv_set = 'RTPAPOSVCNTSET'
aposv_read = 'RTPAPOSVCNT'
APPLY = 'RTPDACSETCMD'
COMMAND_SCAN = 5000
# Command: 
# SCAN_GET_DATA, SCAN_SET_DATA, SCAN_GET_STATUS, SCAN_SET_STATUS
command = [1001,1002,1003,1004]
# wait_time = 5 # seconds

def set_unclean(crate):
  err = open('error.txt','w+')
  err.write('====== error ======\n')

  unclean_packet = [COMMAND_SCAN, command[3],0,0,0,"SCN Status Change","Y"]
  err_flag, reply = u.send_command(crate, unclean_packet)
  if err_flag == u.SOCK_OK:
    log_message = 'SCAN status changed to NOT CLEAN(0)\n'
    print('SCAN status changed to NOT CLEAN(0)\n')
  else:
    err.write('Could not access socket.\n')
    print('Something went wrong! Check the error.txt file.\n')
    sys.exit()

  err.close()
  return(log_message)

def set_clean(crate):
  err = open('error.txt','w+')
  err.write('====== error ======\n')

  clean_packet = [COMMAND_SCAN, command[3],1,0,0,"SCN Status Change","Y"]
  err_flag, reply = u.send_command(crate, clean_packet)
  if err_flag == u.SOCK_OK: 
    log_message = 'SCAN status changed to CLEAN(1)\n'
    print('SCAN status changed to CLEAN(1)\n')
  else:
    err.write('Could not access socket.\n')
    print('Something went wrong! Check the error.txt file.\n')
    sys.exit()

  err.close()
  return(log_message)

def get_value(crate, num):
  err = open('error.txt','w+')
  err.write('====== error ======\n')

  packet = [COMMAND_SCAN, command[0],num,0,0,"Check SCN Data Value","Y"]
  err_flag, reply = u.send_command(crate, packet)
  if err_flag == u.SOCK_OK:
    origin = int(reply[3])
    log_message = 'The set point value of scandata' + str(num) + ' is ' + str(origin) + ' \n'
    print('The set point value of scandata' + str(num) + ' is ' + str(origin) + ' \n')
  else:
    err.write('Could not access socket.\n')
    print('Something went wrong! Check the error.txt file.\n')
    sys.exit()  

  err.close()
  return(origin, log_message)

def set_value(setpoint, crate, num):
  err = open('error.txt','w+')
  err.write('====== error ======\n')  

  packet = [COMMAND_SCAN, command[1],num,setpoint,0,"Set SCN Data Value","Y"]
  err_flag, reply = u.send_command(crate, packet)
  if err_flag == u.SOCK_OK:
    log_message = 'Wrote new SCAN set point ' + str(setpoint) + ' to scandata' + str(num) + '\n'
    print('Wrote new SCAN set point ' + str(setpoint) + ' to scandata' + str(num) + '\n')
  else:
    err.write('Could not access socket.\n')
    print('Something went wrong! Check the error.txt file.\n')
    sys.exit()

  err.close()
  return(log_message)

def caput(value, epics_var):
  err = open('error.txt','w+')
  err.write('====== error ======\n')

  feedback = subprocess.Popen(['caput',epics_var,value], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  B = feedback.rstrip().split(" ")
  if B[0] == 'Old':
    log_message = feedback + '\nWrote SCAN set point ' + value + ' to EPICS variable ' + epics_var + '\n'
    print(feedback + '\nWrote SCAN set point ' + value + ' to EPICS variable ' + epics_var + '\n')
  else:
    err.write(feedback + '\n')
    print('Something went wrong! Check the error.txt file.\n')
    sys.exit()

  err.close()
  return(log_message)

def waiting(current,wait_time,crate):
  log_message = ''
  j = 0
  t = wait_time
  time.sleep(20)
  if float(subprocess.Popen(['caget', '-t', beam], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii'))<3:
    while float(subprocess.Popen(['caget', '-t', beam], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii'))<(current-3):
      time.sleep(1)
    time.sleep(10)
    j = j+1
  # set clean
  log_message += set_clean(crate)
  while t>0:
    if float(subprocess.Popen(['caget', '-t', beam], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii'))<3:
      log_message += set_unclean(crate)
      while float(subprocess.Popen(['caget', '-t', beam], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii'))<(current-3):
        time.sleep(1)
      time.sleep(10)
      t = wait_time
      j = j+1
      time.sleep(1)
      log_message += set_clean(crate)
    else:
      time.sleep(1)
      t = t-1
  if j == 0:
    log_message += ('No beam lost.\n')
  else:
    log_message += ('Lost the beam ' + str(j) + ' time/times\n')
    print('Lost the beam ' + str(j) + ' time/times\n')
  if wait_time >= 60:
    log_message += ('waited for ' + str(wait_time/60) + ' minutes\n\n')
    print('waited for ' + str(wait_time/60) + ' minutes\n\n')
  else:
    log_message += ('waited for ' + str(wait_time) + ' seconds\n\n')
    print('waited for ' + str(wait_time) + ' seconds\n\n')
  return(log_message)

def scan1(value1, crate, num, value2, epics_set1, epics_read1, epics_set2='none', epics_read2='none', epics_set3='none', epics_read3='none', epics_var4='none', epics_read4='none'):
  # set not clean
  log_message = set_unclean(crate)

  # caput the value to EPICS variable accordingly
  log_message += caput(value2,epics_set1)
  if epics_set2 !='none':
    log_message += caput(value2,epics_set2)
    if epics_set3 != 'none' and epics_set4 != 'none':
      log_message += caput(value2,epics_set3)
      log_message += caput(value2,epics_set4)
    else:
      while subprocess.Popen(['caget', '-t', epics_set1], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') != value2: 
        time.sleep(1)
      while subprocess.Popen(['caget', '-t', epics_set2], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') != value2: 
        time.sleep(1)
      time.sleep(1)
      log_message += caput('1',APPLY)

  while subprocess.Popen(['caget', '-t', epics_read1], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') != value2: 
    log_message += caput('1',APPLY)
    time.sleep(1)
  if epics_read2 != 'none':
    while subprocess.Popen(['caget', '-t', epics_read2], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') != value2: 
      log_message += caput('1',APPLY)
      time.sleep(1)
    if epics_read3 != 'none' and epics_read4 != 'none':
      while subprocess.Popen(['caget', '-t', epics_read3], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') != value2: 
        time.sleep(1)
      while subprocess.Popen(['caget', '-t', epics_read4], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') != value2: 
        time.sleep(1)
  
  # set scandata1 in socket
  log_message += set_value(value1, crate, num)

  return(log_message)


def rhwp_scan():
  i = 0
  f = open('parameters_RHWP.txt','r')
  log = open('log.txt','w+')
  err = open('error.txt','w+')
  err.write('====== error ======\n')

  for line in f.readlines():
    if i == 0:
      A = line.rstrip().split(" ")
      if int(A[1]) == 1 or int(A[1]) == 3:
        crate = int(A[1])
        if int(A[3]) > 0:
          wait_time = int(A[3])
        else:
          err.write('Wait_time MUST be positive!!\n')
          print('Something went wrong! Check the error.txt file.\n')
          sys.exit()
      else:
        err.write('Wrong Crate Number!!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    elif i == 1:
      A = line.split(" ")
      if int(A[1]) > 0 and int(A[1]) <= int(A[3]) and int(A[3]) <= 8000:
        xmin = int(A[1])
        xmax = int(A[3])
        if int(A[5]) > 0 and int(A[5]) <= (xmax - xmin):
          np = int(A[5])
        else:
          err.write('Number of points MUST be positive and smaller than (max - min)!!\n')
          print('Something went wrong! Check the error.txt file.\n')
          sys.exit()
      else:
        err.write('Set point range Must be in between 1 to 8000!!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    elif i == 2:
      A = line.split(" ")
      if int(A[1]) > 0:
        current = int(A[1])
        break
      else:
        err.write('Beam current MUST be positive!!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    i += 1

  f.close()
  err.close()

  if xmin == 1:
    step = xmax/(np-1)
  else:
    step = (xmax - xmin)/(np-1)

  # caget the origin value from EPICS
  xorg = subprocess.Popen(['caget', '-t', RHWP_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log.write('The original value of RHWP is ' + xorg + '\n')

  # get the origin scandata1 from socket
  origin, log_message = get_value(crate, 1)

  for i in range(0,np):
    if i == 0:
      value = xmin
    else:
      if xmin == 1:
        value = int(i*step)
      else:
        value = int(xmin + i*step)
    log_message += scan1(value, crate, 1, str(value), RHWP_set, RHWP_read)
    
    # Wait for wait_time seconds
    log_message += waiting(current,wait_time,crate)

  log_message += scan1(origin, crate, 1, xorg, RHWP_set, RHWP_read)
  log.write(log_message)

  log.write('\nRHWP SCAN finished!\nThanks for using the script!')
  log.close()

  return

def pita_scan():
  
  i = 0
  f = open('parameters_PITA.txt','r')
  log = open('log.txt','w+')
  err = open('error.txt','w+')
  err.write('====== error ======\n')

  for line in f.readlines():
    if i == 0:
      A = line.rstrip().split(" ")
      if int(A[1]) == 1 or int(A[1]) == 3:
        crate = int(A[1])
        if int(A[3]) > 0:
          wait_time = int(A[3])
        else:
          err.write('Wait_time MUST be positive!!\n')
          print('Something went wrong! Check the error.txt file.\n')
          sys.exit()
      else:
        err.write('Wrong Crate Number!!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    elif i == 1:
      A = line.split(" ")
      if int(A[1]) > 0 and int(A[3]) > 0 and int(A[1])*int(A[3]) <= 3000:
        step_size = int(A[1])
        np = int(A[3])
      else:
        err.write('Both step_size and max_step MUST be positive and step_size*max_step MUST be smaller than 3000!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    elif i == 2:
      A = line.split(" ")
      if int(A[1]) > 0:
        current = int(A[1])
        break
      else:
        err.write('Beam current MUST be positive!!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    i += 1

  f.close()

  # get the origin scandata1 from socket
  origin, log_message = get_value(crate, 1)

  # caget the EPICS original value from PITA_1 and PITA_2
  pita1 = subprocess.Popen(['caget', '-t', PITA1_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log_message += 'The original value of PITA1 is ' + pita1 + '\n'
  pita2 = subprocess.Popen(['caget', '-t', PITA2_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log_message += 'The original value of PITA2 is ' + pita2 + '\n'
  if pita1 != pita2:
    err.write('PITA_1 and PITA_2 do not have the same value!!')
    print('Something went wrong! Check the error.txt file.\n')
    sys.exit()
  err.close()

  log_message += set_unclean(crate)
  log_message += set_value(round(float(pita1)), crate, 1)
  log_message += waiting(current,wait_time,crate)
  
  for i in range(1,np+1):
    value = round(float(pita1) + i*step_size)
    log_message += scan1(value, crate, 1, str(value), PITA1_set, PITA1_read, PITA2_set, PITA2_read)
    log_message += waiting(current,wait_time,crate)

    value = round(float(pita1) - i*step_size)
    log_message += scan1(value, crate, 1, str(value), PITA1_set, PITA1_read, PITA2_set, PITA2_read)
    log_message += waiting(current,wait_time,crate)

  log_message += scan1(origin, crate, 1, pita1, PITA1_set, PITA1_read, PITA2_set, PITA2_read)
  log.write(log_message)
  
  log.write('\nPITA SCAN finished!\nThanks for using the script!')
  log.close()
  return

def aia_scan():
  
  i = 0
  f = open('parameters_AIA.txt','r')
  log = open('log.txt','w+')
  err = open('error.txt','w+')
  err.write('====== error ======\n')

  for line in f.readlines():
    if i == 0:
      A = line.rstrip().split(" ")
      if int(A[1]) == 1 or int(A[1]) == 3:
        crate = int(A[1])
        if int(A[3]) > 0:
          wait_time = int(A[3])
        else:
          err.write('Wait_time MUST be positive!!\n')
          print('Something went wrong! Check the error.txt file.\n')
          sys.exit()
      else:
        err.write('Wrong Crate Number!!\n')
        sys.exit()
    elif i == 1:
      A = line.split(" ")
      if int(A[1]) > 0 and int(A[3]) > 0:
        step_size = int(A[1])
        np = int(A[3])
      else:
        err.write('Both step_size and max_step MUST be positive!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    elif i == 2:
      A = line.split(" ")
      if int(A[1]) > 0:
        current = int(A[1])
        break
      else:
        err.write('Beam current MUST be positive!!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    i += 1

  f.close()

  # get the origin scandata1 from socket
  origin, log_message = get_value(crate, 1)

  # caget the EPICS original value from DAC03,DAC04,DAC05,DAC06
  dac03 = subprocess.Popen(['caget', '-t', DAC03_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log_message += 'The original value of DAC03 is ' + dac03 + '\n'
  dac04 = subprocess.Popen(['caget', '-t', DAC04_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log_message += 'The original value of DAC04 is ' + dac04 + '\n'
  dac05 = subprocess.Popen(['caget', '-t', DAC05_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log_message += 'The original value of DAC05 is ' + dac05 + '\n'
  dac06 = subprocess.Popen(['caget', '-t', DAC06_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log_message += 'The original value of DAC06 is ' + dac06 + '\n'
  if dac03 != dac04 or dac04 != dac05 or dac05 != dac06:
    err.write('DAC03, DAC04, DAC05 and DAC06 do not have the same value!!')
    print('Something went wrong! Check the error.txt file.\n')
    sys.exit()
  err.close()

  log_message += set_unclean(crate)
  log_message += set_value(int(dac03), crate, 1)
  log_message += waiting(current,wait_time,crate)
  
  for i in range(1,np+1):
    value = int(int(dac03) + i*step_size)
    log_message += scan1(value, crate, 1, str(value), DAC03_set, DAC03_read, DAC04_set, DAC04_read, DAC05_set, DAC05_read, DAC06_set, DAC06_read)
    log_message += waiting(current,wait_time,crate)

    value = int(int(dac03) - i*step_size)
    log_message += scan1(value, crate, 1, str(value), DAC03_set, DAC03_read, DAC04_set, DAC04_read, DAC05_set, DAC05_read, DAC06_set, DAC06_read)
    log_message += waiting(current,wait_time,crate)

  log_message += scan1(origin, crate, 1, dac03, DAC03_set, DAC03_read, DAC04_set, DAC04_read, DAC05_set, DAC05_read, DAC06_set, DAC06_read)
  log.write(log_message)

  log.write('\nAIA SCAN finished!\nThanks for using the script!')
  log.close()
  return

def cia_scan():
  
  i = 0
  f = open('parameters_CIA.txt','r')
  log = open('log.txt','w+')
  err = open('error.txt','w+')
  err.write('====== error ======\n')

  for line in f.readlines():
    if i == 0:
      A = line.rstrip().split(" ")
      if int(A[1]) == 1 or int(A[1]) == 3:
        crate = int(A[1])
        if int(A[3]) > 0:
          wait_time = int(A[3])
        else:
          err.write('Wait_time MUST be positive!!\n')
          print('Something went wrong! Check the error.txt file.\n')
          sys.exit()
      else:
        err.write('Wrong Crate Number!!\n')
        sys.exit()
    elif i == 1:
      A = line.split(" ")
      if int(A[1]) > 0 and int(A[3]) > 0:
        step_size = int(A[1])
        np = int(A[3])
      else:
        err.write('Both step_size and max_step MUST be positive!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    elif i == 2:
      A = line.split(" ")
      if int(A[1]) > 0:
        current = int(A[1])
        break
      else:
        err.write('Beam current MUST be positive!!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    i += 1

  f.close()

  # get the origin scandata1 from socket
  origin, log_message = get_value(crate, 1)

  # caget the EPICS original value from DAC11,DAC12,DAC13,DAC14
  dac11 = subprocess.Popen(['caget', '-t', DAC11_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log_message += 'The original value of DAC11 is ' + dac11 + '\n'
  dac12 = subprocess.Popen(['caget', '-t', DAC12_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log_message += 'The original value of DAC12 is ' + dac12 + '\n'
  dac13 = subprocess.Popen(['caget', '-t', DAC13_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log_message += 'The original value of DAC13 is ' + dac13 + '\n'
  dac14 = subprocess.Popen(['caget', '-t', DAC14_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log_message += 'The original value of DAC14 is ' + dac14 + '\n'
  if dac11 != dac12 or dac12 != dac13 or dac13 != dac14:
    err.write('DAC11, DAC12, DAC13 and DAC14 do not have the same value!!')
    print('Something went wrong! Check the error.txt file.\n')
    sys.exit()
  err.close()

  log_message += set_unclean(crate)
  log_message += set_value(int(dac11), crate, 1)
  log_message += waiting(current,wait_time,crate)
  
  for i in range(1,np+1):
    value = int(int(dac11) + i*step_size)
    log_message += scan1(value, crate, 1, str(value), DAC11_set, DAC11_read, DAC12_set, DAC12_read, DAC13_set, DAC13_read, DAC14_set, DAC14_read)
    log_message += waiting(current,wait_time,crate)

    value = int(int(dac11) - i*step_size)
    log_message += scan1(value, crate, 1, str(value), DAC11_set, DAC11_read, DAC12_set, DAC12_read, DAC13_set, DAC13_read, DAC14_set, DAC14_read)
    log_message += waiting(current,wait_time,crate)

  log_message += scan1(origin, crate, 1, dac11, DAC11_set, DAC11_read, DAC12_set, DAC12_read, DAC13_set, DAC13_read, DAC14_set, DAC14_read)
  log.write(log_message)

  log.write('\nCIA SCAN finished!\nThanks for using the script!')
  log.close()
  return

def aposv_scan():
  
  i = 0
  f = open('parameters_APOSV.txt','r')
  log = open('log.txt','w+')
  err = open('error.txt','w+')
  err.write('====== error ======\n')

  for line in f.readlines():
    if i == 0:
      A = line.rstrip().split(" ")
      if int(A[1]) == 1 or int(A[1]) == 3:
        crate = int(A[1])
        if int(A[3]) > 0:
          wait_time = int(A[3])
        else:
          err.write('Wait_time MUST be positive!!\n')
          print('Something went wrong! Check the error.txt file.\n')
          sys.exit()
      else:
        err.write('Wrong Crate Number!!\n')
        sys.exit()
    elif i == 1:
      A = line.split(" ")
      if int(A[1]) > 0 and int(A[3]) > 0:
        step_size = int(A[1])
        np = int(A[3])
      else:
        err.write('Both step_size and max_step MUST be positive!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    elif i == 2:
      A = line.split(" ")
      if int(A[1]) > 0:
        current = int(A[1])
        break
      else:
        err.write('Beam current MUST be positive!!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    i += 1

  f.close()

  # get the origin scandata1 from socket
  origin, log_message = get_value(crate, 1)

  # caget the EPICS original value from APOSV
  aposv = subprocess.Popen(['caget', '-t', aposv_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log_message += 'The original value of APOSV is ' + aposv + '\n'
  err.close()

  log_message += set_unclean(crate)
  log_message += set_value(int(aposv), crate, 1)
  log_message += waiting(current,wait_time,crate)
  
  for i in range(1,np+1):
    value = int(int(aposv) + i*step_size)
    log_message += scan1(value, crate, 1, str(value), aposv_set, aposv_read)
    while subprocess.Popen(['caget', '-t', aposv_set], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') != value: 
      time.sleep(1)
    time.sleep(1)
    log_message += caput('1',APPLY)
    log_message += waiting(current,wait_time,crate)

    value = int(int(aposv) - i*step_size)
    log_message += scan1(value, crate, 1, str(value), aposv_set, aposv_read)
    while subprocess.Popen(['caget', '-t', aposv_set], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') != value: 
      time.sleep(1)
    time.sleep(1)
    log_message += caput('1',APPLY)
    log_message += waiting(current,wait_time,crate)

  log_message += scan1(origin, crate, 1, aposv, aposv_set, aposv_read)
  log.write(log_message)

  log.write('\nAPOSV SCAN finished!\nThanks for using the script!')
  log.close()
  return

def aposu_scan():
  
  i = 0
  f = open('parameters_APOSU.txt','r')
  log = open('log.txt','w+')
  err = open('error.txt','w+')
  err.write('====== error ======\n')

  for line in f.readlines():
    if i == 0:
      A = line.rstrip().split(" ")
      if int(A[1]) == 1 or int(A[1]) == 3:
        crate = int(A[1])
        if int(A[3]) > 0:
          wait_time = int(A[3])
        else:
          err.write('Wait_time MUST be positive!!\n')
          print('Something went wrong! Check the error.txt file.\n')
          sys.exit()
      else:
        err.write('Wrong Crate Number!!\n')
        sys.exit()
    elif i == 1:
      A = line.split(" ")
      if int(A[1]) > 0 and int(A[3]) > 0:
        step_size = int(A[1])
        np = int(A[3])
      else:
        err.write('Both step_size and max_step MUST be positive!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    elif i == 2:
      A = line.split(" ")
      if int(A[1]) > 0:
        current = int(A[1])
        break
      else:
        err.write('Beam current MUST be positive!!\n')
        print('Something went wrong! Check the error.txt file.\n')
        sys.exit()
    i += 1

  f.close()

  # get the origin scandata1 from socket
  origin, log_message = get_value(crate, 1)

  # caget the EPICS original value from APOSU
  aposu = subprocess.Popen(['caget', '-t', aposu_read], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii')
  log_message += 'The original value of APOSU is ' + aposu + '\n'
  err.close()

  log_message += set_unclean(crate)
  log_message += set_value(int(aposu), crate, 1)
  log_message += waiting(current,wait_time,crate)
  
  for i in range(1,np+1):
    value = int(int(aposu) + i*step_size)
    log_message += scan1(value, crate, 1, str(value), aposu_set, aposu_read)
    while subprocess.Popen(['caget', '-t', aposu_set], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') != value: 
      time.sleep(1)
    time.sleep(1)
    log_message += caput('1',APPLY)
    log_message += waiting(current,wait_time,crate)

    value = int(int(aposu) - i*step_size)
    log_message += scan1(value, crate, 1, str(value), aposu_set, aposu_read)
    while subprocess.Popen(['caget', '-t', aposu_set], stdout=subprocess.PIPE).stdout.read().strip().decode('ascii') != value: 
      time.sleep(1)
    time.sleep(1)
    log_message += caput('1',APPLY)
    log_message += waiting(current,wait_time,crate)

  log_message += scan1(origin, crate, 1, aposu, aposu_set, aposu_read)
  log.write(log_message)

  log.write('\nAPOSU SCAN finished!\nThanks for using the script!')
  log.close()
  return
