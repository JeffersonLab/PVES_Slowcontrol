import subprocess
import timeit

class pycaFFB:
        def __init__(self):
                ''' Constructor for this class. '''
                # Create some members

        def cagetFFB_modState():
                p1 = subprocess.Popen(["caget","-t","BEAMMODSWITCH"], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                (outputp1, errorp1) = p1.communicate()
                output = outputp1.decode('utf-8')
                #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                #status = p1.returncode
                if "Invalid" in output:
                        status = -1
                else:
                        status = 0

                if "OFF" in output:
                        bmodstate = 0
                else:
                        bmodstate = 1
                
                print ('cagetFFB_modstate(): {}' .format(output))
                return (bmodstate,status)

        #get the WAVESTATE
        # OFF_STATE      0
        # CONFIG_STATE   1
        # TRIGGER_STATE  2
        # TEST_STATE     3
        def cagetFFB_waveState(chAlias):
                wavestates = {
                        1:"BMOD1:CHAN0:WAVESTATE",
                        2:"BMOD1:CHAN1:WAVESTATE",
                        3:"BMOD1:CHAN2:WAVESTATE",
                        4:"BMOD1:CHAN3:WAVESTATE",
                        5:"BMOD2:CHAN0:WAVESTATE",
                        6:"BMOD2:CHAN1:WAVESTATE",
                        7:"BMOD2:CHAN2:WAVESTATE",
                        8:"BMOD2:CHAN3:WAVESTATE"
                }
                chName = wavestates.get(chAlias,"BMOD1:CHAN0:WAVESTATE")
                p2 = subprocess.Popen(["caget","-t",chName], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                (outputp1,errorp1) = p2.communicate()
                output = outputp1.decode('utf-8')
                #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                #status = p1.returncode
                if "Invalid" in output:
                        status = -1
                else:
                        status = 0
                        
                if "OFF" in output:
                        bmodstate = 0
                elif "CONFIG" in output:
                        bmodstate = 1
                elif "TRIGGER" in output:
                        bmodstate = 2
                elif "TEST" in output:
                        bmodstate = 3       
                else:
                        bmodstate = -1
                        
                print ('cagetFFB_waveState(): {}={}' .format(chName,output))
                return(bmodstate,status)
        
        def cagetFFB_freq(chAlias):
                freqs = {
                        1:"BMOD1:CHAN0:FREQUENCY",
                        2:"BMOD1:CHAN1:FREQUENCY",
                        3:"BMOD1:CHAN2:FREQUENCY",
                        4:"BMOD1:CHAN3:FREQUENCY",
                        5:"BMOD2:CHAN0:FREQUENCY",
                        6:"BMOD2:CHAN1:FREQUENCY",
                        7:"BMOD2:CHAN2:FREQUENCY",
                        8:"BMOD2:CHAN3:FREQUENCY"
                }
                chName = freqs.get(chAlias,"BMOD1:CHAN0:FREQUENCY")
                p2 = subprocess.Popen(["caget","-t",chName], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                (outputp1,errorp1) = p2.communicate()
                output = outputp1.decode('utf-8')
                #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                #status = p1.returncode
                if "Invalid" in output:
                        status = -1
                else:
                        status = 0
                                
                print ('cagetFFB_Freq(): {}={}' .format(chName,output))
                return(output,status)
                                
        # get the amplitude of the SINEWAVE
        def cagetFFB_amp(chAlias):        
        
                amps = {
                        1:"BMOD1:CHAN0:AMPLITUDE",
                        2:"BMOD1:CHAN1:AMPLITUDE",
                        3:"BMOD1:CHAN2:AMPLITUDE",
                        4:"BMOD1:CHAN3:AMPLITUDE",
                        5:"BMOD2:CHAN0:AMPLITUDE",
                        6:"BMOD2:CHAN1:AMPLITUDE",
                        7:"BMOD2:CHAN2:AMPLITUDE",
                        8:"BMOD2:CHAN3:AMPLITUDE"
                }
                chName = amps.get(chAlias,"BMOD1:CHAN0:AMPLITUDE")
                p2 = subprocess.Popen(["caget","-t",chName], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                (outputp1,errorp1) = p2.communicate()
                output = outputp1.decode('utf-8')
                #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                #status = p1.returncode
                if "Invalid" in output:
                        status = -1
                else:
                        status = 0
                        
                print ('cagetFFB_amp(): {}={}' .format(chName,output))
                return(output,status)
                        
        #get the number of SINEWAVE periods
        def cagetFFB_period(chAlias):        
                
                amps = {
                        1:"BMOD1:CHAN0:RCRINPUT",
                        2:"BMOD1:CHAN1:RCRINPUT",
                        3:"BMOD1:CHAN2:RCRINPUT",
                        4:"BMOD1:CHAN3:RCRINPUT",
                        5:"BMOD2:CHAN0:RCRINPUT",
                        6:"BMOD2:CHAN1:RCRINPUT",
                        7:"BMOD2:CHAN2:RCRINPUT",
                        8:"BMOD2:CHAN3:RCRINPUT"
                }
                chName = amps.get(chAlias,"BMOD1:CHAN0:RCRINPUT")
                p2 = subprocess.Popen(["caget","-t",chName], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                (outputp1,errorp1) = p2.communicate()
                output = outputp1.decode('utf-8')
                #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                #status = p1.returncode
                if "Invalid" in output:
                        status = -1
                else:
                        status = 0
                
                print ('cagetFFB_period(): {}={}' .format(chName,output))
                return(output,status)

        #check whether or not the SINEWAVE has been loaded two states: enables or disabled
        def cagetFFB_load(chAlias):        

                amps = {
                        1:"BMOD1:CHAN0:SINEWAVE",
                        2:"BMOD1:CHAN1:SINEWAVE",
                        3:"BMOD1:CHAN2:SINEWAVE",
                        4:"BMOD1:CHAN3:SINEWAVE",
                        5:"BMOD2:CHAN0:RAMPWAVE",
                        6:"BMOD2:CHAN1:SINEWAVE",
                        7:"BMOD2:CHAN2:SINEWAVE",
                        8:"BMOD2:CHAN3:SINEWAVE"
                }
                chName = amps.get(chAlias,"BMOD1:CHAN0:SINEWAVE")
                p2 = subprocess.Popen(["caget","-t",chName], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                (outputp1,errorp1) = p2.communicate()
                output = outputp1.decode('utf-8')
                #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                #status = p1.returncode
                if "Invalid" in output:
                        status = -1
                else:
                        status = 0
                
                print ('cagetFFB_load(): {}={}' .format(chName,output))
                return(output,status) 

        #get the "Enter Trigger State" state
        # This step is not done in this routine if the "Hardware Trigger" is in initiated state, 
        # settig Trigger State to 1 initiates sine wave outputs
        def cagetFFB_enterTrig(chAlias):        

                trigs = {
                        1:"BMOD1:CHAN0:TRIGSTATEBTN",
                        2:"BMOD1:CHAN1:TRIGSTATEBTN",
                        3:"BMOD1:CHAN2:TRIGSTATEBTN",
                        4:"BMOD1:CHAN3:TRIGSTATEBTN",
                        5:"BMOD2:CHAN0:TRIGSTATEBTN",
                        6:"BMOD2:CHAN1:TRIGSTATEBTN",
                        7:"BMOD2:CHAN2:TRIGSTATEBTN",
                        8:"BMOD2:CHAN3:TRIGSTATEBTN"
                }
                chName = trigs.get(chAlias,"BMOD1:CHAN0:TRIGSTATEBTN")
                p2 = subprocess.Popen(["caget","-t",chName], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                (outputp1,errorp1) = p2.communicate()
                output = outputp1.decode('utf-8')
                #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                #status = p1.returncode
                if "Invalid" in output:
                        status = -1
                else:
                        status = 0
                
                print ('cagetFFB_enterTrig(): {}={}' .format(chName,output))
                return(output,status)

        #get the "Leave Trigger State" state
        #When this state is set to 0, the state will be CONFIG_STATE
        def cagetFFB_leaveTrig(chAlias):        
                
                trigs = {
                        1:"BMOD1:CHAN0:STOPBTN",
                        2:"BMOD1:CHAN1:STOPBTN",
                        3:"BMOD1:CHAN2:STOPBTN",
                        4:"BMOD1:CHAN3:STOPBTN",
                        5:"BMOD2:CHAN0:STOPBTN",
                        6:"BMOD2:CHAN1:STOPBTN",
                        7:"BMOD2:CHAN2:STOPBTN",
                        8:"BMOD2:CHAN3:STOPBTN"
                }
                chName = trigs.get(chAlias,"BMOD1:CHAN0:STOPBTN")
                p2 = subprocess.Popen(["caget","-t",chName], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                (outputp1,errorp1) = p2.communicate()
                output = outputp1.decode('utf-8')
                #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                #status = p1.returncode
                if "Invalid" in output:
                        status = -1
                else:
                        status = 0
                
                print ('cagetFFB_leaveTrig(): {}={}' .format(chName,output))
                return(output,status)

        #get the "Software Trigger" state
        def cagetFFB_Trig(chAlias):        

                trigs = {
                        1:"BMOD1:CHAN0:TRIGBTN",
                        2:"BMOD1:CHAN1:TRIGBTN",
                        3:"BMOD1:CHAN2:TRIGBTN",
                        4:"BMOD1:CHAN3:TRIGBTN",
                        5:"BMOD2:CHAN0:TRIGBTN",
                        6:"BMOD2:CHAN1:TRIGBTN",
                        7:"BMOD2:CHAN2:TRIGBTN",
                        8:"BMOD2:CHAN3:TRIGBTN"
                }
                chName = trigs.get(chAlias,"BMOD1:CHAN0:TRIGBTN")
                p2 = subprocess.Popen(["caget","-t",chName], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                (outputp1,errorp1) = p2.communicate()
                output = outputp1.decode('utf-8')
                #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                #status = p1.returncode
                if "Invalid" in output:
                        status = -1
                else:
                        status = 0
                
                print ('cagetFFB_Trig(): {}={}' .format(chName,output))
                return(output,status)

        #set the Relay for the output from the function generator into DAQ
        def cagetFFB_relay(chAlias):        

                relays = {
                        1:"BMRELAYSET.B0",
                        2:"BMRELAYSET.B2",
                        3:"BMRELAYSET.B4",
                        4:"BMRELAYSET.B6",
                        5:"BMRELAYSET.B8",
                        6:"BMRELAYSET.BA",
                        7:"BMRELAYSET.BC",
                        8:"BMRELAYSET.BE",
                        9:"BMRELAYSET.B1",
                        10:"BMRELAYSET.B3",
                        11:"BMRELAYSET.B5",
                        12:"BMRELAYSET.B7",
                        13:"BMRELAYSET.B9",
                        14:"BMRELAYSET.BB",
                        15:"BMRELAYSET.BD",
                        16:"BMRELAYSET.BF"
                }
                chName = relays.get(chAlias,"BMRELAYSET.B0")
                p2 = subprocess.Popen(["caget","-t",chName], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                (outputp1,errorp1) = p2.communicate()
                output = outputp1.decode('utf-8')
                #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                #status = p1.returncode
                if "Invalid" in output:
                        status = -1
                else:
                        status = 0
                
                print ('cagetFFB_relay(): {}={}' .format(chName,output))
                return(output,status)


        #print(cagetFFB_modState()[0])
        #to calculate the time it take to run a python routine, devide the results by number=10 to get time for single call
        #print(timeit.timeit(cagetFFB_modState,number=10))
        #print(cagetFFB_waveState(0)[0])
        #print(cagetFFB_freq(0)[0])
        #print(cagetFFB_amp(0)[0])
        #print(cagetFFB_period(0)[0])
        #print(cagetFFB_load(0)[0])
        #print(cagetFFB_enterTrig(0)[0])
        #print(cagetFFB_leaveTrig(2)[0])
        #print(cagetFFB_Trig(2)[0])
        #print(cagetFFB_relay(2)[0])




        ######## CAPUT

        #put the Beam Modulation State:: On/Off (1/0)
        def caputFFB_modState(val):
                if val==1 or val ==0:
                        p1 = subprocess.Popen(["caput","BEAMMODSWITCH",str(val)], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                        (outputp1, errorp1) = p1.communicate()
                        print ('caputFFB_modstate() set to {}' .format(val))
                        status = errorp1
                else:
                        print ('caputFFB_modstate() only accept values 1 or 0')
                        status = 1
                        
                        
                return status


        def caputFFB_freq(chAlias,val):
                freqs = {
                        1:"BMOD1:CHAN0:FREQUENCY",
                        2:"BMOD1:CHAN1:FREQUENCY",
                        3:"BMOD1:CHAN2:FREQUENCY",
                        4:"BMOD1:CHAN3:FREQUENCY",
                        5:"BMOD2:CHAN0:FREQUENCY",
                        6:"BMOD2:CHAN1:FREQUENCY",
                        7:"BMOD2:CHAN2:FREQUENCY",
                        8:"BMOD2:CHAN3:FREQUENCY"
                }
                chName = freqs.get(chAlias,"BMOD1:CHAN0:FREQUENCY")
                if val>=10 and val <=250:
                        p2 = subprocess.Popen(["caput",chName,str(val)], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                        (outputp1,errorp1) = p2.communicate()
                        output = outputp1.decode('utf-8')        
                        #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                        print ('caputFFB_freq() set to {}' .format(val))
                        status = errorp1

                else:
                        print ('caputFFB_freq() only accept values 10 to 250')
                        status = 1
  
                return status

                                
        # get the amplitude of the SINEWAVE
        def caputFFB_amp(chAlias,val):        

                amps = {
                        1:"BMOD1:CHAN0:AMPLITUDE",
                        2:"BMOD1:CHAN1:AMPLITUDE",
                        3:"BMOD1:CHAN2:AMPLITUDE",
                        4:"BMOD1:CHAN3:AMPLITUDE",
                        5:"BMOD2:CHAN0:AMPLITUDE",
                        6:"BMOD2:CHAN1:AMPLITUDE",
                        7:"BMOD2:CHAN2:AMPLITUDE",
                        8:"BMOD2:CHAN3:AMPLITUDE"
                }
                chName = amps.get(chAlias,"BMOD1:CHAN0:AMPLITUDE")
                if val>=0 and val <=300:
                        p2 = subprocess.Popen(["caput",chName,str(val)], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                        (outputp1,errorp1) = p2.communicate()
                        output = outputp1.decode('utf-8')
                        #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                        #status = p1.returncode
                        print ('caputFFB_amp() set to {}' .format(val))
                        status = errorp1
                else:
                        print ('caputFFB_amp() only accept values 0 to 300')
                        status = 1
                
                
                return status


                        
        #put the number of SINEWAVE periods
        def caputFFB_period(chAlias,val):        
                amps = {
                        1:"BMOD1:CHAN0:RCRINPUT",
                        2:"BMOD1:CHAN1:RCRINPUT",
                        3:"BMOD1:CHAN2:RCRINPUT",
                        4:"BMOD1:CHAN3:RCRINPUT",
                        5:"BMOD2:CHAN0:RCRINPUT",
                        6:"BMOD2:CHAN1:RCRINPUT",
                        7:"BMOD2:CHAN2:RCRINPUT",
                        8:"BMOD2:CHAN3:RCRINPUT"
                }
                chName = amps.get(chAlias,"BMOD1:CHAN0:RCRINPUT")
                if val>=1 and val <=511:
                        p2 = subprocess.Popen(["caput",chName,str(val)], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                        (outputp1,errorp1) = p2.communicate()
                        output = outputp1.decode('utf-8')
                        #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                        #status = p1.returncode
                        print ('caputFFB_period() set to {}' .format(val))
                        status = errorp1
                else:
                        print ('caputFFB_period() only accept values 1 to 511')
                        status = 1

                return status



        #load/unload the SINEWAVE
        def caputFFB_load(chAlias,val):        

                amps = {
                        1:"BMOD1:CHAN0:SINEWAVE",
                        2:"BMOD1:CHAN1:SINEWAVE",
                        3:"BMOD1:CHAN2:SINEWAVE",
                        4:"BMOD1:CHAN3:SINEWAVE",
                        5:"BMOD2:CHAN0:SINEWAVE",
                        6:"BMOD2:CHAN1:SINEWAVE",
                        7:"BMOD2:CHAN2:SINEWAVE",
                        8:"BMOD2:CHAN3:SINEWAVE"
                }
                chName = amps.get(chAlias,"BMOD1:CHAN0:SINEWAVE")
                if val>=0 and val <=1:
                        p2 = subprocess.Popen(["caput",chName,str(val)], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                        (outputp1,errorp1) = p2.communicate()
                        output = outputp1.decode('utf-8')
                        #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                        #status = p1.returncode
                        print ('caputFFB_load() set to {}' .format(val))
                        status = errorp1
                else:
                        print ('caputFFB_load() only accept values 0 to 1')
                        status = 1
                        
                return status
                        

        #putt the "Enter Trigger State" state
        # This step is not done in this routine if the "Hardware Trigger" is in initiated state, 
        # setting Trigger State to 1 initiates sine wave outputs
        def caputFFB_enterTrig(chAlias,val):        

                trigs = {
                        1:"BMOD1:CHAN0:TRIGSTATEBTN",
                        2:"BMOD1:CHAN1:TRIGSTATEBTN",
                        3:"BMOD1:CHAN2:TRIGSTATEBTN",
                        4:"BMOD1:CHAN3:TRIGSTATEBTN",
                        5:"BMOD2:CHAN0:TRIGSTATEBTN",
                        6:"BMOD2:CHAN1:TRIGSTATEBTN",
                        7:"BMOD2:CHAN2:TRIGSTATEBTN",
                        8:"BMOD2:CHAN3:TRIGSTATEBTN"
                }
                chName = trigs.get(chAlias,"BMOD1:CHAN0:TRIGSTATEBTN")
                if val>=0 and val <=1:
                        p2 = subprocess.Popen(["caput",chName,str(val)], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                        (outputp1,errorp1) = p2.communicate()
                        output = outputp1.decode('utf-8')
                        #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                        #status = p1.returncode
                        print ('caputFFB_enterTrig() set to {}={}' .format(chName,val))
                        status = errorp1
                else:
                        print ('caputFFB_enterTrig() only accept values 0 to 1')
                        status = 1
                
                return status
 

        #set the "Leave Trigger State" state
        #When this state is set to 0, the state will be CONFIG_STATE
        def caputFFB_leaveTrig(chAlias,val):        
                
                trigs = {
                        1:"BMOD1:CHAN0:STOPBTN",
                        2:"BMOD1:CHAN1:STOPBTN",
                        3:"BMOD1:CHAN2:STOPBTN",
                        4:"BMOD1:CHAN3:STOPBTN",
                        5:"BMOD2:CHAN0:STOPBTN",
                        6:"BMOD2:CHAN1:STOPBTN",
                        7:"BMOD2:CHAN2:STOPBTN",
                        8:"BMOD2:CHAN3:STOPBTN"
                }
                chName = trigs.get(chAlias,"BMOD1:CHAN0:STOPBTN")
                if val>=0 and val <=1:
                        p2 = subprocess.Popen(["caput",chName,str(val)], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                        (outputp1,errorp1) = p2.communicate()
                        output = outputp1.decode('utf-8')
                        #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                        #status = p1.returncode
                        print ('caputFFB_leaveTrig() set to {}={}' .format(chName,val))
                        status = errorp1
                else:
                        print ('caputFFB_leaveTrig() only accept values 0 to 1')
                        status = 1
                
                return status

        #set the "Software Trigger" state
        def caputFFB_Trig(chAlias,val):        

                trigs = {
                        1:"BMOD1:CHAN0:TRIGBTN",
                        2:"BMOD1:CHAN1:TRIGBTN",
                        3:"BMOD1:CHAN2:TRIGBTN",
                        4:"BMOD1:CHAN3:TRIGBTN",
                        5:"BMOD2:CHAN0:TRIGBTN",
                        6:"BMOD2:CHAN1:TRIGBTN",
                        7:"BMOD2:CHAN2:TRIGBTN",
                        8:"BMOD2:CHAN3:TRIGBTN"
                }
                chName = trigs.get(chAlias,"BMOD1:CHAN0:TRIGBTN")
                if val>=0 and val <=1:
                        p2 = subprocess.Popen(["caput",chName,str(val)], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                        (outputp1,errorp1) = p2.communicate()
                        output = outputp1.decode('utf-8')
                        #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                        #status = p1.returncode
                        print ('caputFFB_Trig() set to {}={}' .format(chName,val))
                        status = errorp1
                else:
                        print ('caputFFB_Trig() only accept values 0 to 1')
                        status = 1

                return status


        #set the Relay for the output from the function generator into DAQ
        def caputFFB_relay(chAlias,val):        

                relays = {
                        1:"BMRELAYSET.B0",
                        2:"BMRELAYSET.B2",
                        3:"BMRELAYSET.B4",
                        4:"BMRELAYSET.B6",
                        5:"BMRELAYSET.B8",
                        6:"BMRELAYSET.BA",
                        7:"BMRELAYSET.BC",
                        8:"BMRELAYSET.BE",
                        9:"BMRELAYSET.B1",
                        10:"BMRELAYSET.B3",
                        11:"BMRELAYSET.B5",
                        12:"BMRELAYSET.B7",
                        13:"BMRELAYSET.B9",
                        14:"BMRELAYSET.BB",
                        15:"BMRELAYSET.BD",
                        16:"BMRELAYSET.BF"
                }
                chName = relays.get(chAlias,"BMRELAYSET.B0")
                if val>=0 and val <=1:
                        p2 = subprocess.Popen(["caput",chName,str(val)], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                        (outputp1,errorp1) = p2.communicate()
                        output = outputp1.decode('utf-8')
                        #caget commad does not handle stderr or return any error code so p1.returncode always return 0 making it useless
                        #status = p1.returncode
                        print ('caputFFB_relay() set to {}={}' .format(chName,val))
                        status = errorp1
                else:
                        print ('caputFFB_relay() only accept values 0 to 1')
                        status = 1
                        
                return status


        #print(caputFFB_modState()[0])
        #to calculate the time it take to run a python routine, devide the results by number=10 to get time for single call
        #print(timeit.timeit(cagetFFB_modState,number=10))
        #print(caputFFB_waveState(0)[0])
        #print(caputFFB_freq(0)[0])
        #print(caputFFB_amp(0)[0])
        #print(caputFFB_period(0)[0])
        #print(caputFFB_load(0)[0])
        #print(caputFFB_enterTrig(0)[0])
        #print(caputFFB_leaveTrig(2)[0])
        #print(caputFFB_Trig(2)[0])
        #print(caputFFB_relay(2)[0])
