
import tkinter
import subprocess
from tkinter import *
import os
import sys
import pickle
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions




root = Tk()
root.geometry('300x200')
root.title("NFT Checker")
input_save_list = []
main_directory = os.path.join(sys.path[0])


def open_chrome_profile():
    subprocess.Popen(
        [
            "start",
            "chrome",
            "--remote-debugging-port=8989",
            "--user-data-dir=" + main_directory + "/chrome_profile",
        ],
        shell=True,
    )

def save_file_path():
    return os.path.join(sys.path[0], "Save_file.cloud") 


class InputField:
    def __init__(self, label, row_io, column_io, pos, master=root):
        self.master = master
        self.input_field = Entry(self.master)
        self.input_field.label = Label(master, text=label)
        self.input_field.label.grid(row=row_io, column=column_io)
        self.input_field.grid(row=row_io, column=column_io + 1)
        try:
            with open(save_file_path(), "rb") as infile:
                new_dict = pickle.load(infile)
                self.insert_text(new_dict[pos])
        except FileNotFoundError:
            pass

    def insert_text(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)

    def save_inputs(self, pos):
        input_save_list.insert(pos, self.input_field.get())
        with open(save_file_path(), "wb") as outfile:
            pickle.dump(input_save_list, outfile)

###input objects###
collection_input= InputField("Collection Link", 2, 0, 1)
start_num_input = InputField("Start Number:", 3, 0, 2)
end_num_input = InputField("End Number:", 4, 0, 3)
item_num_input= InputField("How many items\nthere should be?:", 5, 0, 4 )




###save inputs###
def save():
    collection_input.save_inputs(1)
    start_num_input.save_inputs(2)
    end_num_input.save_inputs(3)
    item_num_input.save_inputs(4)

  
   

# _____MAIN_CODE_____
def main_program_loop():
    ###START###
    project_path=main_directory
    collection_link = collection_input.input_field.get() # "https://opensea.io/collection/s-o-n--n-e-t"
    start_num = int(start_num_input.input_field.get())
    end_num = int(end_num_input.input_field.get())
    item_num= str(item_num_input.input_field.get())


    ##chromeoptions
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(
        executable_path=project_path + "/chromedriver.exe",
        chrome_options=opt,
    )
    wait = WebDriverWait(driver, 60)

  

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))
    td=[]
    num=1
    while end_num >= start_num:
        if num==1:
            print("Start SEARCHing Posts"+str(start_num))
            driver.get(collection_link)
            time.sleep(1)
            num=num+1
        
               
        wait_xpath('//*[@id="main"]/div/div/div[3]/div/div/div/div[3]/div[1]/div[1]/input')
        name = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div/div/div[3]/div[1]/div[1]/input')
        
        
        name.send_keys(str(start_num)) 
        name.send_keys(Keys.ENTER)
        for d in range(0,4):
            name.send_keys(Keys.BACK_SPACE)
        time.sleep(3)

        wait_xpath('//*[@id="main"]/div/div/div[3]/div/div/div/div[3]/div[2]/div/p')
        a = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div/div/div[3]/div[2]/div/p').get_attribute('innerHTML')
        a=str(a)
        b=a.replace(" item","")
        h=(str(start_num)+" "+a)
        if b==item_num:
            pass
        else: 
            td.append(h)    
        
        print(str(start_num)+" "+a)
        

        start_num=start_num+1
        
    print(td)
         


        

#####BUTTON ZONE#######
button_save = tkinter.Button(root, width=20, text="Save Form", command=save) 
button_save.grid(row=23, column=1)
button_start = tkinter.Button(root, width=20, bg="green", fg="white", text="Start", command=main_program_loop)
button_start.grid(row=25, column=1)
open_browser = tkinter.Button(root, width=20,  text="Open Chrome Browser", command=open_chrome_profile)
open_browser.grid(row=22, column=1)

try:
    with open(save_file_path(), "rb") as infile:
        new_dict = pickle.load(infile)
        global upload_path
        upload_path = new_dict[0]
except FileNotFoundError:
    pass
#####BUTTON ZONE END#######
root.mainloop()
