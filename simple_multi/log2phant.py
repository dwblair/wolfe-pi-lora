import serial
import requests
import time

#### some basic variables


baseURL = 'http://159.203.128.53'
#baseURL = 'https://data.sparkfun.com'

publicKey='KjqJ8gpeq1hzKlJjqm0KFPMGEVN'
privateKey='A9ypzYrKyATn7vg30OW7IGpzL3d'

serialPort="/dev/ttyACM0"

serialBaud = 9600

loopDelay = 9 #seconds

endl="\n"

### convenience function for posting to Phant
def postPhant(line):
    x=line.strip()
    x=x.strip()
    x=x.split(",")
    if (len(x)==6):
        timeVar=x[0]
        temp=float(x[1])
        pres=float(x[2]) 
        rh=float(x[3])
        tempc=float(x[4])
        tempf=float(x[5])

        pushUrl = baseURL+'/input/'+str(publicKey)+'?private_key='+str(privateKey)+'&datetime='+str(timeVar)+'&temperature='+str(temp)+'&pressure='+str(pres)+'&humidity='+str(rh)+'&tempc='+str(tempc)+'&tempf='+str(tempf)

        print pushUrl
        push = requests.get(pushUrl)
        
        return push.status_code
        
###### open and flush serial port

ser = serial.Serial(serialPort, serialBaud)

print "Waiting for serial port ..."
time.sleep(3)
ser.flush() # flush to ge rid of extraneous char

print "\n"

###### main loop 

while True:

    #cmd = "READ"
    #cmd = cmd.strip() + endl
    #ser.write(cmd.encode())
    line = ser.readline()
    line=line.decode('utf-8')
    
    print 'raw serial input: ', line.strip()
  
    parsed = line.split('\t')
    
    rssi=parsed[0].split(':')[1]

    json = parsed[1]

    print 'rssi='+str(rssi)+" json="+json

    # post to Phant
    #status = postPhant(line)
    #print "status =", status
    
    #print "waiting " + str(loopDelay) + " seconds til next read. "
    
    print "\n"
    
    #time.sleep(loopDelay)
    
   
   

