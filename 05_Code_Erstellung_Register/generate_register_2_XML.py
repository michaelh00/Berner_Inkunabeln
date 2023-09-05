#!/usr/bin/env python
# coding: utf-8

# In[1]:


from platform import python_version
import os
import ast
from collections import defaultdict

import pandas as pd
import jinja2
from jinja2 import Template
import regex as re


# In[2]:


print("Python version: " + python_version())
print("Pandas version: " + pd.__version__)
print("Jinja2 version: " + jinja2.__version__)
print("Regex version: " + re.__version__)


# In[ ]:


# Pfad zum Ordner, in dem sich die nachbearbeiteten Inkunabeldatensätze befinden
data_path = r"..."


# In[ ]:


# Pfad zum Ordner, in dem das mit diesem Script erstellte xml-Dokument abgelegt werden soll
output_path = r"..."


# In[ ]:


places_and_people_all_data = []
reference_all_data = []

for item in os.listdir(data_path):
    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()

        reg_2_recognition_start = "<-REGISTER-2-START->\n"
        reg_2_recognition_stop = "<-REGISTER-2-STOP->\n"
        reg_2_content_start = lines.find(reg_2_recognition_start)
        reg_2_content_stop = lines.find(reg_2_recognition_stop)
        reg_2_content_range = lines[reg_2_content_start + len(reg_2_recognition_start) : reg_2_content_stop]
        reg_2_content = re.findall("<-O-START->(.*?)<-O-STOP->\n<-P-START->(.*?)<-P-STOP->", reg_2_content_range)

        reference_recognition_start = "<-REGISTER-REF-START->\n"
        reference_recognition_stop = "<-REGISTER-REF-STOP->\n"
        reference_content_start = lines.find(reference_recognition_start)
        reference_content_stop = lines.find(reference_recognition_stop)
        reference_content_range = lines[reference_content_start + len(reference_recognition_start) : reference_content_stop]
        reference_doi = re.findall("<-DOI-START->(.*?)<-DOI-STOP->", reference_content_range)[0]
        reference_number = re.findall("<-Nr-START->(.*?)<-Nr-STOP->", reference_content_range)[0]
        reference_signature = re.findall("<-SIGN-START->(.*?)<-SIGN-STOP->", reference_content_range)[0]
    
    places_and_people_all_data.append(reg_2_content)
    
    references = [reference_doi, reference_number, reference_signature]
    reference_all_data.append(references)


# In[ ]:


filedict = defaultdict(list)


# In[ ]:


for index, place_and_person in enumerate(places_and_people_all_data):
    for item in place_and_person:
        if reference_all_data[index] not in filedict[item]:
            filedict[item].append(reference_all_data[index])


# In[ ]:


sorted_tuples = sorted(filedict.items())


# In[ ]:


filedict_sorted = dict(sorted_tuples)


# ---

# In[ ]:


path_excelfile = "Vorgaben_Registersortierung/"


# In[ ]:


excelfile = "Register_2_Wunschsortierung.xlsx" 


# In[ ]:


df_sortierliste = pd.read_excel(path_excelfile + excelfile, header=None, names=["printers"])


# In[ ]:


index_sorted_str = df_sortierliste["printers"].to_list()
index_sorted = [tuple(map(str, ast.literal_eval(s))) for s in index_sorted_str]
len(index_sorted)


# In[ ]:


index_unsorted = list(filedict_sorted.keys())
len(index_unsorted)


# In[ ]:


l_drin = []
l_nichtdrin = []

for item in index_unsorted:
    if item in index_sorted:
        l_drin.append(item)
    else:
        l_nichtdrin.append(item)


# In[ ]:


len(l_drin)


# In[ ]:


len(l_nichtdrin)


# In[ ]:


printer_dict_custom_sorted = {k: filedict_sorted[k] for k in index_sorted if k in filedict_sorted}


# In[ ]:


list_of_dictionaries = []

for key, value in printer_dict_custom_sorted.items():
    
    place_dict = {}
    place = key[0]
    printer = key[1]
    references = value
    
    place_dict.update({place : {printer : references}})
    list_of_dictionaries.append(place_dict)


# In[ ]:


final_dict = defaultdict(list)


# In[ ]:


for sub in list_of_dictionaries:
    for key in sub:
        final_dict[key].append(sub[key])


# In[ ]:


template = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE book-part-wrapper PUBLIC "-//NLM//DTD BITS Book Interchange DTD v2.1 20220202//EN" "BITS-book2-1.dtd">
<book-part-wrapper dtd-version="2.1" xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML" xml:lang="de">
  <book-meta>
    <book-title-group>
      <book-title>Die Inkunabeln in der Universitätsbibliothek Bern</book-title>
    </book-title-group>
    <contrib-group>
      <contrib>
        <name>
          <surname>Bürger</surname>
          <given-names>Ulrike</given-names>
        </name>
        <role>Redaktionelle Mitarbeit</role>
      </contrib> 
      <contrib>
        <name>
          <surname>Fricke</surname>
          <given-names>Fabian</given-names>
        </name>
        <role>Mitarbeit an der Herausgabe</role>
      </contrib>  
      <contrib>
        <name>
          <surname>Hanschke</surname>
          <given-names>Petra</given-names>
        </name>
        <role>Mitarbeit an der Herausgabe</role>
      </contrib>   
      <contrib>
        <name>
          <surname>Hartmann</surname>
          <given-names>Volker</given-names>
        </name>
        <role>Mitarbeit an der Herausgabe</role>
      </contrib>
      <contrib>
        <name>
          <surname>Horn</surname>
          <given-names>Michael</given-names>
        </name>
        <role>Projektkoordination, technische Umsetzung, redaktionelle Mitarbeit</role>
      </contrib>
      <contrib>
        <name>
          <surname>Jolidon</surname>
          <given-names>Anne</given-names>
        </name>
        <role>Mitarbeit an der Herausgabe</role>
      </contrib>
      <contrib>
        <name>
          <surname>Matter</surname>
          <given-names>Stefan</given-names>
        </name>
        <role>Redaktionelle Mitarbeit</role>
      </contrib>
      <contrib>
        <name>
          <surname>Meier</surname>
          <given-names>Denis</given-names>
        </name>
        <role>Mitarbeit technische Umsetzung</role>
      </contrib>
      <contrib>
        <name>
          <surname>Pellin</surname>
          <given-names>Elio</given-names>
        </name>
        <role>Mitarbeit technische Umsetzung</role>
      </contrib>
      <contrib>
        <name>
          <surname>Schlüter</surname>
          <given-names>Sabine</given-names>
        </name>
        <role>Herausgeberin</role>
      </contrib>
      <contrib>
        <name>
          <surname>Stocker</surname>
          <given-names>Mathias</given-names>
        </name>
        <role>Mitarbeit technische Umsetzung</role>
      </contrib>
      <contrib>
        <name>
          <surname>Stutzmann</surname>
          <given-names>Jan</given-names>
        </name>
        <role>Mitarbeit technische Umsetzung</role>
      </contrib>
    </contrib-group>
    <pub-date>
      <year>2023</year>
    </pub-date>
    <isbn>978-3-03917-072-2</isbn>
    <publisher>
      <publisher-name>Bern Open Publishing</publisher-name>
      <publisher-loc>Bern</publisher-loc>
    </publisher>
    <edition>1</edition>
    <kwd-group>
      <kwd></kwd>
    </kwd-group>
    </book-meta>
    <index>
      <index-title-group>
        <title>Drucker, Verleger, Buchhändler nach Orten</title>
      </index-title-group>  
      {% for key, value in place_printer_reference_dict.items() %}
      <index-entry>
        <term>{{key}}</term>
        {% for val in value %}
        {% for k, v in val.items() %}
          <index-entry>
            <term>{{k}}</term>
              <nav-pointer-group>
              {% for item in v %}                      
                  <nav-pointer>
                    <ext-link ext-link-type="doi" xlink:href="{{item[0]}}">{{item[1]}}</ext-link>
                  </nav-pointer>
              {% endfor %}
              </nav-pointer-group>
          </index-entry>
        {% endfor%}
        {% endfor%}
      </index-entry> 
      {% endfor %}
    </index>
</book-part-wrapper>
'''


# In[ ]:


data = {
    "place_printer_reference_dict" : final_dict
}


# In[ ]:


t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)


# In[ ]:


with open(output_path + "Register_2_sortiert.xml", 'w', encoding='utf8') as file:
    file.write(bits)

