from Constants import load, export
import datetime

orgdir = load('regsig.csv', 1, 'Organization ID', ["Organization Name", "Completed Reg Req", 'Reg Form', 'Signatory', 'T&C', "Organization Type", "Callink URL", 'Callink Designation' ,"Primary Campus Advisor"])
act = load('checkT&C.csv', 1, 'Organization ID', ['Organization Name', 'Completed T&C'])
actit = {}

for x in act:
    if int(act[x]['Completed T&C'][0]) >= 4:
        orgdir[x]["T&C"] = ['Yes']
        actit[x] = {'XC Date': ["_".join(str(datetime.datetime.today()).split(" ")[0].split("-")[1:])], 'Org Name': orgdir[x]['Organization Name'], 'Previous Status': orgdir[x]['Organization Type'], 'Current Status': ["Registered Student Organizations"], 'Comments': ['Reg Req finished'], 'Date Completed': ['']}

export(actit, 'ActionItems.csv', ['XC Date', 'Organization ID', 'Org Name', 'Previous Status', 'Current Status', 'Comments', 'Date Completed'])
export(orgdir, 'NewRaw.csv', ["Organization ID", "Organization Name", "Completed Reg Req", 'Reg Form', 'Signatory', 'T&C', "Organization Type", "Callink URL", 'Callink Designation' ,"Primary Campus Advisor"])