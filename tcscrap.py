from Constants import load, export, options, webdriver, scrap
driver = webdriver.Firefox(options=options)

check = load('checkT&C.csv', 1, 'Organization ID', ['Organization Name', 'Completed T&C', 'link'])

for x in check:
    tcnm = scrap(check[x]['link'][0], driver)
    print(check[x]['Organization Name'][0], tcnm)
    check[x]['Completed T&C'] = [tcnm]

driver.close()

export(check, 'checkT&C.csv', ['Organization ID', 'Organization Name', 'link', 'Completed T&C'])