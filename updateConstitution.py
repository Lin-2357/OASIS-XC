from Constants import options, webdriver, load
import pyautogui
from selenium.webdriver.common.by import By
import time
driver = webdriver.Firefox(options=options)

def update(link, filepath):
    driver.get('https://callink.berkeley.edu/actioncenter/organization/'+link+'/documents')
    time.sleep(0.5)
    add = driver.find_element(By.CSS_SELECTOR, 'button.mdl-button:nth-child(2)')
    add.click()
    time.sleep(0.5)
    pyautogui.click(pyautogui.size()[0]//2, pyautogui.size()[1]//2)
    time.sleep(0.5)
    upload = driver.find_element(By.CSS_SELECTOR, '#chooseFile')
    upload.send_keys(filepath)
    con = driver.find_element(By.CSS_SELECTOR, '#DocumentTypes')
    con.click()
    time.sleep(0.5)
    pyautogui.hotkey('down')
    pyautogui.hotkey('down')
    pyautogui.hotkey('enter')
    send = driver.find_element(By.CSS_SELECTOR, 'button.mdl-button--raised:nth-child(1)')
    send.click()
    time.sleep(2)

cons = load('update.csv', 'key', ['file_absolute_link'])
for x in cons:
    update(x, x['file_absolute_link'][0])