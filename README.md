# Weblogic Automation Tool
Python-based CLI automation tool for Oracle WebLogic Server — automates managed server creation, datasource configuration, WAR/EAR deployment, and SSL/Keystore setup using WLST.

## Pre Requisites:
- Run the `setDomainEnv.sh` file: `. /<path_to_domain>/bin/setDomainEnv.sh`
- Run the `setWlstEnv_internal.sh` file: `. /<path_to_middleware_home>/oracle_common/common/bin/setWlstEnv_internal.sh`

## Creating Managed Servers
To create managed server, set the required details in the **/config/ManagedServers/Domain_Name.txt** file. Then run the following command once prerequisite steps are done.

`java weblogic.WLST <path_to_createManagedServers.py> -u <weblogic_user> -p <weblogic_user_password> -a t3://<Host>:<Admin_Port> -s /config/ManagedServers/Domain_Name.txt`

## Creating Datasources
To create datasources, set the required details in the **/config/Datasources/Domain_Name.txt** file. Then run the following command once prerequisite steps are done.

`java weblogic.WLST <path_to_createDatasource.py> -u <weblogic_user> -p <weblogic_user_password> -a t3://<Host>:<Admin_Port> -d /config/Datasources/Domain_Name.txt`

## Deploying War/Ear/Library Files
To deploy services, set the required details in the **/config/Services/Domain_Name.txt** file. Then run the following command once prerequisite steps are done.

`java weblogic.WLST <path_to_deployWars.py> -u <weblogic_user> -p <weblogic_user_password> -a t3://<Host>:<Admin_Port> -d /config/Services/Domain_Name.txt -w <Path_to_Dir_Containing_Files>`

## Setting SSL and Keystore Details in Managed Servers
To set the SSL and Keystores in the Managed Servers, set the required details in the **/config/KeystoreSSLConfig.txt** file. Then run the following command once prerequisite steps are done.

`java weblogic.WLST <path_to_keyStoreAndSSLConfig.py> -u <weblogic_user> -p <weblogic_user_password> -a t3://<Host>:<Admin_Port> -c /config/KeystoreSSLConfig.txt`

