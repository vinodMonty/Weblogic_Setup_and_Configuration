if __name__ == '__main__':
    from wlssModule import *
import getopt
import sys
import re
import os
from java.io import File, FileReader, BufferedReader

def connectWeblogic():
    try:
        print("Connecting to Weblogic Server")
        connect(USERNAME,PASSWORD,ADMINURL)
        print("Connected Successfully!!!")
    except WLSTException as e:
        print("Failed to connect : {} ".format(str(e)))
        sys.exit(1)

def disconnectWeblogic():
    try:
        print("Disconnecting from Weblogic Server...")
        disconnect()
        print("Disconnected Successfully!!!")
    except WLSTException as e:
        print('ERROR: Error occured while disconnecting from Weblogic Server... : {}'.format(str(e)))
        sys.exit(1)

def usage():
    toprint = '''
----------------------------------------------
Invoke the script using the following command
----------------------------------------------
java weblogic.WLST <PATH_TO_THIS_FILE>/keyStoreAndSSLConfig.py -u <USERNAME> -p <PASSWORD> -a t3://<weblogic_host>:<adminserverport> -c <PATH_TO_CONFIG_FILE>
----------------------------------------------
        '''
    print(toprint)


#Function for Updating the keystore and SSL configurations of Managed Server
#<KeyStores>|<KeyStoreType>|<IdentityKeyStorePath>|<TrustKeyStorePath>|<Password>|<alias>

def updateKeyStoreSSLConfig():
    
    with open(CONFIGFILE) as file:
        for x in file.readlines():
            x = x.strip()
            configfilelist = x.split('|')
            keystores = configfilelist[0]
            keystoreType = configfilelist[1]
            identitykeystorepath = configfilelist[2]
            trustkeystorepath = configfilelist[3]
            password = configfilelist[4]
            alias = configfilelist[5]
            try:
                domainConfig()
                edit()
                startEdit()
                cd('/Servers')
                servers = ls(returnMap='true')

                for server_name in servers:
                    if server_name != 'AdminServer':
                        print("Updating KeyStore and SSL for Managed Server {}".format(server_name))
                        cd('/Servers/{}'.format(server_name))
                        set('KeyStores',keystores)
                        set('CustomIdentityKeyStoreFileName', identitykeystorepath)
                        set('CustomIdentityKeyStoreType', keystoreType)
                        set('CustomIdentityKeyStorePassPhrase', password)
                        set('CustomTrustKeyStoreFileName', trustkeystorepath)
                        set('CustomTrustKeyStoreType', keystoreType )
                        set('CustomTrustKeyStorePassPhrase', password)

                        save()

                        cd('/Servers/{}/SSL/{}'.format(server_name,server_name))
                        set('KeyAlias',alias)
                        set('KeyPassPhrase',password)

                        save()
                        activate()
                        print("")
                        print("Keystore and SSL Configurations done successfully for Managed Server ==> {}".format(server_name))
                        print("")
            except WLSTException as e:
                print('ERROR: Error occured while configuring Managed Server : {}'.format(str(e)))
                cancelEdit('y')
                disconnectWeblogic()
                sys.exit(1)

#MAIN
USERNAME = "NULL"
PASSWORD = "NULL"
ADMINURL = "NULL"
CONFIGFILE = "NULL"

#Checking length of arguments
if len(sys.argv) < 2:
    print("Invalid number of arguments. Expected 3 arguments, Found[{}]".format(len(sys.argv)))
    print("")

#Defining arguments

try:
    opts,args = getopt.getopt(sys.argv[1:],"h:u:p:a:c:",["help","username=","password=","adminurl=","configfile="])
except getopt.GetoptError:
    print("Check the options. They are not valid")
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h","--help"):
        usage()
        sys.exit()
    elif opt in ("-u","--username"):
        print("INFO: Username set to ==> {}".format(arg))
        USERNAME = arg
    elif opt in ("-p","--password"):
        print("INFO: Password set to ==> {}".format(arg))
        PASSWORD = arg
    elif opt in ("-a","--adminurl"):
        print("INFO: AdminURL set to ==> {}".format(arg))
        ADMINURL = arg
        match = re.match(r'(t3|t3s)(\:)(\/\/)(.*:)(\d+)',ADMINURL)
        if not match:
            print("\nERROR: AdminURL is wrong, Make sure you are using t3/t3s protocol")
            print("Sample AdminURL: t3://localhost:17001")
            sys.exit()
    elif opt in ("-c","--configfile"):
        print("INFO: Config File set to ==> {}".format(arg))
        CONFIGFILE = arg
    else:
        assert False, "ERROR: Option is not supported"
        sys.exit()

print("___________________________________________________________________________")

if "NULL" in USERNAME and "NULL" in PASSWORD and "NULL" in CONFIGFILE:
    print("The script must be started with username and password for Adminserver and config file")
    usage()
    sys.exit(1)

if ADMINURL == "NULL":
    print("AdminURL is empty", ADMINURL)
    usage()
    sys.exit()

connectWeblogic()
updateKeyStoreSSLConfig()
disconnectWeblogic()    
