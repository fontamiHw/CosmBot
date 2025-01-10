# COSM-webex
A WEBEX bot to automate the Pr and Sanity of COSM project

## Reference
https://pypi.org/project/webex-bot/
https://github.com/WebexCommunity/WebexPythonSDK/tree/release/v1/webexteamssdk

## API Documentation

 - ### WebEx
     [Doc](https://webexcommunity.github.io/WebexPythonSDK/user/quickstart.html)

 - ### Atlassian
    [Doc](https://atlassian-python-api.readthedocs.io/)
    [example](https://github.com/atlassian-api/atlassian-python-api/tree/master/examples) 
    
 - ### Jenkins
    [Python Doc](https://python-jenkins.readthedocs.io/en/latest/)
    
   COSM url references
    1. [mainUrl](https://engci-private-gpk.cisco.com/jenkins/svo/job/svo_multibranch)
    2. [All Jobs](https://engci-private-gpk.cisco.com/jenkins/svo/job/svo_multibranch/view/change-requests)
    3. [Single Job](https://engci-private-gpk.cisco.com/jenkins/svo/job/svo_multibranch/view/change-requests/job/<PR#>/)

## installation
pip install -r requirements.txt


## Docker
### network
docker network create --driver=bridge --subnet=172.20.0.0/24 --gateway 172.20.0.1 Cosm-net


## Pr Protocol
###  type
 1. **all**
    - {"type":"all"} : list all the PR of the registered url
 2. **job**
    - {"type":"job", "job":"PR-11210", "status":"status"} : send message to the user of the job status
    - {"type":"job", "job":"PR-11210", "status":"merges"} : send message to the user job is merged

