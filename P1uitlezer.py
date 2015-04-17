#
# DSMR P1 uitlezer
# v1.0 (c) 10-2012 - GJ - gratis te kopieren en te plakken
# v1.1 2014 - changes by roeland@boul.nl to make it work with DSMR4 spec
# v1.2 2014 - roeland@boul.nl - add graphite/carbon logging.

versie = "1.2"
import sys
import serial
import socket
import time

CARBON_SERVER = 'admin.boul.nl'
CARBON_PORT = 2003



################
#Error display #
################
def show_error():
        ft = sys.exc_info()[0]
        fv = sys.exc_info()[1]
        print("Fout type: %s" % ft )
        print("Fout waarde: %s" % fv )
        return


################################################################################################################################################
#Main program
################################################################################################################################################
print ("DSMR P1 uitlezer",  versie)
print ("Control-C om te stoppen")

#Set COM port config
ser = serial.Serial()
ser.baudrate = 115200 
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=1
ser.rtscts=0
ser.timeout=12
ser.port="/dev/ttyUSB0"

while True:
        try:
                 sock = socket.socket()
                 sock.connect((CARBON_SERVER, CARBON_PORT))
                
                 #Open COM port
                 try:
                            ser.open()
                 except:
                            sys.exit ("Fout bij het openen van %s. Programma afgebroken."  % ser.name)     
                             
                
                
                
                 #Initialize
                 # stack is mijn list met de 20 regeltjes.
                 p1_teller=0
                 stack=[]
                 timestamp = int(time.time())
                 while p1_teller < 38:
                         p1_line=''
                 #Read 1 line
                         try:
                                 p1_raw = ser.readline()
                         except:
                                 sys.exit ("Seriele poort %s kan niet gelezen worden. Programma afgebroken." % ser.name )      
                         p1_str=str(p1_raw)
                         #p1_str=str(p1_raw, "utf-8")
                         p1_line=p1_str.strip()
                         stack.append(p1_line)
                 # als je alles wil zien moet je de volgende line uncommenten
                         print (p1_line)
                         p1_teller = p1_teller +1
                 #    print (p1_teller)
                 #Initialize
                 # stack_teller is mijn tellertje voor de 20 weer door te lopen. Waarschijnlijk mag ik die p1_teller ook gebruiken
                 stack_teller=0
                
                 while stack_teller < 38:
                        if stack[stack_teller][0:9] == "1-0:1.8.1":
                                print "Low KWh: ", stack[stack_teller][10:16]
                                message = 'system.raspi1.p1.low-KWh %s %d\n' % (stack[stack_teller][10:16], timestamp)  
                                sock.sendall(message)
                        elif stack[stack_teller][0:9] == "1-0:1.8.2":
                                print "High KWh:", stack[stack_teller][10:16]
                                message = 'system.raspi1.p1.high-KWh %s %d\n' % (stack[stack_teller][10:16], timestamp)
                                sock.sendall(message)
                 # Generated Power, Low Tariff 1-0:2.8.1
                        elif stack[stack_teller][0:9] == "1-0:2.8.1":
                                print "Generated Power, Low: ", stack[stack_teller][10:16]
                                message = 'system.raspi1.p1.generated-power-low %s %d\n' % (stack[stack_teller][10:15], timestamp)
                                sock.sendall(message)
                 # Generated Power, High Tariff 1-0:2.8.2
                        elif stack[stack_teller][0:9] == "1-0:2.8.2":
                                print "Generated Power, High: ", stack[stack_teller][10:16]
                                message = 'system.raspi1.p1.generated-power-high %s %d\n' % (stack[stack_teller][10:15], timestamp)
                                sock.sendall(message)
                 # Power failures: 0-0:96.7.21
                        elif stack[stack_teller][0:11] == "0-0:96.7.21":
                                print "Phase Failures: ", stack[stack_teller][12:17]
                                message = 'system.raspi1.p1.phase-failures %s %d\n' % (stack[stack_teller][12:17], timestamp)
                                sock.sendall(message)
                 # Number of extended failures 0-0:96.7.9
                        elif stack[stack_teller][0:10] == "0-0:96.7.9":
                                print "Extended Failures: ", stack[stack_teller][11:16]
                                message = 'system.raspi1.p1.extended-failures %s %d\n' % (stack[stack_teller][11:16], timestamp)
                                sock.sendall(message)
                 # Number of Voltage Sags L1: 1-0:32.32.0
                        elif stack[stack_teller][0:11] == "1-0:32.32.0":
                                print "Voltage Sags L1: ", stack[stack_teller][12:17]
                                message = 'system.raspi1.p1.voltage-sags-L1 %s %d\n' % (stack[stack_teller][12:17], timestamp)
                                sock.sendall(message)
                 # Number of Voltage Sags L2: 1-0:52.32.0
                        elif stack[stack_teller][0:11] == "1-0:52.32.0":
                                print "Voltage Sags L2: ", stack[stack_teller][12:17]
                                message = 'system.raspi1.p1.voltage-sags-L2 %s %d\n' % (stack[stack_teller][12:17], timestamp)
                                sock.sendall(message)
                 # Number of Voltage Sags L3: 1-0:72.32.0
                        elif stack[stack_teller][0:11] == "1-0:72.32.0":
                                print "Voltage Sags L3: ", stack[stack_teller][12:17]
                                message = 'system.raspi1.p1.voltage-sags-L3 %s %d\n' % (stack[stack_teller][12:17], timestamp)
                                sock.sendall(message)
                 # Number of Voltage Swells L1: 1-0:32.36.0
                        elif stack[stack_teller][0:11] == "1-0:32.36.0":
                                print "Voltage Swells L1: ", stack[stack_teller][12:17]
                                message = 'system.raspi1.p1.voltage-swells-L1 %s %d\n' % (stack[stack_teller][12:17], timestamp)
                                sock.sendall(message)
                 # Number of Voltage Swells L2: 1-0:52.36.0
                        elif stack[stack_teller][0:11] == "1-0:52.36.0":
                                print "Voltage Swells L2: ", stack[stack_teller][12:17]
                                message = 'system.raspi1.p1.voltage-swells-L2 %s %d\n' % (stack[stack_teller][12:17], timestamp)
                                sock.sendall(message)
                 # Number of Voltage Swells L3: 1-0:72.36.0
                        elif stack[stack_teller][0:11] == "1-0:72.36.0":
                                print "Voltage Swells L3: ", stack[stack_teller][12:17]
                                message = 'system.raspi1.p1.voltage-swells-L3 %s %d\n' % (stack[stack_teller][12:17], timestamp)
                                sock.sendall(message)
                 # Current Tariff: 0-0:96.14.0
                        elif stack[stack_teller][0:11] == "0-0:96.14.0":
                                print  "Tariff (1=L 2=H): ", stack[stack_teller][15:16]
                                message = 'system.raspi1.p1.tariff %s %d\n' % (stack[stack_teller][15:16], timestamp)
                                sock.sendall(message)
                 # Current Watt Delivered: 1-0:1.7.0
                        elif stack[stack_teller][0:9] == "1-0:1.7.0":
                                print "Current Watt Delivered: ", int(float(stack[stack_teller][10:16])*1000), " W"
                                message = 'system.raspi1.p1.current-watt %s %d\n' % (int(float(stack[stack_teller][10:16])*1000), timestamp)
                                sock.sendall(message)
                 # Current Watt Generated: 1-0:2.7.0
                        elif stack[stack_teller][0:9] == "1-0:1.7.0":
                                print "Current Watt Generated: ", int(float(stack[stack_teller][10:16])*1000), " W"
                                message = 'system.raspi1.p1.current-watt-generated %s %d\n' % (int(float(stack[stack_teller][10:16])*1000), timestamp)
                                sock.sendall(message)
                 # Limit KWh: 0-0:17.0.0
                        elif stack[stack_teller][0:10] == "0-0:17.0.0":
                                print "Limit: ", int(float(stack[stack_teller][11:16])*1000), " W"
                                message = 'system.raspi1.p1.current-limit %s %d\n' % (int(float(stack[stack_teller][11:16])*1000), timestamp)
                                sock.sendall(message)
                 # Current Amps L1
                        elif stack[stack_teller][0:10] == "1-0:31.7.0":
                                print "Current Amps L1: ", stack[stack_teller][11:14]
                                message = 'system.raspi1.p1.amps-L1 %s %d\n' % (stack[stack_teller][11:14], timestamp)
                                sock.sendall(message)
                 # Current Amps L2
                        elif stack[stack_teller][0:10] == "1-0:51.7.0":
                                print "Current Amps L2: ", stack[stack_teller][11:14]
                                message = 'system.raspi1.p1.amps-L2 %s %d\n' % (stack[stack_teller][11:14], timestamp)
                                sock.sendall(message)
                 # Current Amps L3
                        elif stack[stack_teller][0:10] == "1-0:71.7.0":
                                print "Current Amps L3: ", stack[stack_teller][11:14]
                                message = 'system.raspi1.p1.amps-L3 %s %d\n' % (stack[stack_teller][11:14], timestamp)
                                sock.sendall(message)
                 # Current Watts L1 1-0:21.7.0
                        elif stack[stack_teller][0:10] == "1-0:21.7.0":
                                print "Current Watts L1: ", int(float(stack[stack_teller][11:17])*1000), " W"
                                message = 'system.raspi1.p1.watts-L1 %s %d\n' % (int(float(stack[stack_teller][11:17])*1000), timestamp)
                                sock.sendall(message)
                 # Current Watts L1 - Generated  1-0:22.7.0
                        elif stack[stack_teller][0:10] == "1-0:22.7.0":
                                print "Current Watts L1 Generated: ", int(float(stack[stack_teller][11:17])*1000), " W"
                                message = 'system.raspi1.p1.watts-L1-generated %s %d\n' % (int(float(stack[stack_teller][11:17])*1000), timestamp)
                                sock.sendall(message)
                 # Current Watts L2 1-0:41.7.0
                        elif stack[stack_teller][0:10] == "1-0:41.7.0":
                                print "Current Watts L2: ", int(float(stack[stack_teller][11:17])*1000), " W"
                                message = 'system.raspi1.p1.watts-L2 %s %d\n' % (int(float(stack[stack_teller][11:17])*1000), timestamp)
                                sock.sendall(message)
                 # Current Watts L2 - Generated 1-0:42.7.0
                        elif stack[stack_teller][0:10] == "1-0:41.7.0":
                                print "Current Watts L2 Generated: ", int(float(stack[stack_teller][11:17])*1000), " W"
                                message = 'system.raspi1.p1.watts-L2-generated %s %d\n' % (int(float(stack[stack_teller][11:17])*1000), timestamp)
                                sock.sendall(message)
                 # Current Watts L3 1-0:61.7.0
                        elif stack[stack_teller][0:10] == "1-0:61.7.0":
                                print "Current Watts L3: ", int(float(stack[stack_teller][11:17])*1000), " W"
                                message = 'system.raspi1.p1.watts-L3 %s %d\n' % (int(float(stack[stack_teller][11:17])*1000), timestamp)
                                sock.sendall(message)
                 # Current Watts L3 - Generated 1-0:62.7.0
                        elif stack[stack_teller][0:10] == "1-0:61.7.0":
                                print "Current Watts L3 Generated: ", int(float(stack[stack_teller][11:17])*1000), " W"
                                message = 'system.raspi1.p1.watts-L3-generated %s %d\n' % (int(float(stack[stack_teller][11:17])*1000), timestamp)
                                sock.sendall(message)
                 # Current generated power: 1-0:1.7.0
                 #  elif stack[stack_teller][0:9] == "1-0:2.7.0":
                 #        print "Current generated power  ", int(float(stack[stack_teller][10:16])*1000), " W"
                 # Gasmeter: 0-1:24.2.1
                        elif stack[stack_teller][0:10] == "0-1:24.2.1":
                                print "Gas dm3: ", int(float(stack[stack_teller][26:35])*1000), " dm3"
                                message = 'system.raspi1.p1.gas-dm3 %s %d\n' % (int(float(stack[stack_teller][26:35])*1000), timestamp)
                                sock.sendall(message)
                
                        else:
                                 pass
                        stack_teller = stack_teller +1
                
                 sock.close()
                 #print (stack, "\n")

        except socket.gaierror:
                print "There was a problem with name resolution while sending data to carbon, continue..."
                pass
        
        except socket.error:
                print "There was a socket error, connectivity to Carbon down? continue..."
                pass
        
 #Close port and show status
        try:
                ser.close()
        except:
                sys.exit ("Oops %s. Programma afgebroken." % ser.name )      

