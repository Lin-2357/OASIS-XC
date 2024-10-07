from Constants import load, export, options, webdriver, scrap
import time
from selenium.webdriver.common.by import By

driver = webdriver.Firefox(options=options)

check = load('final.csv', 1, 'Organization ID', ['link'])

firefoxpath = 'C:/Users/linji/AppData/Roaming/Mozilla/Firefox/Profiles/j5utn2tf.default-release'
options = webdriver.firefox.options.Options()
options.add_argument("--profile={}".format(firefoxpath))

for x in check:
    link = 'https:'+check[x]['link'][0][5:]+'/roster/Roster/terms'
    driver.get(link)
    time.sleep(1)
    if not driver.find_elements(By.CSS_SELECTOR, "button.mdl-button"):
        continue
    email = driver.find_elements(By.CSS_SELECTOR, "button.mdl-button")[0]
    time.sleep(1)
    email.click()
    time.sleep(1)