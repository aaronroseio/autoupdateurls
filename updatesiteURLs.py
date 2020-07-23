# import modules
from os import path
import urllib2
import os.path
import os
import getpass
import json
import ssl
# SSL context to provide a CA Bundle for server verification.  Download the CA Bundle here before running https://curl.haxx.se/ca/cacert.pem & make sure the path below is correct
ctx = ssl.create_default_context(cafile="/home/admin/cacert.pem")
# Define variables -- change object name & category as needed
newfile = 'suspiciousdomains.txt'
objectName = 'SUSP-DOM111'
objectCategory = 'Custom_Application_Site'
apiKey = 'API-KEY-HERE'  # only needed for unattended use
domain = 'DOMAIN-NAME-HERE'  # MDM Domain
policyPackage = 'Standard'  # policy-package-name-here
installTargets = 'R8040GWDEVTEST'  # policy-install-targets-here
# retrieve latest file from github


def retrieveLatest():
    filedata = urllib2.urlopen(
        'https://github.com/aaronroseio/autoupdateurls/blob/master/suspiciousdomains.txt', context=ctx)
    datatowrite = filedata.read()

    with open('suspiciousdomains.txt', 'wb') as f:
        f.write(datatowrite)

# function for login to mgmt api and retrieve sid-- this can be used with username & password for testing, as well as with the api key


def apiLogin(logincommand):
    stream = os.popen(logincommand)
    loginOutput = stream.read()
    jsonLoginOutput = json.loads(loginOutput)
    return jsonLoginOutput["sid"]


# function to publish changes using sid from login


def apiPublish(sid):
    stream = os.popen("mgmt_cli publish --session-id " + sid)
    publishOutput = stream.read()
    print (publishOutput)

# function to logout after publish using sid from login


def apiLogout(sid):
    stream = os.popen("mgmt_cli logout --session-id " + sid)
    logoutOutput = stream.read()
    print (logoutOutput)


# function to install policy after publish using sid from login


def apiInstall(sid, policyPackage, installTargets):
    installPolicyCommand = 'mgmt_cli install-policy policy-package "{}" access true threat-prevention false targets "{}" --session-id {} '.format(
        policyPackage, installTargets, sid)
    stream = os.popen(installPolicyCommand)
    installOutput = stream.read()
    print (installOutput)

# this function is for the first time run using the add application-site command


def addApplicationSite(newfile, sid, objectName, objectCategory):
    with open(newfile, 'r') as fp:
        line = fp.readline()
        cnt = 1
        addApplicationCommand = 'mgmt_cli add application-site name {} primary-category {} --format json'.format(
            objectName, objectCategory)
        while line:
            if not line.startswith('#'):
                addApplicationCommand += ' url-list.{} "{}"'.format(
                    cnt, line.strip())
            line = fp.readline()
            cnt += 1
        addApplicationCommand += " --session-id " + sid
        print(addApplicationCommand)
        os.system(addApplicationCommand)

# this function is for the first time run using the set application-site command with url.list.add argument, although it adds all urls in the txt file, only the changes are processed by the mgmt api server


def editApplicationSite(newfile, sid, objectName):
    with open(newfile, 'r') as fp:
        line = fp.readline()
        cnt = 1
        editApplicationCommand = 'mgmt_cli set application-site name {} --format json'.format(
            objectName)
        while line:
            if not line.startswith('#'):
                editApplicationCommand += ' url-list.add.{} "{}"'.format(
                    cnt, line.strip())
            line = fp.readline()
            cnt += 1
        editApplicationCommand += " --session-id " + sid
        print(editApplicationCommand)
        os.system(editApplicationCommand)


# prompt user for login credentials to mgmt api server, then build the login command as a variable to pass to login function - this can be adapted to use an api key to allow for unattended use (cron)
username = raw_input("API Username:")
password = getpass.getpass("Password for " + username + ":")
logincommand = "mgmt_cli login user " + username + \
    " password " + password + " --format json"

# uncomment the variable below and comment out the lines above to use the apikey
# logincommand = 'mgmt_cli login api-key "{}" domain "{}" --format json'.format(apiKey,domain)
print (logincommand)

sid = apiLogin(logincommand)
print path.exists("suspiciousdomains.txt")
# check to see if file exists --- uncomment #apiInstall lines if you want the script to install policy each time or create a separate script to run at the desired interval with the functions login, install & logout
if path.exists('suspiciousdomains.txt'):
    retrieveLatest()
    editApplicationSite(newfile, sid, objectName)
    apiPublish(sid)
    #apiInstall(sid, policyPackage, installTargets)
    apiLogout(sid)
else:
    retrieveLatest()
    addApplicationSite(newfile, sid, objectName, objectCategory)
    apiPublish(sid)
    #apiInstall(sid, policyPackage, installTargets)
    apiLogout(sid)
