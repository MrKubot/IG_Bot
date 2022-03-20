import os

################ Comments and variables are in polish cause I wasn't planning to push it on github
################ And now I'm too lazy to change it - probably noone will see it ever xD


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_driver_path = os.environ.get('CHROME_PATH')
ACCOUNT = os.environ.get('ACCOUNT_NAME')
EMAIL = os.environ.get('MAIL')
PASSWORD = os.environ.get('RH_PASSWORD')

ser = Service(chrome_driver_path)
opt = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=opt)

driver.get("https://www.instagram.com")

#definicja scrolla
def scroll():
    while True:
        try:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", popup)
            break
        except:
            pass
        
#Cookies
while True:
    try:
        driver.find_element(By.XPATH, value='/html/body/div[4]/div/div/button[1]').click()
    except:
        break

#wprowadzenie danych konta
time.sleep(1)
driver.find_element(By.NAME, value="username").send_keys(EMAIL)
time.sleep(2)
driver.find_element(By.NAME, value="password").send_keys(PASSWORD)
time.sleep(1)
driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div/div[3]').click()

#akceptowanie zgód
# while True:
#     try:
#         driver.find_element(By.XPATH, value='/html/body/div[5]/div/div/div/div[3]/button[2]').click()
#         time.sleep(2)
#         break
#     except:
#         pass
        
# Wyszukiwanie konta
while True:
    try:
        szukanie = driver.find_element(By.XPATH, value='//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        szukanie.send_keys(ACCOUNT)
        time.sleep(1)
        szukanie.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        szukanie.send_keys(Keys.ENTER)
        break
    except:
        pass

# nacisniecie liczby obserwujacych, aby wyskoczyla ich lista
while True:
    try:
        driver.find_element(By.XPATH, value='//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div').click()
        break
    except:
        pass

# zapisanie do "popup" wyskakujacego okienka z obserwatorami
while True:
    try:
        popup = driver.find_element(By.XPATH, value='/html/body/div[6]/div/div/div/div[2]')
        break
    except:
        pass

poczatek = 0
i = 0
buttony_nowe = []
# POCZATEK SCROLLOWANIA 'i' okresla ile razy ma sie scrollowac
while i < 35:
    try:
        time.sleep(1)
        buttony = popup.find_elements(By.CSS_SELECTOR, value="li button")
        scroll()
        if len(buttony) > len(buttony_nowe):
            # sprawdza czy rzeczywiscie zaobserwowalo nowych, czy wykonalo scrolla zanim internet pozwolil sie
            # zaladowac popupowi. jezeli sie zaladowalo i zrobilo prawdziwego scrolla to go "zalicza"
            i += 1
            buttony_nowe = buttony
    except:
        break
    
# ZACZECIE OBSERWOWANIA
i = 0
nowi_obserwatorzy = 0
while nowi_obserwatorzy < 40:
    try:
        time.sleep(1)
        # zapisanie do 'buttony' wszystkich widocznych przyciskow obseracji
        buttony = popup.find_elements(By.CSS_SELECTOR, value="li button")
        while i < len(buttony):
            try:
                buttony[i].click()
                i += 1
                nowi_obserwatorzy += 1
                time.sleep(1)
            # jezeli jest juz obserwowany, to pierwsze 'try' sie wykona, ale nastepne juz nie, poniewaz bedzie okieno
            # "czy chcesz przestac obserwowac". W takim wypadku ma wyszukac elementu 'anuluj' i go nacisnac, po czym szukac dalej
            except:
                try:
                    time.sleep(1)
                    popik = driver.find_element(By.XPATH, value='/html/body/div[7]/div/div')
                    time.sleep(1)
                    popik.find_elements(By.CSS_SELECTOR, value="button")[1].click()
                    # zmniejszenie 'nowi_obserwatorzy' poniewaz nie byla to "prawdziwa" obserwacja
                    # nie zmniejszam 'i' poniewaz nie chce, aby ponownie probowalo obserwowac to samo konto.
                    # Doprowadziloby to do nieskonczonego loopa
                    nowi_obserwatorzy -= 1
                except:
                    pass
        break
    except:
        pass

        