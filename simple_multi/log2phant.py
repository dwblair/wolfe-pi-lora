import serial
import requests
import time
import json

#### some basic variables


baseURL = 'http://159.203.128.53'
#baseURL = 'https://data.sparkfun.com'

publicKey='D48m6lJVVGCJ0k41pbA0fxpQ8w6'
privateKey='z98lmbO665sglxzZmYqlHegqwAQ'

serialPort="/dev/ttyACM0"
serialPort="/dev/ttyUSB0"

serialBaud = 9600

loopDelay = 10 #seconds

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

#print "Waiting for serial port ..."
time.sleep(3)
#ser.flush() # flush to get rid of extraneous char

print "\n"

###### main loop 

while True:

    #cmd = "READ"
    #cmd = cmd.strip() + endl
    #ser.write(cmd.encode())
    print "Waiting for serial port ..."
    
    line = ser.readline()
    line=line.decode('utf-8')
    
    print 'raw serial input: ', line.strip()
  
    parsed = line.split('\t')
    
    if len(parsed) == 2:
    
        rssi=parsed[0].split(':')[1]

        j = str(parsed[1])

        #print 'rssi='+str(rssi)+" json="+j
        
        p = json.loads(j)
    
        id = str(p["id"])
        rssi = str(rssi)
        temp = str(p["data"]["temp"])
        vbat = str(p["data"]["vbat"])
        
        print "\n"
            
        print "id="+id
        print "rssi="+rssi
        print "temp="+temp
        print "vbat="+vbat
        

        pushUrl = baseURL+'/input/'+str(publicKey)+'?private_key='+str(privateKey)+'&id='+id+'&temp='+temp+'&humid='+vbat
         
        print pushUrl
         
        push = requests.get(pushUrl)
        
        print push
        
        print "wait after posting ..."
        
        time.sleep(loopDelay)
        

    # post to Phant
    #status = postPhant(line)
    #print "status =", status
    
    #print "waiting " + str(loopDelay) + " seconds til next read. "
    

    
    #time.sleep(loopDelay)
    
   
   

