from exec_cmd import *
import logging
logger = logging.getLogger('check')

def cdfImageDownload(data,target):
    logging.info("************CDF Image download**************************")
    logger.debug("*****************************Starting CDF Image Download************************")
    try:
        print 'Image download Status',data["configuration"]["transport"]["cdf"]["imgDownload"]
        i = 0
        if (data["configuration"]["transport"]["cdf"]["imgDownload"]):
            prod = data["configuration"]["product"]
            print 'Prod-',prod
            targetDockerUserName = target["configuration"]["systems"][0]["userName"]
            targetDockerPassword = target["configuration"]["systems"][0]["password"]
            print 'Docker username-',targetDockerUserName
            print 'Docker password-',targetDockerPassword
            while i<len(target["configuration"]["bundle"]["products"]):
                if prod in target["configuration"]["bundle"]["products"][i]["name"]:
                    for server in target["configuration"]["bundle"]["products"][i]["target"]["hostNames"]:
                        targetUser= target["configuration"]["bundle"]["products"][i]["target"]["security"]["userName"]
                        targetPassword= target["configuration"]["bundle"]["products"][i]["target"]["security"]["password"]
                        targetHostName= server
                        port = 22
                        print 'Target hostname-',targetHostName
                        print 'Target username-',targetUser
                        print 'target password-',targetPassword
                        obj = sshGetConnectionAPI(host=targetHostName, username=targetUser)
                        ssh = obj.sshGetConnection(port=port, password=targetPassword)
                        out, err = obj.sshExecCmd("sudo mkdir -p /bins/images")
                        print out,err
                        out, err = obj.sshExecCmd("sudo docker login -u %s -p %s" %(targetDockerUserName,targetDockerPassword))
                        print out,err
                        out, err = obj.sshExecCmd("bins/scripts/downloadimages.sh -y -u %s -p %s -C /bins/scripts/image-set.json -o hpeswitom -d /bins/images" %(targetDockerUserName,targetDockerPassword))
                        print out,err
                print("Start downloading images")
                return 0
                # code here
        else:
            print("No download of images needed")
            return 1
    except Exception as e:
        logger.debug("Error while executing command")
        raise
