from Constants import load, export

emails = load('inputFile/email_ref.csv', 24, 'Username', ['First Name', 'Last Name', 'Campus Email'])
act = load("ActionItems.csv", 1, "Organization ID", ['XC Date', 'Organization ID', 'Org Name', 'Previous Status', 'Current Status', 'Comments', 'Date Completed'])
sig = load('inputFile/UsersBySystemPositionTemplate.csv', 3, "Organization ID", ["Username"])

out = {}

for x in act:
    if act[x]['Current Status'][0] != act[x]['Previous Status'][0]:
        y = sig[x]['Username'] if x in sig else []
        out[x] = {'Email': [','.join([emails[i]['Campus Email'][0] for i in y])], 'Organization Name': act[x]['Org Name']}
        for b in act[x]:
            out[x][b] = act[x][b]

export(out, 'mailXC.csv', ['Email', 'Organization ID', 'Organization Name']+['XC Date', 'Organization ID', 'Org Name', 'Previous Status', 'Current Status', 'Comments', 'Date Completed'])