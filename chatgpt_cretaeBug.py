import requests
import json

# Azure DevOps REST API endpoint for creating work items
url = "https://dev.azure.com/rahul173Demo/demo/_apis/wit/workitems/$Task?api-version=7.0"

# Replace {organization} and {project} with your organization and project name
#url = url.format(organization="<your_organization>", project="<your_project>")

# Request headers
headers = {
    "Authorization": "oosyebh2tyyn37rycb2ptais2uny7mc36fzpsvwuvalpdo5pc5fq",
    "Content-Type": "application/json-patch+json"
}

# Request body
data = [
    {
        "op": "add",
        "path": "/fields/System.Title",
        "value": "Test Task"
    },
    {
        "op": "add",
        "path": "/fields/System.Description",
        "value": "This is a test task."
    }
]

# Make the POST request
response = requests.post(url, headers=headers, json=data)

print(response)
'''# Check the response status code
if response.status_code == 200:
    # Parse the response JSON data
    response_data = json.loads(response.text)
    print("Work item created successfully with ID:", response_data["id"])
else:
    print("Failed to create work item:", response.text)'''
