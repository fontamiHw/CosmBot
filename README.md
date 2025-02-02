
# COSM-webex
A WEBEX bot to automate the Pr and Sanity of COSM project

     


## Reference
https://pypi.org/project/webex-bot/
https://github.com/WebexCommunity/WebexPythonSDK/tree/release/v1/webexteamssdk

     


## API Documentation
-  ### WebEx
[Doc](https://webexcommunity.github.io/WebexPythonSDK/user/quickstart.html)

-  ### Atlassian
[Doc](https://atlassian-python-api.readthedocs.io/)
[example](https://github.com/atlassian-api/atlassian-python-api/tree/master/examples)

-  ### Jenkins
[Python Doc](https://python-jenkins.readthedocs.io/en/latest/)

COSM url references
1. [mainUrl](https://engci-private-gpk.cisco.com/jenkins/svo/job/svo_multibranch)
2. [All Jobs](https://engci-private-gpk.cisco.com/jenkins/svo/job/svo_multibranch/view/change-requests)
3. [Single Job](https://engci-private-gpk.cisco.com/jenkins/svo/job/svo_multibranch/view/change-requests/job/<PR#>/)

     


## Prerequisite
 1. Python 3.10 or above
 2. The log files will be write in a specific path that sahll be present
    on the disk three directory are required and this shall be theire
    name 
     - logs
     - files
     - resources
     


## Configuration file
The app use the `CosmWebex-config` file to change its beaviour.
The first run of the app in any of the 2 modes will copy the default file in the `resources` directory and use that.
Any other runs does not overwrite the config file.
There are 2 ways to start then:

 1. Run the app, stop it, change the config, run again
 2. Copy the `CosmWebex-config` under the `resources` directory, edit and run

Any element is described in the yaml file itself
     


## Local Mode
If the tools is running in a private server this are the Python library that are requested:
> pip install -r requirements.txt

###  setUp
 1. Create the three directories described before and update that in the
    `start.sh` script    
    >     NOTE: It is not importand where they are located.
    >     They could be in different mount of the disk but is important that 
    >          the path is correctly written in the above script    
2. Create the directory for the internal database.
     The path is defined in the configuration file `CosmWebex-debug-config`,
    on the element  `database: directory: "./database"`.
    The startup script will copy this file under the `resources` directory described above changing its name in the one used by the code
 
###  Run
Simply run the script `start.sh` 

     


## Docker Mode
###  setUp
 - ***Network***
It is required a Newtork bridge for the internal communication between the 2 containers that compose the whole tool.
The network must be the same as the other container  ([COSM-fastapi](https://wwwin-github.cisco.com/mfontane/COSM-fastApi)) it is working with.

 - ***Host volume***
 The Host shall have the three directories described above already presents on disk.
 All the three directories **must be under the same root directory**
 write the path in the  ***HOST*** variable within the  `Docker/startCosmBoth.sh` script

### network
docker network create --driver=bridge --subnet=172.20.0.0/24 --gateway 172.20.0.1 Cosm-net

###  Run
Simply run the `Docker/startCosmBoth.sh` script

     


## Docker Creation
Adapt the script `Docker/createImage.sh` at your need (maybe the name of the image)
Simply run the script 