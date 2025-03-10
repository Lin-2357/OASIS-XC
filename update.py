from Constants import load, request, options, webdriver, note, export
from datetime import datetime
import json
driver = webdriver.Firefox(options=options)
import time

regged = {"id": 1243, "name": 'Registered Student Organizations'}
fro = {"id": 4595, "name": "FROZEN GROUP PENDING COMPLETION OF REGISTRATION STEPS"}
initials= 'Script'

def patch(_id, prev, cur):
    reg = cur == 'Registered Student Organizations'
    print(reg)
    get_current = json.loads(request('?ids='+str(_id), 'GET'))['items'][0]['organizationType']['name']
    print(reg, get_current)
    if get_current == 'Registered Student Organizations' and reg:
        return False
    if get_current == 'FROZEN GROUP PENDING COMPLETION OF REGISTRATION STEPS' and (not reg):
        return False
    body = [{"op": "replace", "path": "/organizationType", "value": regged if reg else fro}]

    date = "/".join(str(datetime.today()).split(" ")[0].split("-")[1:])
    strout = "\n" + date + " Moved from "+ prev +" to " + cur + " upon " + ("failing to complete" if not reg else "completing") + " registration requirement - "+initials
    note('https://callink.berkeley.edu/actioncenter/branch/associatedstudentsoftheuniversityofcalifornia/organizations/edit/'+str(_id), driver, strout)
    print(str(_id), body)
    request(str(_id), 'PATCH', body=body)
    return True

act = load("mailXC.csv", 1, "Organization ID", ['XC Date', 'Organization ID', 'Org Name', 'Previous Status', 'Current Status', 'Comments', 'Date Completed'])
newraw = load('NewRaw.csv', 1, "Organization ID", ["Organization Name", "Completed Reg Req", 'Reg Form', 'Signatory', 'T&C', "Organization Type", "Callink URL", 'Callink Designation' ,"Primary Campus Advisor"])

for x in act:
    print(x)
    if patch(x, act[x]['Previous Status'][0], act[x]['Current Status'][0]):
        act[x]['Date Completed'] = ["_".join(str(datetime.today()).split(" ")[0].split("-")[1:])]
    for i in range(10):
        print("waiting for refresh:", i)
        time.sleep(3)
        try:
            driver.find_element(By.CSS_SELECTOR, ("input.mdl-button"))
        except Exception:
            print('updated '+act[x]['Org Name'][0])
            newraw[x]['Organization Type'] = act[x]['Current Status']
            break

driver.close()
export(newraw, 'NewRaw.csv', ["Organization ID", "Organization Name", "Completed Reg Req", 'Reg Form', 'Signatory', 'T&C', "Organization Type", "Callink URL", 'Callink Designation' ,"Primary Campus Advisor"])
