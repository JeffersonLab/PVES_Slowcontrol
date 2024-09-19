#!/usr/bin/env python3

# SCAN script

# Please modify the "parameters.txt" file for the parameters you need
# In the terminal, type in "chmod +x scan.py" 
# Then execute with "./scan.py"

def g(a,b,c='NONE',d='NONE'):
  if c != 'NONE' and d != 'NONE':
    x = a + b + c + d
  else:
    x = a + b
  return(x)

print(g(1,2,3,4))

