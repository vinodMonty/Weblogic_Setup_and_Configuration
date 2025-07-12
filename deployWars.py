if __name__ == '__main__': 
    from wlstModule import *  # @UnusedWildImport
import sys
import re
import getopt
import os  


def connectWeblogic():
	try:
		connect(USERNAME, PASSWORD, ADMINURL)
		print("Connected to Weblogic Server: {}".format(ADMINURL))
	except WLSTException as error:
		print("Error in connecting to Weblogic Server")
		sys.exit(1)

def disconnectWeblogic():
	try:
		print('Disconnecting from Weblogic Server...')
		disconnect()
		print('Disconnected Successfully!!!')
	except WLSTException as e:
		print('ERROR: Error occured while disconnecting from Weblogic Server... : {}'.format(str(e)))
		sys.exit(1)


def usage():
    toprint = '''
---------------------------------------------------------
Invoke the script using any one of the following commands
---------------------------------------------------------
java weblogic.WLST <PATH_TO_THIS_FILE>/deployWars.py -u <USERNAME> -p <PASSWORD> -a t3://mwiapp01:18001 -w <WAR_FILE_PATH> -s <START_ORDER> 
---------------------------------------------------------
        '''
    print(toprint)

	



def getWarFilePath(serviceName,PATH):
	warFiles = os.listdir(PATH)
	warFilesWithServiceName = []
	for f in warFiles:
		if f.startswith(serviceName) and (f.endswith('.war') or f.endswith('.ear') or f.endswith('.jar') or f.endswith('.rar')):
			warFilesWithServiceName.append(os.path.join(PATH,f));
	if warFilesWithServiceName:
		latest_file = max(warFilesWithServiceName, key=lambda f: os.path.getmtime(f))
		return os.path.join(PATH, max(warFilesWithServiceName, key=lambda f: os.path.getmtime(f)))
	else:
		return None


def deployServices():
	with open(DEPLOYMENTORDER) as file:
		PATHS = WARPATH.split(',')
		for x in file.readlines():
			x = x.strip()
			tList = x.split('|')
			serviceName = tList[0]
			targetName = tList[1]
			isLibrary = tList[2].lower() == 'true'
			try:
				for PATH in PATHS:
					warFilePath = getWarFilePath(serviceName,PATH)
					if warFilePath is not None:
						deploy(serviceName, warFilePath, targets=targetName, stageMode='stage', libraryModule=isLibrary ,block='true')
						print("______________________________________________________________")
						print('Application {} is deployed at {}'.format(serviceName,targetName))
						print("______________________________________________________________")
						break
					else:
						print("War file {} not found in path -- {} ".format(serviceName,PATH))
			except WLSTException as error:
				print("Error while deploying {}: {}\n".format(serviceName,error))
	print("Deployments completed!!!")



# Main
USERNAME = "NULL"
PASSWORD = "NULL"
ADMINURL = "NULL"
WARPATH = "NULL"
DEPLOYMENTORDER = "NULL"

# Checking Argument Length passed
if len(sys.argv) < 2:
    print("Invalid number of arguments, Expected 3 arguments, Found [{}]".format(len(sys.argv)))
    print("")

# Defining the Arguments

try:
    opts, args = getopt.getopt(sys.argv[1:], "h:u:p:d:w:a:", ["help", "username=", "password=", "deployment=", "wardirPath=", "adminurl="])
except getopt.GetoptError:
    print("Check the options. They are not valid")
    usage()
    sys.exit(2)

for opt, arg in opts:
	if opt in ("-h", "--help"):
		usage()
		sys.exit()
	elif opt in ("-d", "--deployment"):
		print("INFO: App Deployment Order ==> {}".format(arg))
		DEPLOYMENTORDER = arg
	elif opt in ("-w", "--wardirPath"):
		print("INFO: War Path ==> {}".format(arg))
		WARPATH = arg
	elif opt in ("-u", "--username"):
		print("INFO: Username set to ==> {}".format(arg))
		USERNAME = arg
	elif opt in ("-p", "--password"):
		print("INFO: Password set to ==> ****")
		PASSWORD = arg
	elif opt in ("-a", "--adminurl"):
		print("INFO: AdminURL set to ==> {}".format(arg))
		ADMINURL = arg
		match = re.match(r'(t3|t3s)(\:)(\/\/)(.*:)(\d+)', ADMINURL)
		if not match:
			print("\nERROR: AdminURL is wrong, Make sure you are using t3/t3s protocol")
			print("Sample AdminURL: t3://localhost:17001")
			sys.exit()
	else:
		assert False, "ERROR: Option is not supported"
		sys.exit()

print("______________________________________________________________")

if "NULL" in USERNAME and "NULL" in PASSWORD and "NULL" in DEPLOYMENTORDER and "NULL" in WARPATH and "NULL" in MDBPATH:
    print("The script must be started with username and password for Adminserver, startOrder, and wardirPath and mdb path if applicable")
    usage()
    sys.exit()

if ADMINURL == "NULL":
    print("AdminURL is empty", ADMINURL)
    usage()
    sys.exit()

# Invoke Functions
connectWeblogic()
deployServices()
disconnectWeblogic()
