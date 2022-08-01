from google.cloud import compute 
import logging

from google.oauth2 import service_account

log = logging.getLogger("cheneque")

#cred = service_account.Credentials.from_service_account_file(environments.config["service_account_key"])
#credentials=cred
instanceClient = compute.InstancesClient()


def computeInstanceList(project, zone):
    instances = []
    instanceList = instanceClient.list(project=project, zone=zone)
    for i in instanceList:
        log.debug(i)
        obj = {
            "id":i.id,
            "name":i.name,
            "machine_type":i.machine_type,
            "cpu_platform":i.cpu_platform,
            "description":i.description,
            "last_start_timestamp":i.last_start_timestamp,
            "status":str(i.status)
        }
        instances.append(obj)
    return instances

def computeInstanceStart(project, zone, instanceId):
    response = instanceClient.start(project=project, zone=zone, instance=instanceId)
    return { "id":response.id, "status":str(response.status), "progress":response.progress }

def computeInstanceStop(project, zone, instanceId):
    response = instanceClient.stop(project=project, zone=zone, instance=instanceId)
    return { "id":response.id, "status":str(response.status), "progress":response.progress }

def processRequest(req):
    log.debug("compute processRequest has been called")
    action = req["action"]
    
    if action == "computeInstanceList":
        project = req["project"]
        zone = req["zone"]
        return computeInstanceList( project, zone )
    elif action == "computeInstanceStart":
        project = req["project"]
        zone = req["zone"]
        instanceName = req["instanceName"]
        return computeInstanceStart( project, zone, instanceName )
    elif action == "computeInstanceStop":
        project = req["project"]
        zone = req["zone"]
        instanceName = req["instanceName"]        
        return computeInstanceStop( project, zone, instanceName )
    else:
        raise Exception("compute connnect request not found")



if __name__ == "__main__":
    print("hello compute_connect")
