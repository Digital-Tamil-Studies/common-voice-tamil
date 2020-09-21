from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

browser = webdriver.Firefox()
browser.get('https://common-voice.github.io/sentence-collector/#/login')

time.sleep(10)

username = browser.find_element_by_id("username")
username.send_keys('PUT_your_USERNAME')

time.sleep(10)

password = browser.find_element_by_id("password")
password.send_keys('PUT_your_PASSWORD')

time.sleep(10)

submitBtn = browser.find_element_by_xpath("/html/body/div/div/main/form/section[2]/button")
submitBtn.send_keys(Keys.ENTER)

time.sleep(10)

addBtn = browser.find_element_by_xpath("/html/body/div/header/nav/a[3]")
addBtn.send_keys(Keys.ENTER)

time.sleep(10)

insertText = browser.find_element_by_xpath("//*[@id=\"sentences-input\"]")
insertText.send_keys('மானம் குலம் கல்வி வண்மை அறிவுடைமை தானம் தவர்உயர்ச்சி தாளாண்மை')

time.sleep(10)

sourceInputText = browser.find_element_by_id("source-input")
sourceInputText.send_keys('ஆத்திசூடி')

time.sleep(10)

agreeBtn = browser.find_element_by_id("agree").click()

time.sleep(10)

submitBtn2 = browser.find_element_by_xpath("/html/body/div/div/main/form/section[5]/button")
submitBtn2.send_keys(Keys.ENTER)

confirmBtn = browser.find_element_by_xpath("/html/body/div/div/main/form/section/button")
confirmBtn.send_keys(Keys.ENTER)

