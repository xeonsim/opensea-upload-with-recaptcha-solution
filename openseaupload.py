import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import os
import sys
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import os
import sys
import urllib
import pydub
import speech_recognition as sr
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time
from datetime import datetime
import requests
import json
import stem.process
from stem import Signal
from stem.control import Controller
from selenium.common.exceptions import NoSuchElementException        
###made by xeonsim https://github.com/xeonsim ###
root = Tk()
root.geometry('500x400')
root.title("NFTs Upload to OpenSea With Recaptcha ")
input_save_list = ["NFTs folder :", 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0])
is_polygon = BooleanVar()
is_polygon.set(False)


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

# ask for directory on clicking button, changes button name.
def upload_folder_input():
    global upload_path
    upload_path = filedialog.askdirectory()
    Name_change_img_folder_button(upload_path)

def Name_change_img_folder_button(upload_folder_input):
    upload_folder_input_button["text"] = upload_folder_input

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
collection_link_input = InputField("OpenSea Collection Link:", 2, 0, 1)
start_num_input = InputField("Start Number:", 3, 0, 2)
end_num_input = InputField("End Number:", 4, 0, 3)
price = InputField("Price:", 5, 0, 4)
title = InputField("Title:", 6, 0, 5)
description = InputField("Description:", 7, 0, 6)
file_format = InputField("NFT Image Format:", 8, 0, 7)
external_link = InputField("External link:", 9, 0, 8)


###save inputs###
def save():
    input_save_list.insert(0, upload_path)
    collection_link_input.save_inputs(1)
    start_num_input.save_inputs(2)
    end_num_input.save_inputs(3)
    price.save_inputs(4)
    title.save_inputs(5)
    description.save_inputs(6)
    file_format.save_inputs(7)
    external_link.save_inputs(8)
   
###RECAPTCHA_SOLVE###


# _____MAIN_CODE_____
def main_program_loop():
    ###START###
    project_path = main_directory
    file_path = upload_path
    collection_link = collection_link_input.input_field.get()
    start_num = int(start_num_input.input_field.get())
    end_num = int(end_num_input.input_field.get())
    loop_price = float(price.input_field.get())
    loop_title = title.input_field.get()
    loop_file_format = file_format.input_field.get()
    loop_external_link = str(external_link.input_field.get())
    loop_description = description.input_field.get()

    ##chromeoptions
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(
        executable_path=project_path + "/chromedriver.exe",
        # chrome_options=opt,
        options=opt,
    )
    wait = WebDriverWait(driver, 240)
    driver.execute_cdp_cmd("Page.setBypassCSP", {"enabled": True})

    ###wait for methods
    def wait_css_selector(code):
        WebDriverWait(driver, 20).until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )
        
    

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))

    def delay(waiting_time=5):
        driver.implicitly_wait(waiting_time)

    def check_exists_by_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True
    
    def solve_recaptcha():
        global displayOk
        displayOk = check_exists_by_xpath('/html/body/div[9]/div/div/div/section/div/p')
        print(displayOk)
        if displayOk:
            try:
                iframes = driver.find_elements_by_tag_name("iframe")
                driver.switch_to.frame(iframes[0])
            except:
                pass
                
            try:
                check_button = WebDriverWait(driver, 10).until(ExpectedConditions.presence_of_element_located((By.XPATH,'//*[@id="recaptcha-anchor"]/div[1]')))
                
                check_button.click()
            except:
                pass

            try:
                driver.switch_to.default_content() 
                driver.switch_to.frame(iframes[-1])
            except:
                pass

            try:
                ssd=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#recaptcha-audio-button")))
                ssd.click()
                time.sleep(1)
            except:
                pass
                
            try:        # get the mp3 audio file
                delay()
                src = driver.find_element_by_id("audio-source").get_attribute("src")
                print(f"[INFO] Audio src: {src}")
                
                path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
                path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))
                
                    # download the mp3 audio file from the source
                urllib.request.urlretrieve(src, path_to_mp3)
            except:
                pass
                    

                # load downloaded mp3 audio file as .wav
            try:
                sound = pydub.AudioSegment.from_mp3(path_to_mp3)
                sound.export(path_to_wav, format="wav")
                sample_audio = sr.AudioFile(path_to_wav)
            except Exception:
                sys.exit(
                    "[ERR] Please run program as administrator or download ffmpeg manually, "
                    "https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/"
                )

            try: 
                # translate audio to text with google voice recognition
                delay()
                r = sr.Recognizer()
                with sample_audio as source:
                    audio = r.record(source)
                key = r.recognize_google(audio)
                print(f"[INFO] Recaptcha Passcode: {key}")

                # key in results and submit
                delay()
                driver.find_element_by_id("audio-response").send_keys(key.lower())
                driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)

                driver.switch_to.default_content()     
                time.sleep(2)  
            except:
                pass
            displayOk=False
           
            
   
    while end_num >= start_num:
        global displayOk
        displayOk= False
        print("Start creating NFT " +  loop_title + str(start_num))
        driver.get(collection_link)
        time.sleep(1)
        
        wait_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/span/a')
        additem = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/span/a')
        additem.click()
        time.sleep(1)
        
        wait_xpath('//*[@id="media"]')
        imageUpload = driver.find_element_by_xpath('//*[@id="media"]')
        imagePath = os.path.abspath(file_path + "\\" + str(start_num) + "." + loop_file_format)  # change folder here
        imageUpload.send_keys(imagePath)
       
        name = driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys(loop_title + str(start_num))  # +1000 for other folders #change name before "#"
        time.sleep(0.5)

        ext_link = driver.find_element_by_xpath('//*[@id="external_link"]')
        ext_link.send_keys(loop_external_link)
        time.sleep(0.5)

        desc = driver.find_element_by_xpath('//*[@id="description"]')
        desc.send_keys(loop_description)
        time.sleep(0.5)

        # Select Polygon blockchain if applicable

      
        # if is_polygon.get():
        #     blockchain_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/section/div/form/div[7]/div/div[2]')
        #     blockchain_button.click()
        #     polygon_button_location = '//span[normalize-space() = "Mumbai"]'
        #     wait.until(ExpectedConditions.presence_of_element_located(
        #         (By.XPATH, polygon_button_location)))
        #     polygon_button = driver.find_element(
        #         By.XPATH, polygon_button_location)
        #     polygon_button.click()
        if is_polygon.get(): 
            create = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/section/div[2]/form/div/div[1]/span/button') 
            driver.execute_script("arguments[0].click();", create) 
            time.sleep(1)
        
        
        create = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/section/div[2]/form/div/div[1]/span/button')
        driver.execute_script("arguments[0].click();", create)
        time.sleep(1)
        solve_recaptcha()
        solve_recaptcha()
        
        

        wait_css_selector("i[aria-label='Close']")
        cross = driver.find_element_by_css_selector("i[aria-label='Close']")
        cross.click()
        time.sleep(1)
      
        main_page = driver.current_window_handle
        wait_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div/span[2]/a')
        sell = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div/span[2]/a')
        sell.click()               

        wait_css_selector("input[placeholder='Amount']")
        amount = driver.find_element_by_css_selector("input[placeholder='Amount']")
        amount.click()
        amount.send_keys(str(loop_price))
        time.sleep(2)
        

        wait_css_selector("button[type='submit']")
        listing = driver.find_element_by_css_selector("button[type='submit']")
        listing.click()
        time.sleep(5)
        
        wait_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb fzwDgL']")
        sign = driver.find_element_by_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb fzwDgL']")
        sign.click()
        time.sleep(2)
        
        for handle in driver.window_handles:
            if handle != main_page:
                login_page = handle
        # change the control to signin page
        driver.switch_to.window(login_page)
        wait_css_selector("button[data-testid='request-signature__sign']")
        sign = driver.find_element_by_css_selector("button[data-testid='request-signature__sign']")
        sign.click()
        time.sleep(1)
        
        # change control to main page
        driver.switch_to.window(main_page)
        time.sleep(1)

        start_num = start_num + 1
        print('NFT creation completed!')

#####BUTTON ZONE#######
button_save = tkinter.Button(root, width=20, text="Save Form", command=save) 
button_save.grid(row=23, column=1)
button_start = tkinter.Button(root, width=20, bg="green", fg="white", text="Start", command=main_program_loop)
button_start.grid(row=25, column=1)
isPolygon = tkinter.Checkbutton(root, text='Polygon Blockchain', var=is_polygon)
isPolygon.grid(row=20, column=0)
open_browser = tkinter.Button(root, width=20,  text="Open Chrome Browser", command=open_chrome_profile)
open_browser.grid(row=22, column=1)
upload_folder_input_button = tkinter.Button(root, width=20, text="Add NFTs Upload Folder", command=upload_folder_input)
upload_folder_input_button.grid(row=21, column=1)
try:
    with open(save_file_path(), "rb") as infile:
        new_dict = pickle.load(infile)
        global upload_path
        Name_change_img_folder_button(new_dict[0])
        upload_path = new_dict[0]
except FileNotFoundError:
    pass
#####BUTTON ZONE END#######
root.mainloop()
