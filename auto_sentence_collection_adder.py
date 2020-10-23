from selenium import webdriver # install gecko driver to use in firefox
from selenium.webdriver.common.keys import Keys
import time

# Declare the e-mail & password of your GMAIL account
#Note: Please enter verified email address with your mobile number otherwise while login Google will ask for mobile number

email_address = ""
password_for_email = ""

#---- Nothing need to be changed---- 
browser = webdriver.Firefox()
browser.get('https://commonvoice.mozilla.org/sentence-collector/login')

time.sleep(10)

googleLogin = browser.find_element_by_xpath("/html/body/div[2]/form/fieldset/div[2]/ul/li[3]/button")
googleLogin.send_keys(Keys.ENTER)

time.sleep(10)

email = browser.find_element_by_id("identifierId")
email.send_keys(email_address)

emailSelect = browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]").click()

time.sleep(10)

password = browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")
password.send_keys(password_for_email)

PasswordSelect = browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]").click()

time.sleep(10)

addBtn = browser.find_element_by_xpath("/html/body/div/header/nav/a[3]")
addBtn.send_keys(Keys.ENTER)

time.sleep(10)

insertText = browser.find_element_by_xpath("//*[@id=\"sentences-input\"]")
insertText.send_keys('அருள்புரிந்தனை புரிதலுங் களித்துத் தலையினால் நடந்தேன் விடைப்பாகா ')

time.sleep(10)

sourceInputText = browser.find_element_by_id("source-input")
sourceInputText.send_keys('திருவாசகம்')

time.sleep(10)

agreeBtn = browser.find_element_by_id("agree").click()

time.sleep(10)

submitBtn2 = browser.find_element_by_xpath("/html/body/div/div/main/form/section[5]/button")
submitBtn2.send_keys(Keys.ENTER)

time.sleep(10)

confirmBtn = browser.find_element_by_xpath("/html/body/div/div/main/form/section/button")
confirmBtn.send_keys(Keys.ENTER)

