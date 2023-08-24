#!/usr/bin/env python
# coding: utf-8

# In[1]:


from platform import python_version
import os

import openpyxl
from openpyxl import load_workbook
import pandas as pd
import regex as re
import urllib


# In[2]:


print("Python version: " + python_version())
print("Openpyxl version: " + openpyxl.__version__)
print("Pandas version: " + pd.__version__)
print("Regex version: " + re.__version__)
print("Urllib version: " + urllib.request.__version__)


# In[3]:


data_path = r"../10_Daten_Grundlage/"
path_legend = "../11_Daten_Legenden/"


# In[4]:


# Pfad zum Ordner, in dem die mit diesem Script nachbearbeiteten Datensätze abgelegt werden sollen
output_path = r"data/"


# In[5]:


excelfile = "information_id_img_leg.xlsx"


# In[6]:


df = pd.read_excel(excelfile, dtype={"MMS-ID": str})


# In[7]:


testliste = df["MMS-ID"].to_list()


# In[8]:


dedub = []
for item in testliste:
    if item not in dedub:
        dedub.append(item)
    else:
        pass


# In[9]:


dct_relevant_info = {k: g["Name Bild und Legende"].tolist() for k,g in df.groupby("MMS-ID")}


# In[10]:


for index, filename in enumerate(os.listdir(data_path)):
    
    with open(data_path + filename, "r", encoding='utf8') as file:
        lines = file.read()

        s_1_1 = "<-1-1-START->\n"
        st_reg = "<-REGISTER-REF-STOP->\n"

        m_orig_start = "<-ORIGINAL-MARC-DATENSATZ-SWISSCOLLECTIONS-START->\n"
        m_orig_stop = "<-ORIGINAL-MARC-DATENSATZ-SWISSCOLLECTIONS-STOP->\n\n"


        start_1_1 = lines.find(s_1_1)
        stop_inc_ref = lines.find(st_reg)

        content = lines[start_1_1 : stop_inc_ref + len(st_reg)]

        pattern = r'"(.*?)"'

        def replace(match):
            return f'«{match.group(1)}»'

        content_with_guillemets = re.sub(pattern, replace, content)

        marc_orig_start = lines.find(m_orig_start)
        marc_orig_stop = lines.find(m_orig_stop)
        marc_orig = lines[marc_orig_start : marc_orig_stop + len(m_orig_stop)]

        l = content_with_guillemets.replace("->; <-VI-5-START->", "->; <-L-5-START-><-L-5-STOP-><-VI-5-START->")
        l2 = l.replace("<-5-1-START->\n<-VI-5-START->", "<-5-1-START->\n<-L-5-START-><-L-5-STOP-><-VI-5-START->")
        lines_with_number = l2.replace("<-Nr-START->LAUFNUMMER<-Nr-STOP->", "<-Nr-START->" + str(index + 1) + "<-Nr-STOP->")

    with open(output_path + filename, "w+", encoding='utf8') as file_output:
        file_output.write("\ufeff")
        file_output.write(lines_with_number) 
        file_output.write("\n\n\n")
        file_output.write(marc_orig)
        
        if filename[-22:-4] in dct_relevant_info.keys():
            value = dct_relevant_info[filename[-22:-4]]

            file_output.write("\n")
            file_output.write("<-BILDINFORMATIONEN-START->\n")
            for index, val in enumerate(value):
                val_url = urllib.parse.quote(val, safe='/', encoding=None, errors=None)
                file_output.write("<-BILD-START->" + str(val_url) + ".tif" + "<-BILD-STOP->\n")
                with open(path_legend + str(val) + ".txt", "r", encoding="utf8") as legend_file:
                    legend_lines = legend_file.read()
                    th_l_1 = re.search("\ufeff(.+?)\n\n", legend_lines)
                    th_l_2 = th_l_1.group(1)
                file_output.write("<-LEGENDE-START->" + str(th_l_2) + "<-LEGENDE-STOP->\n")
            file_output.write("<-BILDINFORMATIONEN-STOP->\n")
        


# In[ ]:




