import subprocess, platform
import time, datetime
import sys

def pingResult(hostaddress,desc):
  try:
    output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', hostaddress), shell=True)
    #print(f"TRACE: {desc} : Connected")
  except Exception as e:
    #print(f"TRACE: {desc} Host Address: {hostaddress} - Not Connected. {e}")
    return False
  return True

def tryNumberOfTimes(hostaddress,desc,times):
  i=0
  res = False
  while i<times and res == False:
    res = pingResult(hostaddress,desc)
    i = i+1
  return res

def evaluate():
  global first_boot, bescom_ON, generator_ON, internet_ON
  BES_DEV = "192.168.0.131"
  GEN_DEV = "192.168.0.105"
  INT_ADD = "google.com"
  if first_boot == True:
    bescom_success = tryNumberOfTimes(BES_DEV,"Bescom",3)
    if bescom_success == True:
      print(f"{datetime.datetime.now()} Running in BESCOM Power")
      bescom_ON = True
    elif tryNumberOfTimes(GEN_DEV,"Generator or Bescom",3) == True:
      print(f"{datetime.datetime.now()} Running in DG")
      generator_ON = True
    if tryNumberOfTimes(INT_ADD,"Internet",3) == True:
      print(f"{datetime.datetime.now()} Internet is Working")
      internet_ON = True
    first_boot = False
  else:
    bescom_success = tryNumberOfTimes(BES_DEV,"Bescom",3)
    if bescom_success:
      if bescom_ON == False:
         print(f"{datetime.datetime.now()} BESCOM Power Restored")
         bescom_ON = True
         generator_ON = False
    else:
      if bescom_ON == True:
         print(f"{datetime.datetime.now()} BESCOM Power gone")
         bescom_ON = False
      gen_success = tryNumberOfTimes(GEN_DEV,"Generator or Bescom",3)
      if gen_success == True:
         if generator_ON == False:
            print(f"{datetime.datetime.now()} DG Power Started")
            generator_ON = True
      else:
         if generator_ON == True:
            print(f"{datetime.datetime.now()} No power from Bescom or DG")
            generator_ON = False
    internet_success = tryNumberOfTimes(INT_ADD,"Internet",3)
    if internet_success:
      if internet_ON == False:
        print(f"{datetime.datetime.now()} Airtel Internet Restored")
        internet_ON = True
    else:
      if internet_ON == True:
        print(f"{datetime.datetime.now()} Airtel Internet gone")
        internet_ON = False 



first_boot = True
bescom_ON = False
generator_ON = False
internet_ON = False

while True:
  evaluate()
  sys.stdout.flush()
  time.sleep(30)

#print(pingResult("192.168.0.131","Bescom"))
#print(pingResult("192.168.0.105","Generator or Bescom"))
#print(tryNumberOfTimes("nogoz.e.google.com","Internet",3))


