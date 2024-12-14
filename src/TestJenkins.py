import json
import jenkins

server = jenkins.Jenkins('https://engci-private-gpk.cisco.com/jenkins/svo', username='mfontane', password='11e3bebab9a1ec38603eb12089a8dc16b2')
user = server.get_whoami()
version = server.get_version()
jobs = server.get_jobs()
print(json.dumps(jobs, indent=2))
print('Hello %s from Jenkins %s' % (user['fullName'], version))