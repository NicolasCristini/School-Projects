
"""
Created on Tue Mar 16 16:28:27 2021

@authors: nicolascristini, Mark Sivolap, Ramon Jakobs
Assignment: Project n.2  Mystery Coffee
University of Utrecht Cotap
"""

### Import libraries

import pandas as pd
import random
import os
import bs4
import requests
import smtplib

### Defining the functions    

## Import the data from a .csv file. The answers are collected with microsoft forms,
## they are automatically updated in an excel sheet via microsoft flow/power automate
## and manually saved to a CSV file. 

def import_data(file_csv):
    
    # header names in the CSV file (name and e-mail of participants)
    #header_name = "name"
    #header_email = "email:"
    #header_country = "country:"
    
    # data has to be loaded everytime before next round        
    # load participant's data
    formdata = pd.read_csv(file_csv, sep=";")
    return formdata

## It matches partecipants from the list of names originated from the .csv file.
## The number of partecipants is asked out of the function and asked again if it is 
## out of the accapeted range.

def shuffle(names_list, group_n):

  while group_n > 5 or group_n < 2:
      print("Please provide a group number between 2 and 5:\t.")
      group_n = int(input("Please enter the group size"))

  #we need to randomize the list 
  random.shuffle(names_list)

  #Dividing into groups if group_n has no remainder
  list_n = []
  if int(len(names_list)) % group_n == 0:
      for i in range(0, len(names_list), group_n):
          list_n.append(names_list[i:i + group_n])
  #And then if groups do indeed have a remaidner 
  else:
      for i in range(0, len(names_list), group_n):
          list_n.append(names_list[i:i + group_n])
  for list in list_n:
      if len(list) < 2:
          list_n[0].extend(list) 
          list_n.remove(list)       
        
  return list_n


## Get a sentence from a random sentence generator in the web and print it with a special function

def generate_sentence(): 
    try:
        response = requests.get("https://conversationstartersworld.com/random-question-generator/")
        
    except Exception as err:
        print("Something went wrong:", err)
        response = None
        
    # if the GET was successful, print status code and content
    # (if available)
    if response!=None:
        print(response.status_code)
        
    if response.ok:
        #Trasform the response form the server in html text
        html_doc = response.text
        soup = bs4.BeautifulSoup(html_doc, "html.parser")
       
        #Find in this html the class that returns the automatically generated quote
        text = str(soup.find("blockquote", {"class" : "quotescollection-quote"}))
        
        #Cleane the quote and return it 
        quote = text.split("<p>")[1][:-17]
        return(quote)
        
    else:
        print("Something went wrong with status code", \
              response.status_code)



## Generate a text file fot each matched group with the greeting, names and random starter
## sentence

def make_files(groups_list, dataframe):
    for e in range(len(groups_list)):
        group_number = str(e)
        list_nationalities = []
        with open(str(base_dir + "/greetings_group" + group_number + ".txt"), "w") as file:
            file.write("Hi!\n")
            for member in groups_list[e]:
                member_country = dataframe[dataframe["name"] == str(member)]["country"]
                country = member_country.to_string()[5:]
                list_nationalities.append(str(country)) 
                file.write(member + ", ") 
            string_nationalities = ", ".join(list_nationalities)
            string = "\n\nIn this groups there are people from: " + f"\n{string_nationalities}" + "\nTry to guess who is from where ;)"
            file.writelines(["\n\nYou have been matched with the other partecipants of this group!", "\nEnjoy this coffee time during this covid-situation", f"{string}",\
                                     "\n\nThis is the question of the day to kick off your conversation:\n",\
                                         f"<<<{generate_sentence()}>>>"])


## Automatically send a mail from an outlook account using the SMTP library

def send_email(sender_mail, pwd, list_names, list_receivers, subject, text):
    
#Set the SMTP server
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    MY_ADDRESS= sender_mail
    MY_PASSWORD= pwd
    s.login(MY_ADDRESS,MY_PASSWORD)
    names= list_names
    emails=list_receivers
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

# For each contact, send the email:
    for name, email in zip(names, emails):
      # create a message
        msg = MIMEMultipart()      
        message = text

    # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']= subject

    # add in the message body
        msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
        s.send_message(msg)
    
        del msg
        print("Message sent!.")

## Use the function send_mail() to send the generated sentence and the greetings to the partecipants of the same group

def matching_mail(groups_list, dataframe):

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
    for e in range(len(groups_list)):
        group_number = str(e)
        text_file = str(base_dir + "/greetings_group" + group_number + ".txt")
        list_names_group = []
        list_emails = []
        for member in groups_list[e]: 
            member_mail = dataframe[dataframe["name"] == str(member)]["email"]
            list_emails.append(member_mail.to_string()[5:])
            list_names_group.append(member)
        with open(text_file, "r") as file:  
 # Create a text/plain message
            content = file.read()
            #The sender account and password  have been creatd for this course
            send_email(sender_mail = "NicolasCristini22@outlook.com",\
                        pwd = 'SendMailPassword',\
                        list_receivers = list_emails,\
                        list_names = list_names_group,\
                        subject = 'Matching_group', \
                        text = content)





### EXECUTION OF THE PROGRAM, CALLING THE FUNCTIONS

#0
#Find the working directory that will be necessary later 
    
base_dir = os.getcwd()
print(base_dir)


#1
### OUTPUT OF IMPORT DATA FUNCTION

partecipants_csv = "Mystery Coffee.csv"

data = import_data(partecipants_csv)
list_of_names = data["name"].to_list()
mail_list = data["email"].to_list()
country_list = data["country"].to_list()

#2
### MATCHING THE GROUPS 

#ask for the number of partecipants the user wants in each group.
#If it will be asked again it

number_participants = int(input("Please enter the group size:\t"))
list_of_groups = shuffle(list_of_names, number_participants)


#3
### CREATE TXT FILES AND SEND MAIL FOR EACH GROUP

make_files(list_of_groups, data)
matching_mail(list_of_groups, data)

