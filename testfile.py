import subprocess, platform
def pingResult(hostaddress):
  try:
    print(platform.system().lower())
    output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', hostaddress), shell=True)
  except Exception as e:
    print(e)
    return False
  return True

print("Hello")
first_boot = True
bescom_ON = False
generator_ON = False
internet_ON = False
print(pingResult("google.com"))
