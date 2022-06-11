import os
import time
from tbselenium import tbdriver
from tbselenium.tbdriver import TorBrowserDriver
from selenium.common.exceptions import ElementNotInteractableException , ElementClickInterceptedException , NoSuchElementException 
import urllib.request
from selenium.webdriver.common.keys import Keys
url = "https://www.upload-4ever.com/ldrw68xzm7q4"
agreebtn = '//*[@id="gdpr-cookie-notice"]/div/div[2]/a'
free_download_btn = '/html/body/div[3]/main/section/div/div/div/div[1]/div[2]/form/span[2]/input'
create_download_link = '//*[@id="downloadbtn"]'
audioToTextDelay = 10
delayTime = 2
audioFile = "\\payload.mp3"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"

driver = TorBrowserDriver("")

driver.get(url)
time.sleep(2)
driver.find_element_by_xpath(agreebtn).click()
driver.find_element_by_xpath(free_download_btn).click()
time.sleep(4)
print("[INFO] scrolling...")
driver.execute_script("window.scroll(0,900);")
time.sleep(2)

def adblocker_clicker_for_create_download_link_def(path):
    list = driver.find_elements_by_xpath(path)
    for element in list:
        try:
            driver.switch_to.default_content()
            time.sleep(2)
            element.click()
            continue
        except ElementNotInteractableException as e:
            pass

def adblock_clicker(driver,ad):
    status = 1
    while status == 1:
        try:
            print("[INFO] errassing ....")
            print(f"[INFO] errassing {ad}")
            driver.find_element_by_xpath(ad).click()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(4)
            driver.execute_script("window.stop();")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except ElementNotInteractableException as e:
            status = status - 1
            pass
        time.sleep(3)

def clicking_span_recaptcha():
    try:
        time.sleep(2)
        ad_xpath = '/html/body/div[contains(@style,"height: 78px; width: 304px; z-index: 2147483647;")]'
        adblock_clicker(driver,ad_xpath)
        try :
            name = driver.find_element_by_xpath('/html/body/div[3]/main/section/div/div/div[2]/form/div[2]/div[3]/center/div[2]/div/div/iframe').get_attribute('name')
            print(name)
            new_name = "c"+"-"+str(name).split("-")[1]
            print(new_name)
            driver.switch_to.frame(name)
            driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]').click()
            time.sleep(7)
            driver.switch_to.default_content()
            time.sleep(5)
            pass
        except ElementClickInterceptedException as e:
            print("[ERROR] trying again")
            print(f" exception is {e}")
            clicking_span_recaptcha()
    except NoSuchElementException as e:
            try :
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[0])
                driver.switch_to.default_content()
                name = driver.find_element_by_xpath('/html/body/div[3]/main/section/div/div/div[2]/form/div[2]/div[3]/center/div[2]/div/div/iframe').get_attribute('name')
                print(name)
                new_name = "c"+"-"+str(name).split("-")[1]
                print(new_name)
                driver.switch_to.frame(name)
                driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]').click()
                time.sleep(7)
                driver.switch_to.default_content()
                time.sleep(5)
                pass
            except ElementClickInterceptedException as e:
                print("[ERROR] in line 97 trying again")
                print(f" exception is {e}")
                clicking_span_recaptcha()
    return new_name

def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    time.sleep(2)
    audioInput = driver.find_element_by_xpath( '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = driver.find_element_by_xpath('//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element_by_xpath('//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result

def converting():
    try:
        src = driver.find_element_by_id('audio-source').get_attribute("src")
        print(f"[INFO] Audio src = {src} ")
        urllib.request.urlretrieve(src,os.getcwd()+"/payload.mp3")
        text = audioToText(os.getcwd()+"/payload.mp3")
        print(f"[INFO] Recaptcha Key is ( {text} )")
        driver.switch_to.default_content()
        driver.switch_to.frame(new_name)
        inputField = driver.find_element_by_id("audio-response")
        inputField.send_keys(text)
        time.sleep(3)
        inputField.send_keys(Keys.ENTER)
        pass
    except ElementClickInterceptedException as e:
        print(f"[ERROR in line 106] ( {e} )")
        ad3 = driver.find_element_by_xpath("/html/body/div[contains(@style,'height: 250px; width: 300px; z-index: 2147483647;')]")
        if ad3.is_enabled:
            adblock_clicker(driver,"/html/body/div[contains(@style,'height: 250px; width: 300px; z-index: 2147483647;')]")
            converting()
            pass

def audio_btn():
    try:        
        ad2 = driver.find_element_by_xpath('/html/body/div[contains(@style,"height: 535px; width: 355px; z-index: 2147483647;")]')
        if ad2.is_enabled:
            print("[INFO] ad found!")
            ad2_path = '/html/body/div[contains(@style,"height: 535px; width: 355px; z-index: 2147483647;")]'
            try:
                driver.switch_to.frame(new_name)
                # time.sleep(2)
                driver.find_element_by_xpath('//*[@id="recaptcha-audio-button"]').click()
                time.sleep(7)
                pass
            except (ElementClickInterceptedException,NoSuchElementException) as e:
                if e == ElementClickInterceptedException :
                    # print(e)
                    driver.switch_to.default_content()
                    adblock_clicker(driver,ad2_path)
                    audio_btn()
                elif e == NoSuchElementException:
                    pass
    except NoSuchElementException :
        try:
            driver.switch_to.frame(new_name)
            # time.sleep(2)
            driver.find_element_by_xpath('//*[@id="recaptcha-audio-button"]').click()
            time.sleep(7)
            pass
        except (ElementClickInterceptedException,NoSuchElementException) as e:
            if e == ElementClickInterceptedException :
                # print(e)
                driver.switch_to.default_content()
                adblock_clicker(driver,ad2_path)
                audio_btn()
            elif e == NoSuchElementException:
                pass

def create_download_link_def():
    try:
        driver.switch_to.default_content()
        driver.find_element_by_xpath(create_download_link).click()
        if len(driver.window_handles) == 1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(3)
        else:
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(3)
    except ElementClickInterceptedException as e:
        driver.switch_to.default_content()
        ad = driver.find_element_by_xpath('/html/body/div[contains(@style,"height: 31.1094px; width: 149.641px; z-index: 2147483647;")]')
        ad_path = '/html/body/div[contains(@style,"height: 31.1094px; width: 149.641px; z-index: 2147483647;")]'
        adblocker_clicker_for_create_download_link_def(ad_path)
        create_download_link_def()

def final_click():
    try:
        driver.find_element_by_xpath('//*[@id="downLoadLinkButton"]').click()
    except Exception as e:
        print(e)

new_name = clicking_span_recaptcha()
audio_btn()
converting()
create_download_link_def()
final_click()