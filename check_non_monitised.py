#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Sun Oct 21 18:42:08 2018

@author: Amit Upreti
"""

import random
import csv
import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import time
import pafy
from langdetect import detect

input_f = input('Please enter input csv file name: ')
output_f = input('Please enter output csv file name: ')


with open(output_f, 'a', newline='') as csvf:
    csv_writer = csv.writer(csvf)
    csv_writer.writerow(['Title','Links'])

ext_file = 'User-Agent-Switcher-for-Chrome_v1.0.43.zip'

try:
    data = pd.read_csv(input_f, encoding='latin-1')
except:
    data = pd.read_csv(input_f)

# Add extension

chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension(ext_file)

chrome_options.add_extension('aailiojlhjbichheofhdpcongebcgcgm.zip')

# Start driver

driver = webdriver.Chrome(chrome_options=chrome_options)

print ('Waiting for 30 second\n Please select the  windows firefox 33 using the user agent spoofer extension')
sleep(30)

clear = lambda : print('\n'*100)
new = pd.DataFrame(columns=['Title', 'Links'])

count = 0
print ('*' * 40)
print ('\t\t\tBeginnnng search for spanish titles\n')
print ('*' * 40)
start_time = time.time()
data = data[:100]
num = len(data)
for i in range(len(data)):
    curr_title = data['Title'][i]
    curr_link = data['Links'][i]

    try:
        if detect(curr_title) == 'es' and 'concierto' not in curr_title \
            and 'kareoke' not in curr_title and 'corridos' \
            not in curr_title and 'covers' not in curr_title \
            and 'en vivo' not in curr_title and 'zumba' \
            not in curr_title:
            clear()
            print ('\t\tTotal Rows:', num)
            print ('\t\t', detect(curr_title), ' detected: ',
                   curr_title)
            new = new.append({'Title': curr_title, 'Links': curr_link},
                             ignore_index=True)
            print ('\t\t', count, ' Spanish titles found out of ', i)
            print ('\t\t', 'Remaining Rows:', num - i)
            print ('\t\t', 'Time:', '%s seconds ' % (time.time()
                   - start_time))
            count += 1
    except Exception as e:
        print ('Error while checking title ', curr_title, '\nError: ', e)

print ('*' * 60)
print (count, ' Spanish  titles found.')
print ('*' * 60)

monitized = pd.DataFrame(columns=['Title', 'Links'])

count = 0
curr = time.time()
for i in range(len(new)):
    link = new['Links'][i]
    driver.get(link)
    try:
        myElem = WebDriverWait(driver,
                               10).until(EC.presence_of_element_located((By.ID,
                'freedom_monetization')))
        status = \
            driver.find_element_by_xpath('//*[@id="freedom_monetization"]'
                ).text
        clear()
        print ('Total links:', len(new))
        print (status, '-', link)
        print ('Current link:', i + 1)
        print ('Remaining : ', len(new) - i + 1)
        if 'Not monetized' in status:
            try:
                print ('Adding ', link)
                vid = pafy.new(link)
                length = int(vid.length)
                print ('length:', length)

                if length >= 120 and length <= 480:

                    with open(output_f, 'a', newline='') as csvf:
                        csv_writer = csv.writer(csvf)
                        csv_writer.writerow([new['Title'][i], link])



                    #monitized = monitized.append({'Title': new['Title'][i], 'Links': link}, ignore_index=True)

                    count += 1
                else:
                    print ('Length:', length)
                    print ('Skipping')
            except:
                print( 'error with video')
        else:
            print ('Skipping')
        print ('Time:', '%s seconds ' % (time.time() - curr))
    except TimeoutException:
        print ('Loading took too much time for video!', link)

    # sleep(random.randint(1,8))

print ()
print ('*' * 30)

print (count, 'Not Monitised video with length 2-7 found')
print ('Total Time:', '%s seconds ' % (time.time() - start_time))
#print ('writing to the csv file', output_f)
#monitized = pd.DataFrame(monitized)
#try:
#    monitized.to_csv(output_f, index=False)
#    print 'Write succesfull'
#except:
#    print 'Error couldnot write to file'
