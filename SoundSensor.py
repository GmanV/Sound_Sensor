import mraa 
import time
import socket   #for sockets
import sys  #for exit

INTERVAL = .05                   # Sound Signature Sample time
SENDMSG_INTERVAL =60           # Minimum time between sending something to cloud

LED_GPIO = 5                   # The LED pin
TRIGGER_GPIO = 6               # The TRIGGER GPIO
led = mraa.Gpio(LED_GPIO)      # Get the LED pin object
led.dir(mraa.DIR_OUT)          # Set the direction as output
trig = mraa.Gpio(TRIGGER_GPIO) # Get the TRIGGER pin object
trig.dir(mraa.DIR_IN)          # Set the direction as input

ledState = False               # LED is off to begin with
led.write(0)


def getTriggerf():
    """ This function operates for minimal send interval """
    t = time.time()
    next_sample_time = t + SENDMSG_INTERVAL
    
    while (1):
        if t > next_sample_time:
            print 'Timed Out'
            return (0)
        if (trig.read() != 1):
            # No trigger detected
            continue
        else:
            # Detected a trigger
            return (1)


def getSignature():
    """ This function determines if a valid shot is fired """                
    t = time.time()
    next_sample_time = t + INTERVAL
    lowCt=0
    highCt=0
                
    while True:
        t = time.time()
        if t > next_sample_time:
            print highCt
            print lowCt
            return int(lowCt)
        else:
            if (trig.read() == 1):
            # valid highpulse
                highCt += 1
                continue
            
            else:
                # Detected a click
                lowCt += 1
                continue
            
            
         

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 41234
    msg = '{"n": "temp", "v": 1.0}'
    msgnull = '{"n": "temp", "v": 0.0}'
    # initialize our socket...
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()

    while 1:
        # wait until trigger or timed out
        lowtrig = getTriggerf()
        print 'Sound Detected or Timed Out'
 
        if lowtrig == 0:
                 
            try :
                #Set the whole string
                s.sendto(nullmsg, (host, port))
                print 'Null Message Sent'

            except socket.error, msg:
                print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                sys.exit() 
            continue
        else :    
            lowCt =getSignature ()
            print 'Signature Detected'
            print lowCt

            if lowCt > 100 <600:
                try :
                    #Set the whole string
                    s.sendto(msg, (host, port))
                    print 'Message Sent'

                except socket.error, msg:
                    print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                    sys.exit()

        # Button click, detected, now toggle the LED
#        if ledState == True:
#            led.write(1)
#            ledState = False
#        else:
#            led.write(0)
#            ledState = True

#    time.sleep(0.005)
