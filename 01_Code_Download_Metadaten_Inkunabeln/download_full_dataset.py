#!/usr/bin/env python
# coding: utf-8

# In[1]:


from platform import python_version
import os
import time

import pandas as pd
import regex as re
import bs4
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen


# In[2]:


print("Python version: " + python_version())
print("pandas version: " + pd.__version__)
print("regex version: " + re.__version__)
print("BeautifulSoup version: " + bs4.__version__)
print("Urllib.request version: " + urllib.request.__version__)


# In[3]:


filename = "Inkunabeln_Network_Ids.xlsx"


# In[4]:


df_network_id = pd.read_excel(filename)


# In[5]:


identifier_list = df_network_id["Network Id"].to_list()


# In[6]:


len(identifier_list)


# In[ ]:


counter = 0

for identifier in identifier_list:

    try:
        time.sleep(1.0)
        url = "https://swisscollections.ch/Record/" + str(identifier)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
        for script in soup(["script", "style"]):
            script.extract()
            text = soup.get_text()
            start = text.find("LEADER")
            stop = text.find("Basisinformationen")
            extract = text[start:stop]
            l = re.split("\n\n\n", extract)

            new_l = []
            for item in l:
                ga = item.replace("\n \n","   ")
                gb = ga.replace("\n", " ")
                gc = gb.replace("\xa0", " ")
                new_l.append(gc)

        with open(str(identifier) + ".txt", 'w', encoding="utf8") as f:
            for element in new_l:
                f.write(element)
                f.write("\n")
        
    except:
        print("Beim Datensatz " + str(identifier) + " hat etwas nicht geklappt.")
    
    counter = counter + 1
    
    print(str(counter) + ". Datensatz bearbeitet.")


# In[ ]:





# In[ ]:




