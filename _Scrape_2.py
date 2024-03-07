from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from time import sleep
from des import split_csv_file
from dotenv import load_dotenv
from traceback import print_exc
import os
import csv

number = 1

class Apollo:
    def __init__(self,proxy :str | None,number : str | int) -> None:
        self.chrome_options = webdriver.FirefoxOptions()
        self.chrome_options.add_argument(f"--user-agent={UserAgent().random }")
        if proxy:
            self.chrome_options.add_argument(f"--proxy-server={proxy.strip()}")
        self.driver = webdriver.Firefox(options=self.chrome_options)
        self.driver.implicitly_wait(10)
        self.actions = ActionChains(self.driver)
        self.pages : int
        self.output_path = os.getcwd() + f"/resources/Output/Output{number}.csv"
        self.output_file = open(self.output_path, 'a+')
        self.csv_writer = csv.writer(self.output_file,delimiter=' ',quotechar=',')

    def login(self,email:str,password:str):
        '''logs in to the self.io website.'''
        self.driver.get('https://app.apollo.io/#/login')
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Email"]//parent::div/div/div/input'))
        )
        email_input.send_keys(email)

        pass_input = self.driver.find_element(By.XPATH, '//span[text()="Email"]//parent::div/following-sibling::div/div/div/div/input')
        pass_input.send_keys(password)

        login_button = self.driver.find_element(By.XPATH, '//div[text()="Log In"]')
        login_button.click()

        sleep(2)

    def upload(self,filepath:str):
        '''Takes one file path and uploads it to the self.io website.'''
        self.driver.get('https://app.apollo.io/#/contacts/import')
        sleep(2)
        try:
            upload = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH,'//input[@type="file"]')))
        except Exception as e:
            print(repr(e))
            print("Please Check your Email or Password. Exiting...")
            input("Press Enter to exit...")
            exit(1)
        upload.send_keys(filepath)
        select = WebDriverWait(self.driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='main-app']/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[2]/div[3]/div/div[2]/div/div/div/div/div")))
        self.actions.move_to_element(select).click().perform()
        
        option = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".Select-option:nth-child(12)"))
        )
        option.click()
        self.driver.find_element(By.CSS_SELECTOR, ".zp_kxUTD:nth-child(2)").click()
        self.driver.find_element(By.CSS_SELECTOR, ".zp-button:nth-child(2) > .zp_kxUTD").click()
        sleep(3)

    def enrich(self):
        #----------------------------------------------
        #Getting the number of pages
        footer = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div/div/div[3]/div/div[1]/span"))
        ).text
        splitter = footer.split(" ")

        last = splitter[-1]
        rem = int(last) % 25
        self.pages = int(last) // 25 + 1 if rem != 0 else int(last) // 25
        #----------------------------------------------

        for i in range(1,self.pages+1):
            self.driver.get(self.driver.current_url.split("&")[0] + f"&page={i}")
            WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".zp_FVbJk"))
            )
            select = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.zp_FVbJk')))
            select.click()
            self.driver.find_element(By.LINK_TEXT, "Select this page").click()
            enrich = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#enrich > .apollo-icon-caret-down-small"))
            )
            enrich.click()
            self.driver.find_element(By.CSS_SELECTOR, ".zp-menu-item:nth-child(1)").click()
            sleep(1)
            confirm = self.driver.find_element(By.CSS_SELECTOR, ".zp_bns67 > .zp-button")
            if confirm:
                confirm.click()

    def scrape_data(self):
        try:
            print("Scraping Data...")
            rows = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,"zp_RFed0"))
            )
            self.driver.implicitly_wait(10)
            a,n,t,i,e,em,c,p,k,l = 0,0,0,0,0,0,0,0,0,0,
            table_head = self.driver.find_element(By.TAG_NAME,"thead")
            for th in table_head.find_elements(By.TAG_NAME,"th"):
                if th.text == "Name":
                    n = a
                elif th.text == "Title":
                    t = a
                elif th.text == "Industry":
                    i = a
                elif th.text == "# Employees":
                    e = a
                elif th.text == "Email":
                    em = a
                elif th.text == "Company":
                    c = a
                elif th.text == "Phone":
                    p = a
                elif th.text == "Keywords":
                    k = a
                elif th.text == "Contact Location":
                    l = a
                a +=1

            rows = self.driver.find_elements(By.CLASS_NAME,"zp_RFed0")
            for row in rows:
                try:
                    colmn = row.find_elements(By.CLASS_NAME,"zp_aBhrx")
                    links_row = row.find_elements(By.CLASS_NAME,"zp_I1ps2")[-1].find_elements(By.TAG_NAME,"a")
                    try:
                        member_linkedin_btn = links_row[0]
                    except:
                        member_linkedin_btn = None
                    try:
                        company_linkedin_btn = links_row[1]
                    except:
                        company_linkedin_btn = None
                    try:
                        facebook_btn = links_row[2]
                    except:
                        facebook_btn = None
                    try:
                        twitter_btn = links_row[3]
                    except:
                        twitter_btn = None
                    #datas
                    name = colmn[n].text
                    title = colmn[t].text
                    company_name = colmn[c].text
                    location = colmn[l].text
                    members = colmn[e].text
                    phone = colmn[p].text
                    industry = colmn[i].text
                    keywords = ''.join([field.text for field in colmn[k].find_elements(By.CLASS_NAME,'zp_yc3J_')])
                    email = colmn[em].text
                    link1 = member_linkedin_btn.get_attribute('href') if member_linkedin_btn else 'NoLink'
                    link2 = company_linkedin_btn.get_attribute('href') if company_linkedin_btn else 'N/A'
                    link3 = facebook_btn.get_attribute('href') if facebook_btn else 'N/A'
                    link4 = twitter_btn.get_attribute('href') if twitter_btn else 'N/A'

                    self.csv_writer.writerow([name,title,company_name,location,email,members,phone,industry,keywords,link1,link2,link3,link4])
                except Exception:
                    continue
        except Exception as e:
            print(e)

    def teardown(self):
        self.driver.quit()
        self.output_file.close()

if __name__ == "__main__":
    try:
        load_dotenv()
        email = os.getenv(f'EMAIL{number}')
        password = os.getenv(f'PASSWORD{number}')
        proxy = os.getenv(f'PROXY{number}')

        if not email or not password:
            print(f'''
            Email and password not found in the .env file.
            Please add the following environment variables to your .env file:
                -EMAIL{number}="YOUR EMAIL HERE"
                -PASSWORD{number}="YOUR PASSWORD HERE"''')
            input("Press Enter to exit...")
            exit(1)

        if not proxy:
            print(f'''
            Proxy not found in the .env file, Using Direct IP Address.
            You can add proxy, IF YOU WANT TO USE PROXY in the .env file:
                Example:
                    -PROXY{number}="PROXYIP:PROXYPORT"
            ''')

        apollo = Apollo(proxy,number)
        apollo.login(email,password)

        split_csv_file(number)
        execpath = os.getcwd()
        file_in_dir = os.listdir(f"{execpath}/resources/Temp/Splits{number}/")

        for file in file_in_dir:
            apollo.upload(f"{execpath}\\resources\\Temp\\Splits{number}\\{file}")
            apollo.enrich()

            for i in range(1,apollo.pages+1):
                apollo.driver.get(apollo.driver.current_url.split("&")[0] + f"&page={i}")
                sleep(4)
                apollo.scrape_data()
                
    except Exception as e:
        print_exc()
        
    finally:
        apollo.teardown()