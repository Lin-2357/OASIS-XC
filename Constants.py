import csv
import urllib.request
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyperclip
import pyautogui
import time

renamer = {"""48449656: 
Enter the name of your first organization or ASUC/ GA Unit as it appears in CalLink.
For New Student Organizations: Please wait to submit this field until you've received your approved organization name during the New Org process.
""": 'org1', """48450305: Enter the Org ID of your first organization. If this org is a ASUC/GA office, program, or unit, enter the numeral zero 0. 
For New Student Organizations: Please wait to submit this field until you've received your CalLink Org ID number during the New Org process.""":"id1", """48450416: 



Enter the name of your second organization or ASUC/ GA Unit as it appears in CalLink.



""": "org2", """48450417: 
Enter the Org ID of your second organization. If this org is a ASUC/GA office, program, or unit, enter the numeral zero 0.
""": "id2", """48450699: 

Enter the name of your third organization or ASUC/ GA Unit as it appears in CalLink.

""":"org3","""48451126: Enter the Org ID of your third organization. If this org is a ASUC/GA office, program, or unit, enter the numeral zero 0.""":"id3", """48451127: 

Enter the name of your fourth organization or ASUC/ GA Unit as it appears in CalLink.

""":'org4', """48451128: Enter the Org ID of your fourth organization. If this org is a ASUC/GA office, program, or unit, enter the numeral zero 0.""":"id4", """48472906: 

Enter the name of your fifth organization or ASUC/ GA Unit as it appears in CalLink.

""":"org5", """48472910: 

Enter the Org ID of your fifth organization. If this org is a ASUC/GA office, program, or unit, enter the numeral zero 0.

""":"id5", """48472907: Enter the name of your sixth organization or ASUC/ GA Unit as it appears in CalLink.""":"org6", """48472911: 

Enter the Org ID of your sixth organization. If this org is a ASUC/GA office, program, or unit, enter the numeral zero 0.

""":"id6", """48472908: Enter the name of your seventh organization or ASUC/ GA Unit as it appears in CalLink.""":"org7", """48472912: 

Enter the Org ID of your seventh organization. If this org is a ASUC/GA office, program, or unit, enter the numeral zero 0.

""":"id7", """48472909: Enter the name of your eighth organization or ASUC/ GA Unit as it appears in CalLink.""":"org8", """48472913: 

Enter the Org ID of your eighth organization. If this org is a ASUC/GA office, program, or unit, enter the numeral zero 0.

""":"id8"

}

SixTypes = {
    "FROZEN GROUP PENDING COMPLETION OF REGISTRATION STEPS",
    "NEW ORG PENDING FINAL COMPLETION OF APPROVAL STEPS",
    "Registered Student Organizations",
    "Sponsored Student Organizations",
    "CalGreeks",
    "CalGreeks Affinity Groups"
}

def load(path, titlerow, key, ind):
    out = {}
    with open(path, encoding="utf-8", errors="replace") as f1:
        f1r = csv.reader(f1)
        row = []
        for i in range(titlerow):
            row = f1r.__next__()
        indexValue = {x: row.index(x) for x in ind}
        _id = row.index(key)
        tp = row.index("Organization Type") if "Organization Type" in row else -1
        for row in f1r:
            # if row[_id] in out:
            #     print("duplicate key", row[_id])
            if tp == -1 or row[tp] in SixTypes:
                for x in ind:
                    if row[_id] not in out:
                        out[row[_id]] = {}
                    if x not in out[row[_id]]:
                        out[row[_id]][x] = [row[indexValue[x]]]
                    else:
                        out[row[_id]][x].append(row[indexValue[x]])
    return out

def request(link, meth, body=-1):
    baseUrl = 'https://engage-api.campuslabs.com/api'
    apiKey = 'esk_live_4472c106d615292ac9735e865e78db93'

    url = baseUrl + "/v3.0/organizations/organization/" + link
    headers = {'Accept': 'application/json', 'X-Engage-Api-Key': apiKey}
    if body == -1:
        req = urllib.request.Request(url, headers=headers, method=meth)
    else:
        headers['Content-Type'] = 'application/json'
        data = str(json.dumps(body))
        data = data.encode('ascii') # data should be bytes
        req = urllib.request.Request(url, data, headers=headers, method=meth)

    with urllib.request.urlopen(req) as response:
        js = response.read().decode('utf-8')
        return js

def export(js, path, cols):
    with open(path, 'w', newline='', errors='ignore') as f:
        fw = csv.writer(f)
        fw.writerow(cols)
        for x in js:
            row = [x if i=='Organization ID' else js[x][i][0] for i in cols]
            fw.writerow(row)

firefoxpath = 'C:/Users/linji/AppData/Roaming/Mozilla/Firefox/Profiles/j5utn2tf.default-release'
options = webdriver.firefox.options.Options()
options.add_argument("--profile={}".format(firefoxpath))

def scrap(link, driver):
    driver.get(link)
    # This will get the html after on-load javascript
    html2 = driver.execute_script("return document.documentElement.innerHTML;").lower()
    noti = len(re.findall('(?=(notify))', html2))
    total = len(re.findall('(?=(signatory))', html2))
    return (total-noti+1)

def note(link, driver, text):
    driver.get(link)
    email = driver.find_elements(By.CSS_SELECTOR, "div.group-set")[2]
    time.sleep(0.5)
    email.click()
    time.sleep(0.5)
    pyautogui.press('down', 10)
    pyautogui.press('right', 100)
    pyautogui.write(text, 0.03)
    time.sleep(1)
    submit = driver.find_element(By.CSS_SELECTOR, (".mdl-button.mdl-js-button.mdl-button--raised.mdl-button--colored"))
    submit.click()

def sim(str1, str2):
    dpmat = [[float('inf') for x in range(len(str2)+1)] for x in range(len(str1)+1)]
    for i in range(len(str1)+1):
        dpmat[i][0] = i
        for j in range(len(str2)+1):
            dpmat[0][j] = j
    for i in range(1, len(str1)+1):
        for j in range(1, len(str2)+1):
            a = dpmat[i-1][j]+1
            b = dpmat[i-1][j-1]+(1 if str1[i-1] != str2[j-1] else 0)
            c = dpmat[i][j-1]+1
            dpmat[i][j] = min(a,b,c)
    return dpmat[len(str1)][len(str2)]#/max(len(str1),len(str2))

def late(time1, time2):
    t1 = time1.split(" ")[0].split("-") + time1.split(" ")[1].split(":")
    t2 = time2.split(" ")[0].split("-") + time2.split(" ")[1].split(":")
    t1 = [int(x) for x in t1]
    t2 = [int(y) for y in t2]
    i = 0
    for x in t1:
        if x > t2[i]:
            return True
        elif x < t2[i]:
            return False
        else:
            i += 1
    return False