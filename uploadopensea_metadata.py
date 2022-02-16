
import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO
import os
import io
import sys
import pickle
import time
from decimal import *
import webbrowser
from numpy import inner
from numpy import imag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import Select
import json 
import requests
import pydub
import speech_recognition as sr
import stem.process
from stem import Signal
from stem.control import Controller
from selenium.common.exceptions import NoSuchElementException  
 

root = Tk()

root.geometry('700x700')
root.resizable(False, False)
root.title("NFTs Upload to OpenSea ")

input_save_list = ["NFTs folder :", 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0])


def supportURL():
    webbrowser.open_new("https://opensea.io/collection/s-o-n--n-e-t")

def coffeeURL():
    webbrowser.open_new("https://github.com/xeonsim/opensea-upload-with-recaptcha-solution")

class WebImage:
    def __init__(self, url):
        h = { 'User-Agent': 'Neo'}
        r = requests.get(url, headers=h)
        
        image = Image.open(io.BytesIO(r.content))
            
        image.resize((100, 200))     
        self.image = ImageTk.PhotoImage(image)

    def get(self):
        return self.image
imageurl = "https://lh3.googleusercontent.com/1uSHeqz_2qxP-IYAXb_YXzjhG8G7ypTkcCvxXz8_7GTBOfkd31K06UrJTG5QuBIr-vtljGCcQoRoc8RF6z3G3tpPDo7heSvh1HL1KQ=s130"
img = WebImage(imageurl).get()
imagelab = tk.Label(root, image=img)
imagelab.grid(row=0, columnspan=1)
imagelab.bind("<Button-1>", lambda e:supportURL())
imageurl2 = "https://lh3.googleusercontent.com/1uSHeqz_2qxP-IYAXb_YXzjhG8G7ypTkcCvxXz8_7GTBOfkd31K06UrJTG5QuBIr-vtljGCcQoRoc8RF6z3G3tpPDo7heSvh1HL1KQ=s130"
img2 = WebImage(imageurl2).get()
imagelab2 = tk.Label(root, image=img2)
imagelab2.grid(row=0, columnspan=2)
imagelab2.bind("<Button-2>", lambda e:supportURL())

is_polygon = BooleanVar()
is_polygon.set(True)

is_listing = BooleanVar()
is_listing.set(True)

is_numformat = BooleanVar()
is_numformat.set(False)






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
    #return os.path.join(sys.path[0], "Save_file.cloud")
    return os.path.join(sys.path[0], "Save_gui.cloud")


# ask for directory on clicking button, changes button name.
def upload_folder_input():
    global upload_path
    upload_path = filedialog.askdirectory()
    Name_change_img_folder_button(upload_path)

def Name_change_img_folder_button(upload_folder_input):
    upload_folder_input_button["text"] = upload_folder_input

def is_numeric(val):
        if str(val).isdigit():
                return True
        elif str(val).replace('.','',1).isdigit():
                return True
        else:
                return False

class InputField:
    def __init__(self, label, row_io, column_io, pos,  master=root):
        self.master = master
        self.input_field = Entry(self.master, width=60)
        self.input_field.grid(ipady=3)
        self.input_field.label = Label(master, text=label, anchor="w", width=20, height=1 )
        self.input_field.label.grid(row=row_io, column=column_io, padx=12, pady=2)
        self.input_field.grid(row=row_io, column=column_io + 1, padx=12, pady=2)
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
        #messagebox.showwarning("showwarning", "Warning")
        input_save_list.insert(pos, self.input_field.get())
        with open(save_file_path(), "wb") as outfile:
            pickle.dump(input_save_list, outfile)

    def validate_inputs(self, maxlen, type, message):

        if type == 0 and (len(self.input_field.get()) == 0 or (self.input_field.get()).isdigit() != True or len(self.input_field.get()) > maxlen):
            messagebox.showwarning("showwarning", message)

        elif type == 1 and (len(self.input_field.get()) == 0 or is_numeric(self.input_field.get()) == False or len(self.input_field.get()) >= maxlen):
            messagebox.showwarning("showwarning", message)

        elif type == 2 and ( len(self.input_field.get()) == 0 or len(self.input_field.get()) > maxlen):
            messagebox.showwarning("showwarning", message)

        else:
            return True


###input objects###
collection_link_input = InputField("OpenSea Collection Link:", 2, 0, 1)
start_num_input = InputField("Start Number:", 3, 0, 2)
end_num_input = InputField("End Number:", 4, 0, 3)
price = InputField("Default Price:", 5, 0, 4)
title = InputField("Title:", 6, 0, 5)
description = InputField("Description:", 7, 0, 6)
file_format = InputField("NFT Image Format:", 8, 0, 7)
external_link = InputField("External link:", 9, 0, 8)

###save inputs###
def save():

    if len(start_num_input.input_field.get()) == 0 or len(end_num_input.input_field.get()) == 0 or (int(end_num_input.input_field.get()) < int(start_num_input.input_field.get())):
        #messagebox.showwarning("showwarning", "End number should greater than start number!")
        #return True
        print("true")
    elif len( start_num_input.input_field.get()) == 0 or len(end_num_input.input_field.get()) > 4 :
        #messagebox.showwarning("showwarning", "Start / end number range 0 - 9999")
        #return True
        print ("true")
    else:
        collection_link_input.validate_inputs(200, 2, 'Collection link required')
        price.validate_inputs(100, 1, 'Price required')
        title.validate_inputs(100, 2, 'title required')
        description.validate_inputs(100, 2, 'description required')
        file_format.validate_inputs(100, 2, 'file format required - png, jpg, jpeg')
        external_link.validate_inputs(100, 3, '')


    input_save_list.insert(0, upload_path)
    collection_link_input.save_inputs(1)
    start_num_input.save_inputs(2)
    end_num_input.save_inputs(3)
    price.save_inputs(4)
    title.save_inputs(5)
    description.save_inputs(6)
    file_format.save_inputs(7)
    external_link.save_inputs(8)



# _____MAIN_CODE_____
def main_program_loop():
 ###START###
    if len(end_num_input.input_field.get()) > 4 :
        messagebox.showwarning("showwarning", "Start / end number range 0 -9999")
        sys.exit()

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
        chrome_options=opt,
    )
    wait = WebDriverWait(driver, 60)

    def check_exists_by_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True
    ###wait for methods
    def delay(waiting_time=5):
        driver.implicitly_wait(waiting_time)

    def wait_css_selector(code):
        wait.until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))

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
        if is_numformat.get():
            start_numformat = f"{ start_num:04}"
        else:
             start_numformat = f"{ start_num:01}"

        try:
            server_error=WebDriverWait(driver, 5).until(ExpectedConditions.presence_of_element_located((By.XPATH,'/html/body/pre'))).get_attribute('innerHTML')
            if server_error =='Internal Server Error':
                driver.get(collection_link)
                print('server error happend')
        except:
            pass

        print("Start creating NFT " +  loop_title + str(start_numformat))
        print('number ',  start_numformat)
        driver.get(collection_link)


        wait_xpath('//*[@id="media"]')
        imageUpload = driver.find_element_by_xpath('//*[@id="media"]')
        imagePath = os.path.abspath(file_path + "\\images\\" + str(start_numformat) + "." + loop_file_format)  # change folder here
        imageUpload.send_keys(imagePath)
        time.sleep(0.8)

        name = driver.find_element_by_xpath('//*[@id="name"]')
        name.send_keys(loop_title + str(start_numformat))  # +1000 for other folders #change name before "#"

        time.sleep(0.8)

        ext_link = driver.find_element_by_xpath('//*[@id="external_link"]')
        ext_link.send_keys(loop_external_link)
        time.sleep(0.8)

        desc = driver.find_element_by_xpath('//*[@id="description"]')
        desc.send_keys(loop_description)
        time.sleep(0.8)

        #jsonData = JSON(file_path + "/json/"+ str(start_num) + ".json").readFromFile()

        jsonFile = file_path + "/json/"+ str(start_numformat) + ".json"
        if os.path.isfile(jsonFile) and os.access(jsonFile, os.R_OK):

            #print(str(jsonMetaData))
            wait_css_selector("button[aria-label='Add properties']")
            properties = driver.find_element_by_css_selector("button[aria-label='Add properties']")
            driver.execute_script("arguments[0].click();", properties)
            time.sleep(0.8)

            # jsonData = JSON(os.getcwd() + "/data/"+ str(start_num) + ".json").readFromFile()
            # jsonMetaData = jsonData['attributes']

             # checks if file exists
            jsonData = json.loads(open(file_path + "\\json\\"+ str(start_numformat) + ".json").read())

        jsonMetaData = jsonData['attributes']

        for key in jsonMetaData:
            input1 = driver.find_element_by_xpath('//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[1]/div/div/input')
            input2 = driver.find_element_by_xpath('//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[2]/div/div/input')
           
            input1.send_keys(str(key['trait_type']))
            input2.send_keys(str(key['value']))
                # driver.find_element_by_xpath('//button[text()="Add more"]').click()
            addmore_button = driver.find_element_by_xpath('//button[text()="Add more"]')
            driver.execute_script("arguments[0].click();", addmore_button)
            time.sleep(0.9)

            driver.find_element_by_xpath('//button[text()="Save"]').click()
            time.sleep(0.8)



        # Select Polygon blockchain if applicable
        #if is_polygon.get():
            # blockchain_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/section/div/form/div[7]/div/div[2]')
            # blockchain_button.click()
            # polygon_button_location = '//span[normalize-space() = "Mumbai"]'
            # wait.until(ExpectedConditions.presence_of_element_located(
            #     (By.XPATH, polygon_button_location)))
            # polygon_button = driver.find_element(
            #     By.XPATH, polygon_button_location)
            # polygon_button.click()


        create = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/section/div[2]/form/div/div[1]/span/button')
        driver.execute_script("arguments[0].click();", create)
        time.sleep(0.8)
        solve_recaptcha()
        solve_recaptcha()

        # wait_css_selector("i[aria-label='Close']")
        # cross =
        driver.find_element_by_css_selector("i[aria-label='Close']")
        # cross.click()

        wait_xpath('/html/body/div[5]/div/div/div/div[2]/button/i')
        cross = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[2]/button/i')
        cross.click()
        time.sleep(0.8)

        main_page = driver.current_window_handle

        if is_listing.get():
            wait_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div/span[2]/a')
            sell = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div/span[2]/a')
            sell.click()

            wait_css_selector("input[placeholder='Amount']")
            amount = driver.find_element_by_css_selector("input[placeholder='Amount']")
            amount.send_keys(str(loop_price))
            time.sleep(1)

            wait_css_selector("button[type='submit']")
            listing = driver.find_element_by_css_selector("button[type='submit']")
            listing.click()
            time.sleep(10)

            #for Live
            #wait_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb fzwDgL']")
            #signcomplete = driver.find_element_by_css_selector("button[class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 bhqEJb fzwDgL']")
            #signcomplete.click()

       #driver.execute_script("arguments[0].click();", signcomplete)

            if is_polygon.get():
                driver.find_element_by_xpath('//button[text()="Sign"]').click()
                time.sleep(1)

            for handle in driver.window_handles:
                if handle != main_page:
                    login_page = handle
                    #break
            # change the control to signin page
            driver.switch_to.window(login_page)
            wait_css_selector("button[data-testid='request-signature__sign']")
            sign = driver.find_element_by_css_selector("button[data-testid='request-signature__sign']")
            sign.click()
            time.sleep(1)

        #change control to main page
        driver.switch_to.window(main_page)
        time.sleep(0.7)

        start_num = start_num + 1
        print('NFT creation completed!')

#####BUTTON ZONE#######
# isnumFormat = tkinter.Checkbutton(root, text='Number format 0001 ~ 9999', var=is_numformat, width=49, anchor="w")
# isnumFormat.grid(row=18, column=1)
isCreate = tkinter.Checkbutton(root, text='Complete Listing', var=is_listing, width=49, anchor="w")
isCreate.grid(row=19, column=1)
isPolygon = tkinter.Checkbutton(root, text='Polygon Blockchain', var=is_polygon, width=49, anchor="w")
isPolygon.grid(row=20, column=1)
upload_folder_input_button = tkinter.Button(root, width=50, height=1,  text="Add NFTs Upload Folder", command=upload_folder_input)
upload_folder_input_button.grid(row=21, column=1, padx=2)
open_browser = tkinter.Button(root, width=50, height=1,  text="Open Chrome Browser", command=open_chrome_profile)
open_browser.grid(row=23, column=1, pady=2)
button_save = tkinter.Button(root, width=50, height=1,  text="Save This Form", command=save)
button_save.grid(row=22, column=1, pady=2)
button_start = tkinter.Button(root, width=44, height=2, bg="green", fg="white", text="Start", command=main_program_loop)
button_start['font'] = font.Font(size=10, weight='bold')
button_start.grid(row=25, column=1, pady=2)
footer = tkinter.Button(root, height=3, width=60, text='Do you you want to show support? \n Now you have the chance to buy me a coffee. Thank you.',  command=coffeeURL, relief=GROOVE  )
footer.grid(row=31, columnspan=2, padx=31, pady=31)


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