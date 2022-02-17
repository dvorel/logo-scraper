import time, sys, csv, os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.user_data_dir = "C:\chrome_temp"
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    options.add_argument('log-level=1')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.delete_all_cookies()
    driver.start_client()
    time.sleep(1.0)
    driver.get("https://worldvectorlogo.com/alphabetical")
    time.sleep(1.0)
    
    #cookie accept
    try:
        driver.find_element_by_id("accept-choices").click()
        print("Cookie accepted")
    except:
        print("No Cookie")
    
    try:
        title_elements = driver.find_elements_by_class_name("logo")
    except:
        print("no titles")       
    time.sleep(3.0)
    
    for i in range(len(title_elements)):
        try:
            title_elements = driver.find_elements_by_class_name("title")
            print("Titles found")
        except:
            print("No titles found")        
        try:
            title_elements[i].click()
            print("Title clicked")
        except:
            print("No title to click")
        time.sleep(3.0)
        
        while True:
            time.sleep(12.0)
            l=0
            
            while True:
                #while globals
                fw = open(os.path.join(os.getcwd(), "dataset.csv"), "a", newline="")
                opened = True
                downloaded = True
                exists_csv = True
                ad = True
                #------------#
                try:
                    logos = driver.find_elements_by_class_name("logo__wrapper")
                    print(len(logos), " Found")
                except:
                    print("No logos found")
                #break statement
                if l >= len(logos):
                    break
                
                #open logo to download                
                try:
                    logos[l].click()
                    print("Logo opened")
                    time.sleep(4.0)
                except:
                    print("Cant open logo ", l)
                    opened = False
                
                #get logo tags
                tags = list()
                tags_el = driver.find_elements_by_class_name("meta__tag-link")
                for tel in tags_el:
                    tags.append(str((tel.get_attribute('href')).split("/")[-1]))
                
                #download logo
                try:
                    dwl = driver.find_element_by_class_name("button.margin")
                    logo_fname = str((dwl.get_attribute('href')).split("/")[-1])
                    print("File name: ", logo_fname)     
                except:
                    print(l, "No filename")
                    downloaded = False
                
                #check if logo is already downloaded
                with open('dataset.csv', 'r') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row in reader:
                        if logo_fname == row[0]:
                            exists_csv = False
                
                if exists_csv:
                    try:
                        dwl.click()
                        print("Download clicked")
                    except:
                        print("No download")
                        downloaded = False          

                time.sleep(2.0)
                tabs = driver.window_handles
                if len(tabs)>1:
                    for handle in tabs[1:]:
                        driver.switch_to.window(handle)
                        driver.close()
                    driver.switch_to.window(tabs[0])
                    ad = False
                    time.sleep(8.0)
                
                
                #write to csv
                if exists_csv and opened and downloaded and ad:                                       
                    writer = csv.writer(fw)
                    writer.writerow([logo_fname, tags])
                    fw.close()

                #final checks
                if opened or downloaded:
                    driver.back()
                    time.sleep(2.0)
                                  
                    if downloaded and exists_csv:
                        driver.back()
                    if ad:
                        l+=1           

                #final sleep
                time.sleep(4.0)
                if l%8 == 0:
                    time.sleep(15.0)
                #clear output console
                print("\n####################################\n",l)
            
            #open next or main page
            try:
               driver.find_element_by_xpath("/html/body/div[1]/main/section[2]/div/div[2]/div/div[5]/a").click()
               print("Next Page")               
            except:
               print("Main page")            
               driver.get("https://worldvectorlogo.com/alphabetical")               
               break
        
    print(f"Ended with {l} logos downloaded")
