#!/usr/bin/env python
# coding: utf-8

# In[1]:


from platform import python_version
import os

import jinja2
from jinja2 import Template
import regex as re


# In[2]:


print("Python version: " + python_version())
print("Jinja2 version: " + jinja2.__version__)
print("Regex version: " + re.__version__)


# In[3]:


# Pfad zum Ordner, in dem sich die Inkunabeldatensätze im xml-Format befinden
data_path = r"..."


# In[4]:


# Pfad zum Ordner, in dem das mit diesem Script erstellte, konkatenierte xml-File abgelegt werden soll
output_path = r"..."


# In[5]:


template ='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE book PUBLIC "-//NLM//DTD BITS Book Interchange DTD v2.1 20220202//EN" "BITS-book2-1.dtd">
<book dtd-version="2.1" xmlns:xlink="http://www.w3.org/1999/xlink"
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
    <isbn>ISBN</isbn>
    <publisher>
      <publisher-name>Bern Open Publishing</publisher-name>
      <publisher-loc>Bern</publisher-loc>
    </publisher>
    <edition>1</edition>
    <kwd-group>
      <kwd></kwd>
    </kwd-group>
  </book-meta>
  
  <front-matter>
    <preface>
      <book-part-meta>
        <title-group>
          <title>Einleitung</title>
        </title-group>
        <contrib-group>
          <contrib>
            <name>
              <surname>Schlüter</surname>
              <given-names>Sabine</given-names>
            </name>
          </contrib>
        </contrib-group>
      </book-part-meta>
      <named-book-part-body>
        <p>bla bla bla bla</p>
      </named-book-part-body>
    </preface>
  </front-matter>
  
  <book-body>
    <book-part>
        <book-part-meta>
            <title-group>
              <title>Inkunabeln</title>
            </title-group>
        </book-part-meta>
    <body>
{% for item in content %}
    {{item}}
{% endfor %}
    </body>
    </book-part>
    </book-body>

<book-back>
    
</book-back>
</book>'''


# In[6]:


filelist = []

for item in os.listdir(data_path):

    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()

    s_1_1 = "</book-meta>\n"
    st_1_1 = "</book-part>\n"

    start_1_1 = lines.find(s_1_1)
    stop_1_1 = lines.find(st_1_1)

    p_1_1 = lines[start_1_1 + len(s_1_1) : stop_1_1 + len(st_1_1)]
    
    filelist.append(p_1_1)
    
    data = {
        "content": filelist
    }

t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)


# In[7]:


output_filename = "xml_datasets_concat"

with open(output_path + output_filename + ".xml", 'w', encoding='utf8') as file:
    file.write(bits)


# In[ ]:




