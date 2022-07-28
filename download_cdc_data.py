#mcandrew

import sys
import numpy as np
import pandas as pd

class cdc(object):
    def __init__(self):
        self.downloads_folder = "cdc_webpage_downloads/"
    
    def ping_response_module(self):
        import requests
        self.url = "https://www.cdc.gov/poxvirus/monkeypox/response/modules/MX-response-case-count-US.json"
        self.client = requests.get(self.url)
        
    def grab_data(self):
        import pandas as pd
        import json

        self.ping_response_module()
        
        if self.client.status_code==200:
            self.data = json.loads(self.client.content)['data']

        time_stamp = self.time_today()
            
        count_data = {"location": [], "abbr": [], "count":[], "range":[], "time_stamp":[] }
        for state_data in self.data:
            count_data["location"].append(state_data["State"]) 
            count_data["abbr"].append(state_data["State"])
            count_data["count"].append(state_data["Cases"])
            count_data["range"].append(state_data["Range"])
            count_data["time_stamp"].append(time_stamp)
        count_data = pd.DataFrame(count_data)
        self.count_data = count_data

    def list_all_snapshots(self):
        from waybackpy import WaybackMachineCDXServerAPI

        url = "https://www.cdc.gov/poxvirus/monkeypox/response/2022/us-map.html"
        user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
        
        cdx = WaybackMachineCDXServerAPI(url, user_agent, start_timestamp=2022, end_timestamp=2022)

        pages_ts = []
        for page in cdx.snapshots():
            ts = page.datetime_timestamp
            pages_ts.append( (page.archive_url,ts) )
        self.list_of_pages = pages_ts
        return self.list_of_pages

    def most_recent_data_at_each_day(self):
        date2page = {}
        for page,dt in self.list_of_pages:
            d = dt.strftime("%Y-%m-%d")
            if d not in date2page:
                date2page[d] = (page,dt)
            else:
                current_page,current_date = date2page[d]
                
                if dt > current_date:
                    date2page[d] = (page,dt)
        self.list_of_pages = [ (page,dt)  for date, (page,dt) in date2page.items() ]
        return self.list_of_pages
    
    def click_download_button(self, url_dt):
        import selenium
        from selenium import webdriver
        from selenium.webdriver.support.ui import WebDriverWait       
        from selenium.webdriver.common.by import By       
        from selenium.webdriver.support import expected_conditions as EC
        
        import os
        import time
        
        import pandas as pd

        path_to_webdriver = "browser_driver/chromedriver"

        cwd = os.getcwd()
        
        options = webdriver.ChromeOptions()
        options.headless = False
        
        prefs = { "download.default_directory": os.path.join(cwd,self.downloads_folder)
                 ,"profile.default_content_settings.popups": 0
                  ,"directory_upgrade": True}
        options.add_experimental_option("prefs",prefs)

        url,dt = url_dt
        
        browser = webdriver.Chrome(path_to_webdriver, chrome_options = options)

        wait=WebDriverWait(browser, 20)
        browser.get(url)

        dta_txt = "Download Data (CSV)"
        download_button =  wait.until( EC.element_to_be_clickable((By.LINK_TEXT, dta_txt)))   #browser.find_element_by_link_text(dta_txt) 
        download_button.click()

        #--find date of review
        LRD = browser.find_element_by_id("last-reviewed-date")
        time_stamp = pd.to_datetime(LRD.text).strftime("%Y-%m-%d")

        time.sleep(1)

        #--add time stamp to file
        most_recent_download = self.most_recent_file(self.downloads_folder)

        most_recent_download_root = most_recent_download.split(".csv")[0]
       
        os.rename( most_recent_download, "{:s}__{:s}__{:s}.csv".format(most_recent_download_root,time_stamp, dt.strftime("%Y-%m-%d %H %M %S") ) )
   
    def most_recent_file(self,dirr):
        import os

        time_file = []
        for root, dirs, files in os.walk(self.downloads_folder):
            for fil in files:
                f = os.path.join(root,fil)
                
                time = os.path.getctime(f)
                time_file.append( (time,f) )
        return sorted(time_file)[-1][-1]
        
    def time_today(args):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H %M %S")

    def get_stored_timestamps(self):
        from glob import glob
        time_stamps = [ fil.split("__")[-1].split(".csv")[0] for fil in glob(self.downloads_folder+"*")]
        self.stored_time_stamps = time_stamps
        
    def write(self):
        self.count_data.to_csv("./data/cdc__{:s}.csv".format( self.time_today() ), index=False)
    
if __name__ == "__main__":

    data = cdc()
    data.list_all_snapshots()
    data.most_recent_data_at_each_day()

    snapshots = data.list_of_pages

    try:
        url_list = []
        f_in = open("urls_downloaded.txt","r")
        for line in f_in:
            url_list.append(line.strip())
        f_in.close()
    except:
        pass
    fout = open("urls_downloaded.txt","a")
        
    while snapshots:
        url_dt = snapshots.pop(-1)
        url,dt = url_dt

        if url in url_list:
            continue
            
        data.click_download_button(url_dt)
        fout.write("{:s}\n".format(url))
