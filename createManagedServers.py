if __name__ == '__main__':
    from wlstModule import * 
import getopt
import sys
import re


def connectWeblogic():
    try:
        print("Connecting to Weblogic Server")
        connect(USERNAME, PASSWORD, ADMINURL)
        print("Connected Successfully!!!")
    except WLSTException as e:
        print("Failed to connect : {}".format(str(e)))
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
java weblogic.WLST <PATH_TO_THIS_FILE>/createDatasources.py -u <USERNAME> -p <PASSWORD> -a t3://mwiapp01:18001 -d <DATASOURCESFILE>  
---------------------------------------------------------
        '''
    print(toprint)


def createDatasources():
    with open(DATASOURCELIST) as file:
        for x in file.readlines():
            x = x.strip()
            datasourceList = x.split('|')
            dsName = datasourceList[0]
            jndiName = datasourceList[1]
            driverName = datasourceList[2]
            dbUser = datasourceList[3]
            dbPassword = datasourceList[4]
            clusters = datasourceList[5]
            dburl = datasourceList[6]
            try:
                domainConfig()
                edit()
                startEdit()
                cd('/')
                try:
                    create(dsName,'JDBCSystemResource')
                except:
                    print("_______________________________________________")
                    print('Datasource {} already available'.format(dsName))
                    print("_______________________________________________")
                    stopEdit('y')
                    continue
                cd('/JDBCSystemResources/'+ dsName +'/JDBCResource/'+dsName)
                set('Name',dsName)
                set('DatasourceType','AGL')
                #DriverParams
                cd('/JDBCSystemResources/'+ dsName +'/JDBCResource/'+dsName+'/JDBCDriverParams/' + dsName)
                set('DriverName',driverName)
                set('Url',dburl)
                set('Password',dbPassword)
                cd('/JDBCSystemResources/'+ dsName +'/JDBCResource/'+dsName+'/JDBCDriverParams/' + dsName+'/Properties/' + dsName)
                create('user','Property')
                cd('Properties/user')
                set('Value',dbUser)
                #OracleParams
                cd('/JDBCSystemResources/'+ dsName +'/JDBCResource/'+dsName+'/JDBCOracleParams/' + dsName)
                set('FanEnabled','false')
                set('OnsNodeList','')
                set('OnsWalletFile','')
                set('OnsWalletPassword','')
                #DatasourceParams
                cd('/JDBCSystemResources/'+ dsName +'/JDBCResource/'+dsName+'/JDBCDataSourceParams/' + dsName)
                set('GlobalTransactionsProtocol','None')
                set('JNDINames',jarray.array([String(jndiName)],String))
                cd('/JDBCSystemResources/'+ dsName)
                #Setting Cluster
                print('Setting Cluster')
                clusterObjectArray = []
                clusterArray = clusters.split(',')
                for cluster_name in clusterArray:
                    clusterObject = ObjectName('com.bea:Name=' + cluster_name +',Type=Cluster')
                    clusterObjectArray.append(clusterObject)
                set('Targets',jarray.array(clusterObjectArray, ObjectName))
                save()
                activate()
                print("______________________________________________________________")
                print("Datasource {} created successfully".format(dsName))
                print("______________________________________________________________")

            except WLSTException as e:
                print("ERROR: Getting error while creating datasource {} : {}".format(dsName,str(e)))
                undo('true','y')
                cancelEdit('y')
                disconnectWeblogic()
                sys.exit(1)
                

def datasourceStatus():
    try:
        serverRuntime()
        cd('/JDBCServiceRuntime/AdminServer/JDBCDataSourceRuntimeMBeans')

        datasourceMBeans = ls(returnMap = 'true')

        for dsName in datasourceMBeans:
            cd('/JDBCServiceRuntime/AdminServer/JDBCDataSourceRuntimeMBeans/'+dsName)
            dsState = get('State')
            print("Datasource {} status ==> {}".format(dsName,dsState))
            print("_______________________________________________")
    except WLSTException as e:
        print("ERROR: Error Occured while fetching status of datasources: {}".format(str(e)))
        disconnectWeblogic()
        sys.exit(1)



# Main
USERNAME = "NULL"
PASSWORD = "NULL"
ADMINURL = "NULL"
DATASOURCELIST = "NULL"

#Checking Argument Length passed

if len(sys.argv) < 2:
    print("Invalid number of Arguments, Expected 3 arguments, Found [{}]".format(len(sys.argv)))
    print("")

#Defining Arguments
try:
    opts, args = getopt.getopt(sys.argv[1:],"h:u:p:a:d:",["help","username=","password","adminurl=","datasourcelist="])  
except getopt.GetoptError:
    print("Check the options. They are not valid")
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h","--help"):
        usage()
        sys.exit()
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
    elif opt in ("-d","--datasourcelist"):
        print("Datasource Lists ==> {}".format(arg))
        DATASOURCELIST = arg
    else:
        assert False, "ERROR: Option is not supported"
        sys.exit()

print("______________________________________________________________")

if "NULL" in USERNAME and "NULL" in PASSWORD and "NULL" in DATASOURCELIST:
    print("The script must be started with username and password for Adminserver and server list")
    usage()
    sys.exit()

if ADMINURL == "NULL":
    print("AdminURL is empty", ADMINURL)
    usage()
    sys.exit()

connectWeblogic()
createDatasources()
datasourceStatus()
disconnectWeblogic()




