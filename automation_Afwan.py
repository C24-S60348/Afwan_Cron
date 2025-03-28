import sys
import variables
from datetime import datetime, timezone, timedelta
# import logging
import json

# logging.basicConfig(filename="cron_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

#import urllib3
#import requests

#pip install selenium
#pip install beautifulsoup4
#pip install urllib3
#pip install requests
#pip install webdriver-manager



#VARIABLES-------------------------------------
program = variables.program
if program == "":
    program = "CB" 

                # A - AutoBooking , CB - Check Booking PNR , CT - Celik Tafsir fetch ,
                # TB - Telegram Bot , WS - Web Scraping , AAI - AI Chat test ,
                # CRS - Cron Run Server , CRPC - Cron Run PC , CSFTP - Check SFTP , FW - Flask Website afwanproductions,
                # CM - Check message telegram , BP - Bot Polling
#VARIABLES------------------



#print(len(sys.argv))
if len(sys.argv) > 1:
    program = sys.argv[1]

program = program.upper()


if (program == "FW"):
    from flask import Flask, request, jsonify, render_template, render_template_string
    from flask_cors import CORS
    app = Flask(__name__)
    # cors = CORS(app)
    CORS(app, supports_credentials=True, 
        resources={r"/*": {"origins": "http://localhost:8081"}}, 
        allow_headers=["Content-Type", "Authorization"]
    )

#Public variables
if True:
    fyuser = ""
    fypass = ""
    fycode = ""
    tbtoken = ""
    csftplink = ""
    timenowKL = 0
    last_run_times = {
        "0.5":0,
        "1":0,
        "2":0,
        "3":0,
        "5":0,
        "10":0,
        "30":0,
        "60":0,
    }
    reminder = {} #todo - get data from user
    #http = urllib3.PoolManager()

def run_function(program_code, code2=None, info3=None):
    program = program_code
    global variables
    global timenowKL
    #global http



    #functions
    if (True):
        import urllib.request as ur
        import variables
        import time
        import datetime
        from datetime import datetime, timezone, timedelta
        from decimal import Decimal
        browser_code = 'F' # C - Chrome , F - Firefox , E - Microsoft Edge , S - Safari
        openfileorfolder = 'F' # F - File , FD - Folder
        xmlformatted = True
        def getbrowser(browser_code):
            if browser_code == 'C':
                trymethod = 0
                if trymethod == 0:
                    chrome_options = ChromeOptions()
                    chrome_options.add_experimental_option("detach", True)
                    chrome_options.add_argument("user-data-dir=C:\\Users\\YourUser\\AppData\\Local\\Google\\Chrome\\User Data")
                    chrome_options.add_argument("--profile-directory=Default")
                    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
                elif trymethod == 1:
                    options = webdriver.ChromeOptions()
                    options.add_experimental_option("detach", True)
                    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
                else:
                    options = ChromeOptions()
                    options.add_experimental_option("detach", True)  # Prevents browser from closing
                    #service = Service("chromedriver.exe")  # Path to your ChromeDriver
                    browser = webdriver.Chrome(options=options)
            elif browser_code == 'F':
                trymethod = 1
                if trymethod == 1:
                    options = webdriver.FirefoxOptions()
                    service = FirefoxService(FirefoxDriverManager().install())
                    browser = webdriver.Firefox(service=service, options=options)
                else:
                    browser = webdriver.Firefox()
            elif browser_code == 'S':
                browser = webdriver.Safari()
            elif browser_code == 'E':
                trymethod = 1
                if trymethod == 1:
                    options = EdgeOptions()
                    options.add_experimental_option("detach", True)  # Prevents browser from closing
                    service = EdgeService(EdgeDriverManager().install())
                    browser = webdriver.Edge(service=service, options=options)
                else:
                    options = EdgeOptions()
                    options.add_experimental_option("detach", True)  # Prevents browser from closing
                    browser = webdriver.Edge(options=options)
                # browser = webdriver.Edge(options=options)
            else:
                browser = webdriver.Firefox()

            return browser


    #CHECK BOOKING PNR
    if program == "CB":
        #needPass()

        import xml.dom.minidom
        #import urllib.request
        import os
        import platform
        import base64
        #needPass()

        #VARIABLES------------------
        pnr = input("Please input PNR: ")
        stagingorprod = input("Staging - s , Prod - p: ").upper() #S - Staging , P - Prod
        #VARIABLES------------------
        fycode = variables.fy_code
        bookingtype = "Production"

        if stagingorprod == "S":
            bookingtype = "Staging"
            link = variables.fy_app_staging
            url = f"{link}?Key={fycode}&RecordLocator={pnr}"
        else:
            bookingtype = "Production"
            link = variables.fy_app_prod
            url = f"{link}?Key={fycode}&RecordLocator={pnr}"

        #content = http.request("GET", url)
        #content = content.data.decode("utf-8")
        #content = base64.b64decode(content).decode('utf-8')
        req = ur.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        #try:
            #with urllib.request.urlopen(req) as response:
                #content = response.read()
        #except urllib.error.HTTPError as e:
            #print(f"HTTP Error: {e.code} - {e.reason}")
        #except urllib.error.URLError as e:
            #print(f"URL Error: {e.reason}")

        with ur.urlopen(req) as response:
                content = response.read().decode('utf-8')
        content = base64.b64decode(content)


        if xmlformatted:
            dom = xml.dom.minidom.parseString(content)
            content = dom.toprettyxml(indent="    ")

        file_name = f"output booking/{pnr} - {bookingtype}.xml"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Content has been written to {file_name}")

        # Open the file location
        file_path = os.path.abspath(file_name)
        if openfileorfolder == "FD":
            file_path = os.path.dirname(file_path)

        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{file_path}"')
        else:  # Linux
            os.system(f'xdg-open "{file_path}"')

    #BOOKING FIREFLY - Auto Booking
    elif program == "A":
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.alert import Alert
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.edge.options import Options as EdgeOptions
        from selenium.webdriver.chrome.service import Service as ChromeService
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from selenium.webdriver.edge.service import Service as EdgeService
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager as FirefoxDriverManager
        from webdriver_manager.microsoft import EdgeChromiumDriverManager as EdgeDriverManager
        from webdriver_manager.opera import OperaDriverManager
        # from webdriver_manager.drivers import edge
        import time
        #needPass()

        #VARIABLES------------------
        is_one_way = input("Is one way? y/n: ").upper() # Y - Yes, N - No
        is_one_way = is_one_way == "Y"
        # is_login = input("Is login? y/n: ").upper() # Y - Yes , N - No
        is_login = "N" # Y - Yes , N - No - need to No because of OTP
        is_login = is_login == "Y"
        fyuser = variables.fy_dev_user
        fypass = variables.fy_dev_pass
        if fyuser == "":
            fyuser = ""  # put your custom email and pass fy staging here
            fypass = ""
        station_depart = input("Input Departure: ").upper()
        station_return = input("Input Return: ").upper()
        adult = int(input("Input Adult: "))
        infant = int(input("Input Infant: "))
        flight_fare_type = input("Input Fare type (S) (B) (F): ").upper()   #S - Saver , B - Basic , F - Flex
        target_date = '2025' + input("Input date (0319 = march 19): ")
        if not is_one_way:
            flight_fare_type2 = input("Input Fare type (S) (B) (F): ").upper()
            target_date2 = '2025' + input("Input date (0320 = march 20): ")
        
        
        first_name = 'afwan'
        last_name = 'haziq'
        contact_first_name = 'afwann'
        contact_last_name = 'haziqq'
        contact_email = 'afwan@haziq.com'
        mobile_phone = '01152853044'
        #VARIABLES-------------------------

        
        

        # options = ChromeOptions()
        # options.add_experimental_option("detach", True)  # Prevents browser from closing

        #service = Service("chromedriver.exe")  # Path to your ChromeDriver
        # browser = webdriver.Chrome(options=options)

        browser = getbrowser(browser_code)

        #functions
        if True:
            def scrollClickClass(class_name):
                e = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

                for _ in range(5):  # multiple scrolls
                    browser.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", e)
                    time.sleep(0.5)

                e = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
                e.click()

            def scrollSearchClass(class_name):
                e = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

                for _ in range(5):  # multiple scrolls
                    browser.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", e)
                    time.sleep(0.5)

            def scrollSearchID(id):
                e = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, id)))

                for _ in range(5):  # multiple scrolls
                    browser.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", e)
                    time.sleep(0.5)

            def clickClass(class_name):
                e = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
                e.click()

            def clickXPath(key):
                e = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, key)))
                e.click()

            def clickID(id):
                e = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, id)))
                e.click()

            def waitBackdrop():
                WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "offcanvas-backdrop")))

            def clickDate(date):
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "calendar-day")))
                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "calendar-day")))
                date_element = browser.find_element(By.XPATH, f"//div[@class='calendar-day' and @data-date3='{date}']")
                date_element.click()

            def sendKeyID(id, key):
                e = browser.find_element(By.ID, id)
                e.send_keys(key)

            def scrollAndType(id, key):
                scrollSearchID(id)
                sendKeyID(id, key)

            def clickBeforeSelected(data_market):
                element = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'before_selected')][@data-market='{data_market}']"))
                )
                print("Clicking the element...")
                element.click()

            def scrollSearchXPath2(key):
                elements = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, key)))

                for e in elements:
                    for _ in range(5):  # Scroll multiple times
                        browser.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", e)
                        time.sleep(0.5)

                        # Check if element is visible and clickable
                        if e.is_displayed() and e.is_enabled():
                            print("Element found and clickable, clicking now...")
                            e.click()
                            return  # Exit after clicking

            def scrollSearchXPath(key):
                e = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, key)))

                for _ in range(5):  # multiple scrolls
                    browser.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", e)
                    time.sleep(0.5)

            def getFareID(key):
                if key == 'S':
                    return 1
                elif key == 'B':
                    return 2
                elif key == 'F':
                    return 4
                else:
                    return 1

        fydevlink = variables.fydevlink
        username = variables.fy_mweb_user
        password = variables.fy_mweb_pass
        url = f"https://{username}:{password}@{fydevlink}"

        browser.get(url)
        assert 'Firefly' in browser.title

        #login
        if is_login:
            browser.get(url+'/Login')
            sendKeyID('username', fyuser)
            sendKeyID('password', fypass)
            clickID('button_login')

        #search page
        if True:
            if is_one_way:
                clickID('one-way')

            clickClass('departure-station-div')
            scrollSearchID('station'+station_depart)
            clickID('station'+station_depart)

            waitBackdrop()

            clickClass('arrival-station-div')
            scrollSearchID('station'+station_return)
            clickID('station'+station_return)

            waitBackdrop()

            clickClass('calendar-div')
            scrollSearchXPath(f"//div[@class='calendar-day' and @data-date3='{target_date}']")
            clickXPath(f"//div[@class='calendar-day' and @data-date3='{target_date}']")
            # clickDate(target_date)
            if not is_one_way:
                scrollSearchXPath(f"//div[@class='calendar-day' and @data-date3='{target_date2}']")
                clickXPath(f"//div[@class='calendar-day' and @data-date3='{target_date2}']")
            clickClass('calendar-done')

            waitBackdrop()

            clickClass('passengers-div')
            for x in range(adult-1):
                clickClass('adult-plus')
            for x in range(infant):
                clickClass('infant-plus')
            clickClass('passengers-done')

            waitBackdrop()

            clickID('button_search')

        flight_fare_id = getFareID(flight_fare_type)
        if not is_one_way:
            flight_fare_id2 = getFareID(flight_fare_type2)


        #select page
        if True:
            # clickClass('before_selected')
            data_market = 0
            scrollSearchXPath(f"//div[contains(@class, 'before_selected')][@data-market='{data_market}']")
            clickXPath(f"//div[contains(@class, 'before_selected')][@data-market='{data_market}']")
            scrollSearchXPath(f"//div[@class='selectFareButton' and @onclick='selectFlightProduct(this, {flight_fare_id});']")
            clickXPath(f"//div[@class='selectFareButton' and @onclick='selectFlightProduct(this, {flight_fare_id});']")

            if not is_one_way:
                data_market = 1
                scrollSearchXPath(f"//div[contains(@class, 'before_selected')][@data-market='{data_market}']")
                clickXPath(f"//div[contains(@class, 'before_selected')][@data-market='{data_market}']")
                scrollSearchXPath(f"//div[@class='selectFareButton' and @onclick='selectFlightProduct(this, {flight_fare_id2});']")
                clickXPath(f"//div[@class='selectFareButton' and @onclick='selectFlightProduct(this, {flight_fare_id2});']")

            clickID('button_continue')

        #passenger page
        if not is_login:
            scrollAndType('first_name1', first_name)
            scrollAndType('last_name1', last_name)
            scrollAndType('contact_first_name', contact_first_name)
            scrollAndType('contact_last_name', contact_last_name)
            scrollAndType('contact_email', contact_email)
            scrollAndType('contact_mobile_phoneINPUT', mobile_phone)
            #click ID 'agreement'
        if True:
            scrollSearchID('agreement')
            clickID('agreement')
            clickID('button_continue')

        #elem.send_keys('seleniumhq' + Keys.RETURN)
        #elem.send_keys('seleniumhq')
        print(f"Done")
        #browser.quit()

    #CELIK TAFSIR
    elif program == "CT":
        import urllib.request #url getter
        import re #get from pattern
        import os
        #from bs4 import BeautifulSoup
        import platform
        isProd = True

        ct_link = variables.CT_LINK

        if isProd:
            req = urllib.request.urlopen(ct_link)
            data = req.read()

        index = data.find("Senarai Surah".encode("utf-8"))

        # Get the substring from the index to the end of the string
        substring = data[index:len(data)]

        #get all list
        indexS = substring.find("<ul>".encode("utf-8"))
        indexE = substring.find("</ul>".encode("utf-8"))
        substring2 = substring[indexS:indexE+5]

        #get all list of surah
        index3 = substring2.find("al-fatihah/".encode("utf-8"))
        index4 = substring2.find("an-nas/".encode("utf-8"))
        ss = substring2[index3-90 : index4+20]
        decoded_ss = ss.decode("utf-8")

        #get all href in Array
        nums = re.findall(r'href="(.+?)"', decoded_ss)

        #print(nums[0])

        #Date
        today = datetime.today().strftime("%Y%m%d-%H%M")

        #get all link and store it inside .txt file
        if False :
            txt = ""
            for f in nums:
                txt += (f + "\n")

            filename = "output python/output" + today + ".txt"
            with open(filename, "a") as f:
                print(txt, file=f)

            exit()


        #links
        txt = ""
        for link in nums:
            req = urllib.request.urlopen(link)
            data = req.read()

            print(link)

            #idx = data.find("entry-title")
            #soup = BeautifulSoup(data, 'html.parser')
            #get all Surah's inside pages
            data = str(data)
            idx = data.find('entry-title')
            s = data[idx:len(data)]
            idx2 = s.find('</ul>')
            s = s[0:idx2]
            #print(s)

            #get all href in Array
            pages = re.findall(r'href="(.+?)"', s)
            #print(pages)

            #put all inside txt variable
            for f in pages:
                txt += (f + " ")

            #albaqarah ada 3 part
            if (not (link == f'{ct_link}surah-002-al-baqarah/' or link == f'{ct_link}surah-002-bahagian-2/')):
                #remove last space
                txt = txt[:-1]
                #add newline foreach surah
                txt += ";\n"

        #remove last space
        # txt = txt[:-1]
        # txt += ";\n"

        #20-Feb-2025
        date = datetime.now()
        formatted_date = date.strftime('%d-%b-%Y')
        txt += formatted_date

        #create file
        file_name = "output python/output" + today + ".txt"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, "w") as f:
            print(txt, file=f)

        print(f"Successfully created file {file_name}")

        # Open the file location
        file_path = os.path.abspath(file_name)
        if openfileorfolder == "FD":
            file_path = os.path.dirname(file_path)


        os.startfile(file_path)  # Windows
        # os.system(f'open "{file_path}"') # macOS
        # os.system(f'xdg-open "{file_path}"') # Linux


        exit()

    #TELEGRAM BOT
    elif program == "TB":
        # needPass()
        import json
        import requests

        # VARIABLES -----------------
        TOKEN = tbtoken
        if info3 == None:
            code2 = "Afwan" #Custom to
            info3 = "custom" #Custom message
        #VARIABLES ------------------

        if code2 == "Afwan":
            CHAT_ID = "222338004" # Celik Tafsir website update Warning : -4723012335 , Study with Afwan : -4515480710 , Afwan : 222338004
        elif code2 == "Study":
            CHAT_ID = "-4515480710"
        elif code2 == "Study":
            CHAT_ID = "-4515480710"
        elif code2 == "Sara":
            CHAT_ID = "6238256254"

        MESSAGE = info3


        # VARIABLES -----------------
        tb_token = variables.tb_token

        # Telegram API URL
        url = f"https://api.telegram.org/bot{tb_token}/sendMessage"
        # data={"chat_id": CHAT_ID, "text": MESSAGE}
        # data = json.dumps(data).encode("utf-8") #change to json
        # headers = {"Content-Type":"application/json"}
        #response = http.request("POST", url, body=data, headers=headers)

        # req = ur.Request(url, data=data, headers=headers, method="POST")
        # with ur.urlopen(req) as response:
        #     status_code = response.getcode()
        #     response = response.read().decode("utf-8")



        # Send the message
        response = requests.post(url, data={"chat_id": CHAT_ID, "text": MESSAGE})
        status_code = response.status_code

        # Check response
        #if response.status_code == 200:
        if status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message: {response.text}")

    #WEB SCRAPING WITH LOGIN FOR afwanhaziq.pythonanywhere.com
    elif program == "WS":

        import urllib.request #url getter
        import urllib.parse
        import re #get from pattern
        import http.cookiejar
        import os
        from bs4 import BeautifulSoup
        import datetime

        def login_and_get_data(url, data, cookie_jar=None):

            encoded_data = urllib.parse.urlencode(data).encode()
            if not cookie_jar:
                cookie_jar = http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
            urllib.request.install_opener(opener)
            req = urllib.request.Request(url, data=encoded_data, method='POST')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            try:
                with urllib.request.urlopen(req) as response:
                    response_data = response.read().decode()
                    return response_data
            except urllib.error.HTTPError as e:
                print(f"Request failed with status code: {e.code}")
                return None

        def count_tags(html_string, tag_name):
            soup = BeautifulSoup(html_string, 'html.parser')
            li_tags = soup.find_all(tag_name)
            return len(li_tags)

        #initialize url, data, & cookie
        url = 'https://afwanhaziq.pythonanywhere.com/login'
        email = variables.afwanemail
        data = {'email': email, 'password': 'test12345', 'submit':''}
        cookie_jar = http.cookiejar.CookieJar()

        response_data = login_and_get_data(url, data, cookie_jar)
        #print(response_data)

        if response_data:
            txt = ""
            soup = BeautifulSoup(response_data, 'html.parser')

            # Find the specific ul element
            li_tags = soup.find_all('li', class_="list-group-item")
            li_count = len(li_tags)
            txt += f"Total post: {li_count}\n\n"
            print(f"Number of <li> tags with class 'list-group-item': {li_count}")
            count = 0
            for li_tag in li_tags:
                count += 1
                posting_data = li_tag.find('div')
                if posting_data:
                    post_text = posting_data.text.strip()
                    txt += f"Post {count}: {post_text}\n"
                    print(f"Post {count}: {post_text}")
                #print(posting_data)
                #print(li_tag.text.strip())

            #GET ALL DATA THEN PUT IT INSIDE TXT FILE ==========================================
            today = datetime.datetime.now().strftime("%Y%m%d-%H%M")
            print(today)

            filename = "/home/AfwanProductions/mysite/cron_output/output" + today + ".txt"
            os.makedirs(os.path.dirname(filename), exist_ok=True) #make dir if not exist

            #note- "a" is append, "w" is overwrite
            if os.path.exists(filename):
                with open(filename, "w") as f:
                    print(txt, file=f)
            else:
                with open(filename, "a") as f:
                    print(txt, file=f)

        else:
            print("Login failed or an error occurred.")

    #AI auto message test
    elif program == "AAI":
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.alert import Alert
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.edge.options import Options as EdgeOptions
        from selenium.webdriver.chrome.service import Service as ChromeService
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from selenium.webdriver.edge.service import Service as EdgeService
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager as FirefoxDriverManager
        from webdriver_manager.microsoft import EdgeChromiumDriverManager as EdgeDriverManager
        from webdriver_manager.opera import OperaDriverManager
        # from webdriver_manager.drivers import edge
        import time

        browser = getbrowser(browser_code)
        url = f"https://deepai.org/chat"

        browser.get(url)

        text = "Hello guys, i am a man with testing testing , how can i help you? eh? you're an AI chatbot, sorry, i think,"

        time.sleep(1)
        e = browser.find_element(By.CLASS_NAME, "chatbox")
        e.send_keys(text)
        time.sleep(1)
        # e = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='send-button']")))
        e = browser.find_element(By.ID, "chatSubmitButton")
        e.click()

    #CRON RUN
    elif program == "CRS" or program == "CRPC" or program == "CRF" or program == "CRO" or program == "CRM":
        #CRPC - Cron Run PC , CRO - Cron Run Once , CRM - Cron Run Multiple
        import platform
        #from bs4 import BeautifulSoup
        import re

        def run_cron():
            print("Run check...")
            cronchecklink = variables.cronchecklink
            url = cronchecklink

            req = ur.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with ur.urlopen(req) as response:
                 response = response.read().decode("utf-8")

            def get_html_true(class_name, html):
                pattern = rf'<p class="{class_name}">(.*?)</p>'
                match = re.search(pattern, html)
                if match:
                    if match.group(1) == "True":
                        return True
                return False
            def get_html(class_name, html):
                pattern = rf'<p class="{class_name}">(.*?)</p>'
                match = re.search(pattern, html)
                if match:
                    return match.group(1)
                return ""

            print(response)

            timenowKL = get_html("timenowKL", response)
            timenowKL = Decimal(timenowKL)
            global last_run_times
            cans = {}
            for key in last_run_times.keys():
                cans[key] = get_html_true(f"min{key}", response)

            print("Done check")

            for key in cans.keys():
                if cans[key]:
                    load_min(key)


        def load_min(min):
            global program
            print (f"program = {program}")
            print(f"---------------------- every {min} min")
            if min == "0.5":
                print("")
            if min == "1":
                print("")
            if min == "2":
                # logging.info(f"Run RP")
                run_function("RP")
            if min == "3":
                print("")
            if min == "5":
                print("")
            if min == "10":
                print("")
            if min == "30":
                print("")
            if min == "60":
                if program != "CRF":
                    # logging.info(f"Run CSFTP")
                    run_function("CSFTP")
            print(f"---------------------- every {min} min")

        run_cron()

        if program == "CRPC":
            while True:
                totalsec = 120
                countsec = 10
                for remaining in range(0, totalsec, countsec): #sleep 5min
                    esec = remaining
                    print(f"\rElapsed {esec}s ...", end="", flush=True)
                    time.sleep(countsec)
                run_cron()
        elif program == "CRF" or program == "CRM":
            while True:
                time.sleep(120)
                run_cron()

    #CHECK SFTP
    elif program == "CSFTP":
        csftp_link = variables.csftp_link
        url = csftp_link
        try:
            print("running CSFTP...")
            req = ur.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with ur.urlopen(req) as response:
                 response = response.read().decode("utf-8")
            html_data = response
            #response = requests.get(url)
            #response = http.request("GET", url)
            #response = response.data.decode("utf-8")
            #html_data = response
            #print(html_data)
            if (html_data != "connected to NAVITAIRE1SAP<br/>connected to NPS1FIREFLY<br/>connected to ELNVOICE1NAVITAIRE<br/>connected to 2360692 prod<br/>connected to 2360692 staging"): #has changes
                run_function("TB", "Afwan", f"One of the SFTP is not running  \n  \n  {html_data}")
            print (html_data)
            print("done CSFTP")

        except Exception as e:
            print(f"Failed to load {url} - Error: {e}")

    #Reminder Parking
    elif program == "RP":

        print("running RP...")

        now = datetime.now(timezone.utc)
        gmt8 = timezone(timedelta(hours=8))
        now = now.astimezone(gmt8)

        current_time = now.strftime("%H:%M")
        weekdays = now.weekday() < 5  # Monday to Friday are considered weekdays (0-4)

        print(f"now is {current_time}")



        # Load reminders from JSON

        reminders = [
            {"time_range": ["08:58", "09:01"], "message": "Bayar parking pagii https://play.google.com/store/apps/details?id=my.com.lits.flexiparking2", "days": "weekdays", "to": "Afwan"}
            ,{"time_range": ["13:58", "14:01"], "message": "Bayar parking petanggg https://play.google.com/store/apps/details?id=my.com.lits.flexiparking2", "days": "weekdays", "to": "Afwan"}
            ,{"time_range": ["20:50", "21:10"], "message": "Cakap SAYANG kat saraa", "days": "all", "to": "Afwan"}
            ,{"time_range": ["16:30", "16:50"], "message": "ya iya sayang", "days": "all", "to": "Sara"}
        ]

        for reminder in reminders:
            if (weekdays and reminder["days"] == "weekdays") or reminder["days"] == "all":
                if reminder["time_range"][0] <= current_time <= reminder["time_range"][1]:
                    run_function("TB", reminder["to"], reminder["message"])


        print("done RP")
   
    #Check message
    elif program == "CM":
        import json
        import requests

        tb_token = variables.tb_token
        url = f"https://api.telegram.org/bot{tb_token}/getUpdates"
        target_id = "222338004"
        target_username = "sra2931" #Afwanhz , sra2931
        search_by = "CM" # ID , US - username , CM - Command
        try:
            print("running CM...")
            response = requests.get(url)
            data = response.json()
            for update in data.get("result", []):
                message = update.get("message", {})
                user = message.get("from", {})

                # Check if the message is from the target user
                if search_by == "ID":
                    if str(user.get("id")) == target_id:
                        id = user.get("id", "Unknown")
                        username = user.get("username", "Unknown")
                        text = message.get("text", "[No text message]")
                        print(f"Id: {id} | User: {username} | Message: {text}")

                elif search_by == "US":
                    if str(user.get("username")) == target_username:
                        id = user.get("id", "Unknown")
                        username = user.get("username", "Unknown")
                        text = message.get("text", "[No text message]")
                        print(f"Id: {id} | User: {username} | Message: {text}")

                elif search_by == "CM":
                    id = user.get("id", "Unknown")
                    username = user.get("username", "Unknown")
                    text = message.get("text", "[No text message]")
                    date = message.get("date", "[No date]") #Unique
                    # print(f"Id: {id} | User: {username} | Message: {text}")

                    #Command


                    if "/command1" in text:
                        if "/command1@I_Awesome_OT_Bot" in text:
                            print(f"{username} | date:{date} | command : {text}")
                        else:
                            print(f"{username} | date:{date} | command private : {text}")

        except Exception as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Failed to load {url} - Error: {e}")

    #Flask website afwanproductions
    elif program == "FW":
        import mysql.connector
        import json, time
        from contextlib import contextmanager
        from werkzeug.exceptions import BadRequest
        import os
        #pip install flask mysql-connector-python flask-cors werkzeug

        @contextmanager
        def connect_to_db():
            try:
                mydb = mysql.connector.connect(
                    host="AfwanProductions.mysql.pythonanywhere-services.com",
                    user="AfwanProductions",
                    password="afwan987",
                    database="AfwanProductions$afwan_db"
                )
                admin_db = mydb.cursor()
                yield admin_db, mydb
            except mysql.connector.Error as err:
                print(f"Error connecting to database: {err}")
                raise
            finally:
                if mydb:
                    mydb.close()
        
        @app.route('/api/test', methods=['GET','POST', 'OPTIONS'])
        def test():
            return jsonify({"message": "Query executed successfully"}), 200
        #TRY===========================================================================
        @app.route('/api', methods=['GET','POST'])
        def handle_request():
            text = str(request.args.get('input')) #?input=a
            character_count = len(text)

            data_set = {'input': text, 'timestamp': time.time(), 'character_count': character_count}
            json_dump = json.dumps(data_set)
            return json_dump

        #QUERY EXECUTER============================================================================
        @app.route('/api/execute', methods=['GET','POST'])
        def execute_query():
            try:
                with connect_to_db() as (admin_db, mydb):

                    sql = str(request.args.get('query'))
                    password = str(request.args.get('password'))

                    if "'" in sql:
                        return jsonify({"error": "query parameter is not valid"}), 400
                    if not sql:
                        return jsonify({"error": "query parameter is required"}), 400
                    if not password:
                        return jsonify({"error": "password parameter is required"}), 400

                    if password == variables.website_pass:
                        try:
                            admin_db.execute(sql)
                            if admin_db.with_rows: # Check if the query returns rows
                                results = admin_db.fetchall() # Fetch all results
                                return jsonify({"results": results}), 200 # Return results in JSON
                            else:
                                mydb.commit() # Commit for insert, update, delete
                                return jsonify({"message": "Query executed successfully"}), 200
                        except mysql.connector.Error as db_err:
                            mydb.rollback() # Rollback in case of error
                            return jsonify({"error": f"Database error: {db_err}"}), 500
                    else:
                        return jsonify({"error": "Incorrect password"}), 401
            except Exception as e:
                return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

        #QUERY EXECUTER JSON============================================================================
        @app.route('/api/executejson', methods=['GET','POST'])
        def execute_query_json():
            try:
                with connect_to_db() as (admin_db, mydb):

                    data = request.get_json()

                    if 'query' not in data:
                        return jsonify({"error": "query parameter is required"}), 400

                    if 'password' not in data:
                        return jsonify({"error": "password parameter is required"}), 400

                    sql = data['query']
                    password = data['password']

                    #if "'" in sql:
                        #return jsonify({"error": "query parameter is not valid"}), 400

                    if password == variables.website_pass:
                        try:
                            admin_db.execute(sql)
                            if admin_db.with_rows: # Check if the query returns rows
                                results = admin_db.fetchall() # Fetch all results
                                return jsonify({"results": results}), 200 # Return results in JSON
                            else:
                                mydb.commit() # Commit for insert, update, delete
                                return jsonify({"message": "Query executed successfully"}), 200
                        except mysql.connector.Error as db_err:
                            mydb.rollback() # Rollback in case of error
                            return jsonify({"error": f"Database error: {db_err}"}), 500
                    else:
                        return jsonify({"error": "Incorrect password"}), 401
            except Exception as e:
                return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

        #QUERY EXECUTER JSON V2============================================================================
        @app.route('/api/executejsonv2', methods=['GET','POST'])
        def execute_query_json_v2():
            try:
                with connect_to_db() as (admin_db, mydb):

                    data = request.get_json()

                    if 'query' not in data:
                        return jsonify({"error": "query parameter is required"}), 400

                    if 'password' not in data:
                        return jsonify({"error": "password parameter is required"}), 400

                    sql = data['query']
                    password = data['password']

                    #if "'" in sql:
                        #return jsonify({"error": "query parameter is not valid"}), 400

                    if password == variables.website_pass:
                        try:
                            admin_db.execute(sql)
                            if admin_db.with_rows: # Check if the query returns rows
                                columns = [column[0] for column in admin_db.description] # Get column names
                                results = []
                                for row in admin_db.fetchall():
                                    results.append(dict(zip(columns, row))) # Create dictionary for each row
                                return jsonify({"results": results}), 200 # Return results in JSON
                            else:
                                mydb.commit() # Commit for insert, update, delete
                                return jsonify({"message": "Query executed successfully"}), 200
                        except mysql.connector.Error as db_err:
                            mydb.rollback() # Rollback in case of error
                            return jsonify({"error": f"Database error: {db_err}"}), 500
                    else:
                        return jsonify({"error": "Incorrect password"}), 401
            except Exception as e:
                return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

        #QUERY EXECUTER JSON TEST============================================================================
        @app.route('/api/executejsontest', methods=['GET','POST'])
        def execute_query_json_test():
            try:
                with connect_to_db() as (admin_db, mydb):

                    if request.is_json:
                        data = request.get_json()
                        return jsonify(data)
                    else:
                        return jsonify({"error": "Invalid JSON data provided."}), 400

                    return data

            except Exception as e:
                return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

        #afwan
        TXT_FILES_DIR = "/home/AfwanProductions/mysite/cron_output/"  # Replace with the actual path

        @app.route("/croncheck")
        def cron_check():
            global last_run_times

            #get time
            now = datetime.now(timezone.utc)
            gmt8 = timezone(timedelta(hours=8))
            current_time_raw = now.astimezone(gmt8)
            current_time_timestamp = current_time_raw.timestamp()

            # get time
            timenowKL = current_time_timestamp
            times = {}
            for key in last_run_times.keys():
                times[key] = datetime.fromtimestamp(last_run_times[key], tz=gmt8).strftime('%Y-%m-%d %I:%M %p')


            # get can or not
            cans = {}
            for key in times.keys():
                print(current_time_timestamp)
                print(last_run_times[key])
                print(current_time_timestamp - last_run_times[key])
                if (current_time_timestamp - last_run_times[key]) > ((float(key)*30)-10):
                    last_run_times[key] = current_time_timestamp
                    cans[key] = True
                else:
                    cans[key] = False

            current_time = current_time_raw.strftime('%Y-%m-%d %I:%M %p')

            html = f"""
                <!DOCTYPE html>
                <html>
                <head><title>Cron Check</title></head>
                <body>
                    <h2>Cron Check</h2>
                    <p>Current time: { current_time }</p>
                    """

            for key in times.keys():
                html += f'<p>Last {key}min: { times[key] }</p>'
            for key in times.keys():
                html += f'<p class="min{key}">{cans[key]}</p>'

            html += f"""
                    <p class="timenowKL">{timenowKL}</p>
                </body>
                </html>
            """

            return render_template_string(html)


        @app.route("/")
        def index():

            txt_files = [f for f in os.listdir(TXT_FILES_DIR) if f.endswith(".txt")]
            txt_files.sort(reverse=True)
            return render_template("index.html", files=txt_files)

        @app.route("/view/<filename>")
        def view_file(filename):
            filepath = os.path.join(TXT_FILES_DIR, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()
                return render_template("view.html", content=content, filename=filename)
            except FileNotFoundError:
                return "File not found", 404



        #APP DEBUG==============================================================================
        if __name__ == '__main__':
            app.run(debug=True)

    #Run Bot Polling
    elif program == "BP":
        #pip install python-telegram-bot --upgrade
        #pip install apscheduler

        from telegram import Update
        from telegram.ext import Application, CommandHandler, CallbackContext #, MessageHandler, filters
        from apscheduler.schedulers.background import BackgroundScheduler
        import datetime
        import asyncio

        TOKEN = variables.tb_token
        scheduler = BackgroundScheduler()
        scheduler.start()

        #reminder--------------------
        async def reminder_command(update: Update, context: CallbackContext):
            user_id = update.effective_user.id
            user_name = update.effective_user.username
            message_parts = update.message.text.split(maxsplit=2)  # Split text into parts

            if len(message_parts) < 3:
                await update.message.reply_text("Usage: /reminder <time> <message>\nExamples:\n- /reminder 2pm lunch\n- /reminder 2:30pm meeting")
                return

            timing = message_parts[1]
            reminder_text = message_parts[2]

            # Try to parse "2pm" and "2:30pm" formats
            reminder_time = None
            for time_format in ("%I:%M%p", "%I%p"):
                try:
                    reminder_time = datetime.datetime.strptime(timing, time_format).time()
                    break
                except ValueError:
                    continue

            if reminder_time is None:
                await update.message.reply_text("Invalid time format! Use:\n- `2pm`\n- `2:30pm`\n- `10am`\n- `10:45pm`")
                return

            tz_gmt8 = datetime.timezone(datetime.timedelta(hours=8))
            now = datetime.datetime.now(tz=tz_gmt8).time()
            # now = datetime.datetime.now().time()
            if reminder_time <= now:
                await update.message.reply_text("The time must be in the future!")
                return

            run_time = datetime.datetime.combine(datetime.date.today(), reminder_time)
            run_time = run_time.replace(tzinfo=tz_gmt8)
            scheduler.add_job(
                asyncio.create_task, 'date', run_date=run_time, args=[send_reminder(context.application, user_id, reminder_text)]
            )

            print(f"{user_name} : Reminder set for {timing}: {reminder_text}")
            await update.message.reply_text(f"Reminder set for {timing}: {reminder_text}")

        # Remove the synchronous wrapper as we are now directly using asyncio.create_task

        async def send_reminder(application: Application, user_id, message):
            await application.bot.send_message(chat_id=user_id, text=f"🔔 Reminder: {message}")
        #reminder--------------------

        async def start(update: Update, context: CallbackContext):
            user_id = update.effective_user.id  # Get User ID
            user_message = update.message.text
            print(f"User ID: {user_id}")
            print(f"User Message: {user_message}")
            await update.message.reply_text("Hai sara, laju tak saya reply, hihi, sorry haritu ngantuukk")

        async def help_command(update: Update, context: CallbackContext):
            await update.message.reply_text("Available commands: /start")
        async def sayang_afwan(update: Update, context: CallbackContext):
            await update.message.reply_text("SAYANG SARA JUGAKKKKKKKK")

        async def handle_messages(update: Update, context: CallbackContext):
            user_id = update.effective_user.id
            user_name = update.effective_user.username
            user_message = update.message.text
            print(f"Message from {user_name} : {user_message}")

            # Example: If user says "hello", bot replies "Hello too!"
            if "hello" in user_message.lower():
                await update.message.reply_text("Hello too!")
            if "hai afwan" in user_message.lower():
                await update.message.reply_text("Hai saraaa -Afwan 2025")
            # else:
            #     await update.message.reply_text(f"Afwan received: {user_message}")

        def main():
            app = Application.builder().token(TOKEN).build()

            # Add command handlers
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CommandHandler("help", help_command))
            app.add_handler(CommandHandler("sayangafwan", sayang_afwan))

            # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
            app.add_handler(CommandHandler("reminder", reminder_command))

            print("Bot is running...")

            # Start long polling
            app.run_polling()

        if __name__ == "__main__":
            main()

    #Summary today log
    elif program == "STL":
        today = datetime.now().strftime("%Y-%m-%d")
        log_summary = []

        with open("cron_log.txt", "r") as file:
            for line in file:
                if today in line:
                    log_summary.append(line.strip())

        
        now = datetime.now(timezone.utc)
        gmt8 = timezone(timedelta(hours=17.81))
        current_time_raw = now.astimezone(gmt8)
        current_time_timestamp = current_time_raw.timestamp()
        current_time = current_time_raw.strftime('%Y-%m-%d %I:%M %p')
        current_time2 = current_time_raw.strftime('%I:%M %p')
        if ("11:59 PM" <= current_time2 <= "12:01 AM"):
            #show summary
            today = datetime.now().strftime("%Y-%m-%d")
            log_summary = []

            with open("cron_log.txt", "r") as file:
                for line in file:
                    if today in line:
                        log_summary.append(line.strip())
            summary = "\n".join(log_summary) if log_summary else "No logs for today."
            run_function("TB", "Afwan", f"Summary of today's log:\n{summary}")
        print(current_time2)
        
    #expo react native bundle release
    elif program == "EXPO":
        import textwrap

        print(textwrap.dedent(r"""
            README: This will run ./gradlew bundleRelease , please make sure:
                              
            Inside android\build.gradle:
                              
            ext {
                buildToolsVersion = findProperty('android.buildToolsVersion') ?: '35.0.0'
                minSdkVersion = Integer.parseInt(findProperty('android.minSdkVersion') ?: '24')
                compileSdkVersion = Integer.parseInt(findProperty('android.compileSdkVersion') ?: '35')
                targetSdkVersion = Integer.parseInt(findProperty('android.targetSdkVersion') ?: '34')
                kotlinVersion = findProperty('android.kotlinVersion') ?: '1.9.25'
                ndkVersion = "26.1.10909125"  ---important
            }
            repositories {
                google()
                mavenCentral()
            }
            dependencies {
                classpath('com.android.tools.build:gradle')
                classpath('com.facebook.react:react-native-gradle-plugin')
                classpath('org.jetbrains.kotlin:kotlin-gradle-plugin')
            }

            if want to use gradle 8.10.2:
            distributionUrl=https\://services.gradle.org/distributions/gradle-8.10.2-all.zip
            
            dependencies {
                classpath("com.android.tools.build:gradle:8.10.2") 
                ...
            }


            """
        ))

        import os
        import subprocess
        import sys
        import datetime
        import requests

        #Put directory app
        # projectloc = input("Please input project directory location: ")
        projectname = "Escabee"
        projectloc = r"C:\escabee-mobile"
        projectloc += r"\android" 

        # go to directory
        if True:
            if os.path.exists(projectloc):
                os.chdir(projectloc)
                print(f"Changed directory to: {os.getcwd()}")
            else:
                print(f"Warning: The specified directory '{projectloc}' does not exist.")

            # Check 
            if not os.path.exists("gradle"):
                print("Error: This is not an Android folder. You cannot run gradlew here.")
                sys.exit(1)

        def run_command(command):
            """Runs a command in the shell and waits for it to complete."""
            process = subprocess.Popen(command, shell=True)
            process.communicate()
            if process.returncode != 0:
                print(f"Error: Command '{command}' failed.")
                sys.exit(1)

        # Gradlew clean , bundleRelease
        if True:
            print(r"Running: .\gradlew clean")
            run_command(r".\gradlew clean")

            print(r"Running: .\gradlew bundleRelease")
            run_command(r".\gradlew bundleRelease")

        # If already has AAB file, run this
        if True:
            # goto AAB file
            if True:
                output_dir = "app/build/outputs/bundle/release/"
                if os.path.exists(output_dir):
                    os.chdir(output_dir)
                    print(f"Changed directory to: {os.getcwd()}")
                else:
                    print(f"Warning: Output directory '{output_dir}' not found.")
            
            run_command("dir")

            bundletool_file = "bundletool-all-1.18.1.jar"
            keystore_file = "my-release-key.jks"
            aab_file = "app-release.aab"
            apks_file = datetime.datetime.now().strftime("my_app%d%b.apks")
            # Download bundletool
            if True:
                bundletool_url = "https://github.com/google/bundletool/releases/download/1.18.1/bundletool-all-1.18.1.jar"
                if not os.path.exists(bundletool_file):
                    print(f"Downloading {bundletool_file}...")
                    response = requests.get(bundletool_url, stream=True)
                    with open(bundletool_file, "wb") as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                print("Download completed.")

            # Generate Keystore
            if True:
                if not os.path.exists(keystore_file):
                    print("Generating keystore...")
                    run_command("keytool -genkeypair -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias")
                    print("Keystore generated.")

            # Build APK
            if True:
                if os.path.exists(apks_file):
                    print(f"Deleting existing {apks_file}...")
                    os.remove(apks_file)
                print("Building APKs using bundletool...")
                run_command(f'java -jar {bundletool_file} build-apks --bundle={aab_file} --output={apks_file} --mode=universal --ks={keystore_file} --ks-pass=pass:123456 --ks-key-alias=my-key-alias --key-pass=pass:123456')
                print(f"APKs successfully built as {apks_file}.")
            
            #Extract APK
            if True:
                if not os.path.exists(apks_file):
                    print(f"Error: {apks_file} not found.")
                    sys.exit(1)
                    
                print(f"Extracting {apks_file}...")
                extracted_dir = "extracted_apks"
                if not os.path.exists(extracted_dir):
                    os.makedirs(extracted_dir)
                # run_command(f'unzip -o "{apks_file}" -d {extracted_dir}')
                run_command(f'tar -xf "{apks_file}" -C {extracted_dir}')

            # Rename APK
            if True:
                universal_apk_path = os.path.join(extracted_dir, "universal.apk")
                if os.path.exists(universal_apk_path):
                    formatted_date = datetime.datetime.now().strftime("Escabee_%d_%b_%Y_%I%M%p.apk")
                    #Rename
                    # new_apk_name = os.path.join(os.getcwd(), formatted_date)
                    new_apk_name = os.path.join(extracted_dir, formatted_date)
                    os.rename(universal_apk_path, new_apk_name)
                    
                    print(f"Renamed 'universal.apk' to '{formatted_date}'")
                else:
                    print("Error: 'universal.apk' not found in extracted_apks.")
                    sys.exit(1)





run_function(program)

