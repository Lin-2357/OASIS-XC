import csv
from Constants import load, export

regprog = load("inputFile/RegistrationProgress.csv", 7, "Organization ID", ["Status"])
sig = load("inputFile/UsersBySystemPositionTemplate.csv", 3, "Organization ID", ["Username"])
orgdir = load("inputFile/OrganizationDirectory.csv", 3, "Organization ID", ["Organization Name", "Organization Type", "Website Key", "Primary Campus Advisor", 'Callink Designation'])
last = load("inputFile/raw.csv", 1, 'Organization ID', ['T&C', 'Completed Reg Req'])

for x in orgdir:
    orgdir[x]["Callink URL"] = ["https://callink.berkeley.edu/actioncenter/organization/" + orgdir[x]["Website Key"][0]]
    orgdir[x]["Signatory"] = [len(sig[x]['Username']) if x in sig else 0]
    orgdir[x]['Completed Reg Req'] = ["Yes" if (x in regprog and regprog[x]["Status"][0] == "Approved" and (len(sig[x]['Username']) if x in sig else 0)>=4) else "No"]
    orgdir[x]['T&C'] = last[x]['T&C'] if x in last else ['In Progress']
    orgdir[x]['Reg Form'] = regprog[x]['Status'] if x in regprog else ['Not Started']

export(orgdir, 'regsig.csv', ["Organization ID", "Organization Name", "Completed Reg Req", 'Reg Form', 'Signatory', 'T&C', "Organization Type", "Callink URL", 'Callink Designation' ,"Primary Campus Advisor"])

act = {}
for x in orgdir:
    if ((x not in last or last[x]['Completed Reg Req'][0] != 'Yes' or last[x]['T&C'][0] != 'Yes') and orgdir[x]['Completed Reg Req'][0] == 'Yes'):
        act[x] = {"Organization Name": orgdir[x]['Organization Name'], 'Completed T&C': [''], "link": ["https://callink.berkeley.edu/actioncenter/organization/"+orgdir[x]['Website Key'][0]+"/roster/Roster/terms"]}
        print("Exported "+orgdir[x]['Organization Name'][0]+" to check for T&C")

export(act, 'checkT&C.csv', ['Organization ID', 'Organization Name', 'link', 'Completed T&C'])