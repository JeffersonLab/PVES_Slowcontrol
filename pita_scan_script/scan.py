#!/usr/bin/env python3

# SCAN script
# Author: Yufan Chen
# Please modify the "parameters.txt" file for the parameters as you need
# In the terminal, type in "chmod +x scan.py" 
# Then execute with "./scan.py"

import sys
import tkinter as tk
import time
import utils as u
import subprocess
import scan_para as p
from ctypes import cdll

if len(sys.argv) == 2:
  if sys.argv[1] == 'rhwp' or sys.argv[1] == "rhwp" or sys.argv[1] == "RHWP" or sys.argv[1] == 'RHWP':
    p.rhwp_scan()
    print(sys.argv[1] + ' SCAN finished\nThanks for using the script!')
  elif sys.argv[1] == 'pita' or sys.argv[1] == "pita" or sys.argv[1] == "PITA" or sys.argv[1] == 'PITA':
    p.pita_scan()
    print(sys.argv[1] + ' SCAN finished\nThanks for using the script!')
  elif sys.argv[1] == 'aia' or sys.argv[1] == "aia" or sys.argv[1] == "AIA" or sys.argv[1] == 'AIA':
    p.aia_scan()
    print(sys.argv[1] + ' SCAN finished\nThanks for using the script!')
  elif sys.argv[1] == 'cia' or sys.argv[1] == "cia" or sys.argv[1] == "CIA" or sys.argv[1] == 'CIA':
    p.aia_scan()
    print(sys.argv[1] + ' SCAN finished\nThanks for using the script!')
  elif sys.argv[1] == 'aposv' or sys.argv[1] == "aposv" or sys.argv[1] == "APOSV" or sys.argv[1] == 'APOSV':
    p.aposv_scan()
    print(sys.argv[1] + ' SCAN finished\nThanks for using the script!')
  elif sys.argv[1] == 'aposu' or sys.argv[1] == "aposu" or sys.argv[1] == "APOSU" or sys.argv[1] == 'APOSU':
    p.aposu_scan()
    print(sys.argv[1] + ' SCAN finished\nThanks for using the script!')
  else:
    print('Cannot recognize command type!')
else:
  print('Please specify SCAN type !')

