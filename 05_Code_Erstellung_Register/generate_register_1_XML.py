#!/usr/bin/env python
# coding: utf-8

# In[1]:


from platform import python_version
import os
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


people_all_data = []
reference_all_data = []

for item in os.listdir(data_path):
    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()

        reg_1_recognition_start = "<-REGISTER-1-START->\n"
        reg_1_recognition_stop = "<-REGISTER-1-STOP->\n"
        reg_1_content_start = lines.find(reg_1_recognition_start)
        reg_1_content_stop = lines.find(reg_1_recognition_stop)
        reg_1_content_range = lines[reg_1_content_start + len(reg_1_recognition_start) : reg_1_content_stop]
        reg_1_content = re.findall("<-P-START->(.*?)<-P-STOP->", reg_1_content_range)

        reference_recognition_start = "<-REGISTER-REF-START->\n"
        reference_recognition_stop = "<-REGISTER-REF-STOP->\n"
        reference_content_start = lines.find(reference_recognition_start)
        reference_content_stop = lines.find(reference_recognition_stop)
        reference_content_range = lines[reference_content_start + len(reference_recognition_start) : reference_content_stop]
        reference_doi = re.findall("<-DOI-START->(.*?)<-DOI-STOP->", reference_content_range)[0]
        reference_number = re.findall("<-Nr-START->(.*?)<-Nr-STOP->", reference_content_range)[0]
        reference_signature = re.findall("<-SIGN-START->(.*?)<-SIGN-STOP->", reference_content_range)[0]
    
    people_all_data.append(reg_1_content)
    
    references = [reference_doi, reference_number, reference_signature]
    reference_all_data.append(references)


# In[ ]:


filedict = defaultdict(list)


# In[ ]:


for index, author in enumerate(people_all_data):
    for item in author:
        if reference_all_data[index] not in filedict[item]:
            filedict[item].append(reference_all_data[index])


# In[ ]:


sorted_dict = sorted(filedict.items())


# In[ ]:


filedict_sorted = dict(sorted_dict)


# ---

# In[ ]:


path_excelfile = "Vorgaben_Registersortierung/"


# In[ ]:


excelfile = "Register_1_Wunschsortierung.xlsx" 


# In[ ]:


df_sortierliste = pd.read_excel(path_excelfile + excelfile, header=None, names=["authors"])


# In[ ]:


index_sorted = df_sortierliste["authors"].to_list()
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


auth_dict_custom_sorted = {k: filedict_sorted[k] for k in index_sorted if k in filedict_sorted}


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
        <title>Autorinnen und Autoren, Herausgeber, Übersetzer, Illustratoren</title>
      </index-title-group>  
    {% for key, value in author_reference_dict.items() %}
      <index-entry>
        <term>{{key}}</term>
          <nav-pointer-group>
            {% for element in value %}
              <nav-pointer>
                <ext-link ext-link-type="doi" xlink:href="{{element[0]}}">{{element[1]}}</ext-link>
              </nav-pointer>
            {% endfor%}
          </nav-pointer-group>
      </index-entry> 
    {% endfor %}   
    </index>
</book-part-wrapper>
'''


# In[ ]:


data = {
    "author_reference_dict" : auth_dict_custom_sorted
}


# In[ ]:


t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)


# In[ ]:


with open(output_path + "Register_1_sortiert.xml", 'w', encoding='utf8') as file:
    file.write(bits)

