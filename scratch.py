import urllib.request
import json

def request(link, meth, body=-1):
    baseUrl = 'https://engage-api.campuslabs.com/api'
    apiKey = 'esk_live_4472c106d615292ac9735e865e78db93'

    url = baseUrl + "/v3.0/organizations/" + link
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
        return json.loads(js)

print([(x['name'],x['positionId'],x.keys()) for x in request('organization/91369/positionholder', 'GET')['items'] if x['name'] == 'Signatory'])