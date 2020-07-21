from telethon.sync import TelegramClient, events
import configparser
from telethon import utils
from tqdm import tqdm
import time
import random
'''
config = configparser.ConfigParser()
config.read("config.ini")
'''
# Setting configuration values
api_id = 1691230
api_hash = '3691002563fda04ab7eaf714691ac7ca'

#api_hash = str(api_hash)

phone = +918310160935
username = '@adiakagami'

news_papers = ['Editorial-Business Standard',
 'The-Hindu',
 'Editorial-Indian-Express',
 'Editorial-The-Hindu',
 'Indian Express']

while True:
    with TelegramClient('newsbot',api_id,api_hash) as client:
    
        messages = client.get_messages('https://t.me/UpscMaterials',limit=10000)
        print('messages no: ',len(messages))
        
        count = 0
        required_files = 0
        exception_count = 0
        
        for msg in messages:
            count +=1
            #print('message no: ',count, msg.id)
            #print('message :', msg.message)
            try:
                pdf_name = msg.media.document.attributes[0].file_name
            except:
                exception_count +=1
                continue
              
            for x in news_papers:
                    if x in pdf_name:
                        print('message no: ',count)
                        yn = input("do you want to download " + msg.media.document.attributes[0].file_name + " ?")
                        if yn == 'y':
                            required_files +=1
                            client.download_media(msg)
                            print("downloaded "+msg.media.document.attributes[0].file_name)
                            break

                            #if count%2000 == 1 or count%2000 == 2:  #this condition allowed to download atmax 2 files.
                                    
                            

                        elif yn == 'n':
                            print("skipped "+msg.media.document.attributes[0].file_name)
                
            
            count +=1
            
        print('Total messaged :', count)
        print('required files: ', required_files)
        print('Other messages :', exception_count)
        time.sleep(120)   #code is automated, runs every 2 minutes

client.run_until_disconnected()
   
        


    
 