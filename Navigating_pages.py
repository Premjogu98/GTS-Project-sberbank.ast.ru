from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import Global_var
import sys, os
import re
import ctypes
import pymysql.cursors
from datetime import datetime
import wx
app = wx.App()

def chromedriver():
    chrome_options = Options()
    chrome_options.add_extension('C:\\BrowsecVPN.crx')
    browser = webdriver.Chrome(executable_path=str(f"C:\\chromedriver.exe"),chrome_options=chrome_options)
    browser.maximize_window()
    # browser.get("""https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")
    wx.MessageBox(' -_-  Add Extension and Select Proxy Between 10 SEC -_- ', 'Info', wx.OK | wx.ICON_WARNING)
    time.sleep(15)  # WAIT UNTIL CHANGE THE MANUAL VPN SETtING
    browser.get("http://www.sberbank-ast.ru/UnitedPurchaseList.aspx")
    time.sleep(5)
    for Date_wise in browser.find_elements_by_xpath('//*[@id="sortControls"]/a[2]'):
        Date_wise.click()
        break
    time.sleep(5)
    clicking_process(browser)


def Local_connection_links():
    a = 0
    while a == 0:
        try:
            # File_Location = open(
            #     "D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\sberbank-ast.ru\\Location For Database & Driver.txt",
            #     "r")
            # TXT_File_AllText = File_Location.read()

            # Local_host = str(TXT_File_AllText).partition("Local_host_link=")[2].partition(",")[0].strip()
            # Local_user = str(TXT_File_AllText).partition("Local_user_link=")[2].partition(",")[0].strip()
            # Local_password = str(TXT_File_AllText).partition("Local_password_link=")[2].partition(",")[0].strip()
            # Local_db = str(TXT_File_AllText).partition("Local_db_link=")[2].partition(",")[0].strip()
            # Local_charset = str(TXT_File_AllText).partition("Local_charset_link=")[2].partition("\")")[0].strip()

            connection = pymysql.connect(host='185.142.34.92',
                                         user='ams',
                                         password='TgdRKAGedt%h',
                                         db='tenders_db',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
            return connection
        except pymysql.connect  as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,"\n", exc_tb.tb_lineno)
            a = 0
            time.sleep(10)


def clicking_process(browser):
    a = False
    while a == False:
        try:
            mydb_Local = Local_connection_links()
            mycursorLocal = mydb_Local.cursor()
            page = ''
            for page in browser.find_elements_by_xpath('/html/body/form/div[7]/div/div/div[7]/span/span[13]/span[1]'):
                page = page.get_attribute('innerText')
                break
            publish_date1 = ''
            for next_page in range(1, int(page), 1):
                global c
                c = True
                while c == True:
                    try:
                        for Posting_date in browser.find_elements_by_xpath('//*[@content="leaf:PublicDate"]'):  # Publish Date
                            Posting_date = Posting_date.get_attribute('innerHTML')
                            tender_posting_date = str(Posting_date).partition(' ')[0].strip()
                            datetime_object = datetime.strptime(tender_posting_date, '%d.%m.%Y')
                            publish_date1 = datetime_object.strftime("%Y-%m-%d")
                            break
                        c = False
                    except:
                        c = True
                    if publish_date1 >= Global_var.From_Date:
                        Tender_value = ''
                        d = False
                        while d == False:
                            try:
                                for Tender_value in browser.find_elements_by_xpath('//*[@class="es-reestr-tbl its"]'):
                                    Tender_value = Tender_value.get_attribute('outerHTML')
                                    href = str(Tender_value).partition('content="leaf:objectHrefTerm"')[2].partition('>')[0].strip()
                                    Tender_link = str(href).partition('value="')[2].partition('"')[0].strip()  # get href from outer Html
                                    Global_var.Total += 1
                                    if Tender_link != '':
                                        if Tender_link.startswith('http://www.sberbank-ast.ru/purchaseview.aspx?') or Tender_link.startswith('https://www.sberbank-ast.ru/purchaseview.aspx?'):
                                            commandText = "SELECT ID from sberbank_temptbl where doc_links = '" + str(Tender_link) + "'"
                                            mycursorLocal.execute(commandText)
                                            results = mycursorLocal.fetchall()
                                            if len(results) > 0:
                                                print('Duplicate Tender')
                                                Global_var.duplicate += 1
                                            else:
                                                print('Live Tender')
                                                print(Tender_link)
                                                sql = "INSERT INTO sberbank_temptbl(doc_links)VALUES(%s)"  # Collected Link Inserting on Database
                                                val = (str(Tender_link))
                                                database_error = False
                                                while database_error == False:
                                                    try:
                                                        mycursorLocal.execute(sql, val)
                                                        mydb_Local.commit()
                                                        Global_var.links_Insert_On_Database += 1
                                                        Global_var.Collected_link += 1
                                                        database_error = True
                                                    except Exception as e:
                                                        print('Error While Inserting Data On Database: ', str(e))
                                                        database_error = False
                                    else:
                                        Global_var.Link_Empty += 1
                                d = True
                            except:
                                d = False
                        break
                    else:
                        print("Publish Date Dead")
                        wx.MessageBox('Total:  ' + str(Global_var.Total) + '\n''Duplicate : ' + str(Global_var.duplicate) + '\n''links Insert On Database : ' + str(Global_var.links_Insert_On_Database), 'Info',wx.OK | wx.ICON_INFORMATION)
                        Global_var.Process_End()
                        browser.close()
                        sys.exit()
                b = 0
                while b == 0:
                    try:
                        for next_button in browser.find_elements_by_xpath('/html/body/form/div[7]/div/div/div[7]/span/span[14]/span[1]'):
                            next_button.click()
                            break
                        b = 1
                    except:
                        b = 0
            a = True
            print("Publish Date Dead")
            Global_var.Process_End()
            browser.close()
            sys.exit()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",exc_tb.tb_lineno)
            a = False


chromedriver()
