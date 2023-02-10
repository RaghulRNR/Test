import requests
import base64
import json 
import sys
#PAT should be replace by parameters
#PAT = 'oosyebh2tyyn37rycb2ptais2uny7mc36fzpsvwuvalpdo5pc5fq'
WORKITEMNAME=sys.argv[1]
PAT=sys.argv[2]
USEREMAIL=sys.argv[3]
DIRECTORYFORFILE=sys.argv[4]
authorization = str(base64.b64encode(bytes(':'+PAT, 'ascii')), 'ascii')


print(WORKITEMNAME,PAT,USEREMAIL,DIRECTORYFORFILE)

headers = {
    'content-type': 'application/json-patch+json',
    'Authorization': 'Basic '+authorization
}

BASE_URL="https://dev.azure.com/rahul173Demo/demo/"
GETSPRINT_ENDPOINT="_apis/work/teamsettings/iterations?api-version=7.0"
GETRUNID_ENDPOINT="_apis/test/runs?api-version=7.0"
CREATEWORKITEM_ENDPOINT="_apis/wit/workitems/$task?api-version=7.0"
ATTACHFILE_TO_AZURE_ENDPOINT="_apis/wit/attachments?fileName=report.html&api-version=7.0"
#file name should be replace by parameters

def GetCurrentSprint():
    response = requests.get(BASE_URL+GETSPRINT_ENDPOINT,headers=headers)
    data=json.loads(response.text)
    Sprint="No active Sprint"
    SprintCount=data['count']
    Sprint=data['value'][1]['name']
    for x in range(SprintCount):
        if data['value'][x]['attributes']['timeFrame']=="current":
            Sprint=data['value'][x]['name']    
    print("SPRINT=",Sprint)    
    return Sprint

def GetRunId():
    response = requests.get(BASE_URL+GETRUNID_ENDPOINT,headers=headers)
    data=json.loads(response.text)
    RunId=data['count']
    print("RUNID=",RunId)
    return RunId+1

RUNID=GetRunId()
GETRUNIDDETAILS_ENDPOINT="_apis/test/Runs/"+str(RUNID)+"/results?api-version=7.0"

def GetRunIdDetails():
    response = requests.get(BASE_URL+GETRUNIDDETAILS_ENDPOINT,headers=headers)
    data=json.loads(response.text)
    FailedTestcases=[]
    TestcasesCount=data['count']
    for x in range(TestcasesCount):
        if data['value'][x]["outcome"]=="Failed":
            FailedTestcases.append(data['value'][x]["testCase"]["name"])
    print("Run ID details Fecthed SucessFully")
    print("Failed Testcases=",FailedTestcases)
    return FailedTestcases


def CreateBUG():
    payload=[
    {
        "op": "add",
        "path": "/fields/System.Title",
        "value": WORKITEMNAME#get title from paramter
    },
    {
        "op": "add",
        "path": "/fields/System.AssignedTo",
        "value": USEREMAIL#get user from system variable
    },
    {
        "op": "add",
        "path": "/fields/System.AreaPath",
        "value": "demo\\"
    },
    {
        "op": "add",
        "path": "/fields/System.IterationPath",
        "value": "demo\\"+GetCurrentSprint()
    },
    {
        "op": "add",
        "path": "/fields/System.Description",
        "value": "Please Find the Failed Testcase here"+str(GetRunIdDetails())
    }]
    response = requests.post(BASE_URL+CREATEWORKITEM_ENDPOINT,headers=headers,json=payload)
    print("work item created Succesfully",)
    data=json.loads(response.text)
    WorkItemID=data['id']
    print("WORK ITEM ID=",WorkItemID)
    return WorkItemID

def AttachFileToAzure():
    header = { 'Authorization': 'Basic '+authorization, "Content-Type": "application/octet-stream" }
    #this file path will be replace from azure directory
    #file = open("C:\\Users\\manopriya\\Desktop\\test\\outputXunit.xml", "rb")
    file = open(DIRECTORYFORFILE,"rb")

    response = requests.post(BASE_URL+ATTACHFILE_TO_AZURE_ENDPOINT, headers=header, data=file)
    URL=''
    if response.status_code == 201:
        data=json.loads(response.text)
        URL=data['url']
    else:
        print("Failed to attach file")
        data=json.loads(response.text)
        URL=data['url']
    print("File Attched to Azure is Successfull")
    return URL

WorkItemID=CreateBUG()
ATTACHFILE_TO_WORKITEMS_ENDPOINT="_apis/wit/workitems/"+str(WorkItemID)+"?api-version=7.0"

def AttachFileToWorkItem():
    payload=[
        {
            "op": "add",
            "path": "/relations/-",
            "value": {
            "rel": "AttachedFile",
            "url": AttachFileToAzure(),
            "attributes": {
                "comment": "Spec for the work"
            }
            }
        } ]
    response = requests.patch(BASE_URL+ATTACHFILE_TO_WORKITEMS_ENDPOINT, headers=headers, json=payload)
    print("File attached to Workitem is Successfull")

AttachFileToWorkItem()