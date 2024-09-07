from Constants import load, request, options, webdriver, note, export
from datetime import datetime
import json
driver = webdriver.Firefox(options=options)
import time

regged = {"id": 1243, "name": 'Registered Student Organizations'}
fro = {"id": 4595, "name": "FROZEN GROUP PENDING COMPLETION OF REGISTRATION STEPS"}
initials= 'JL'

def patch(_id, prev, cur):
    reg = cur == 'Registered Student Organizations'
    get_current = json.loads(request('?ids='+str(_id), 'GET'))['items'][0]['organizationType']['name']
    if get_current == 'Registered Student Organizations' and reg:
        return False
    if get_current == 'FROZEN GROUP PENDING COMPLETION OF REGISTRATION STEPS' and (not reg):
        return False
    body = [{"op": "replace", "path": "/organizationType", "value": regged if reg else fro}]
    request(str(_id), 'PATCH', body=body)
    date = "/".join(str(datetime.today()).split(" ")[0].split("-")[1:])
    strout = "\n" + date + " Moved from "+ prev +" to " + cur + "upon " + ("failing to complete" if not reg else "completing") + " registration requirement - "+initials
    note('https://callink.berkeley.edu/actioncenter/branch/associatedstudentsoftheuniversityofcalifornia/organizations/edit/'+str(_id), driver, strout)
    return True

act = load("mailXC.csv", 1, "Organization ID", ['XC Date', 'Organization ID', 'Org Name', 'Previous Status', 'Current Status', 'Comments', 'Date Completed'])

for x in act:
    if patch(x, act[x]['Previous Status'][0], act[x]['Current Status'][0]):
        act[x]['Date Completed'] = ["_".join(str(datetime.today()).split(" ")[0].split("-")[1:])]
    time.sleep(0.1)
    print('updated '+act[x]['Org Name'][0])

driver.close()