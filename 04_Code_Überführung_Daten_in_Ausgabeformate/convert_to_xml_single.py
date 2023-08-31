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


# Pfad zum Ordner, in dem sich die nachbearbeiteten Inkunabeldatensätze befinden
data_path = r"..."


# In[4]:


# Pfad zum Ordner, in dem die mit diesem Script erstellten xml-Datensätze abgelegt werden sollen
output_path = r"..."


# In[5]:


template ='''<?xml version="1.0" encoding="UTF-8"?>
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
  <book-part seq="{{inc_nr}}">
      <book-part-meta>
        <book-part-id book-part-id-type="doi">{{doi}}</book-part-id>
        <title-group>
          <label>{{inc_nr}}</label>
            <title>{{title}}</title>
            <subtitle>{{subtitle}}</subtitle>
        </title-group>
        <custom-meta-group>
          <custom-meta>
            <meta-name>Network Zone MMS-ID</meta-name>
            <meta-value>{{mms_id}}</meta-value>
          </custom-meta>
        </custom-meta-group>
      </book-part-meta>
      <body>
        <sec>
          <boxed-text content-type="position-2">
          {% for item in footnotes_500 %}
            <p content-type="p-2-500">{{item}}</p>
          {% endfor %}
          {% for item in footnotes_700 %}
            <p content-type="p-2-700">{{item}}</p>
          {% endfor %}
          {% for item in footnotes_710 %}
            <p content-type="p-2-710">{{item}}</p>
          {% endfor %}
          {% for item in footnotes_730 %}
            <p content-type="p-2-730">{{item}}</p>
          {% endfor %}
          </boxed-text>
          <boxed-text content-type="position-3">
            <p content-type="p-3-main">{{p_3_main}}</p>
          {% for item in p_3_footnotes_500 %}
            <p content-type="p-3-500">{{item}}</p>
          {% endfor %}
          {% for item in p_3_footnotes_700 %}
            <p content-type="p-3-700">{{item}}</p>
          {% endfor %}
          {% for item in p_3_footnotes_710 %}
            <p content-type="p-3-710">{{item}}</p>
          {% endfor %}
          {% for item in p_3_footnotes_730 %}
            <p content-type="p-3-730">{{item}}</p>
          {% endfor %}
          </boxed-text> 
          <boxed-text content-type="position-4">
            <p content-type="p-4-main">{{p_4_main}}</p>
          {% for item in p_4_footnotes_500 %}
            <p content-type="p-4-500">{{item}}</p>
          {% endfor %}
          {% for item in p_4_footnotes_700 %}
            <p content-type="p-4-700">{{item}}</p>
          {% endfor %}
          {% for item in p_4_footnotes_710 %}
            <p content-type="p-4-710">{{item}}</p>
          {% endfor %}
          {% for item in p_4_footnotes_730 %}
            <p content-type="p-4-730">{{item}}</p>
          {% endfor %}
          </boxed-text> 
            <p content-type="position-5">{{links_cats}}</p>
            <p content-type="position-6">{{block}}</p>
            <p content-type="position-7">{{cover}}</p>
            <p content-type="position-8">{{p_8_1}}</p>
            <p content-type="position-9">{{binding_information}}</p>
            <p content-type="position-10">{{provenience}}</p>
            <p content-type="position-11">{{links_swisscoll}}</p>
        </sec>
      </body>
      <back>
        <app>
            {% if figures != {} %}
            <fig-group> <!-- angepasst gemäss Vorgabe Dennis vom 27.1.2023 -->
                {% for key, value in figures.items() %}
                  <fig> <!-- angepasst gemäss Vorgabe Mathias vom 28.3.2023 -->
                    <legend>
                      <label>Abbildung {{loop.index}}</label>
                      <p>{{key}}</p>
                    </legend> 
                        <graphic xlink:href="{{value}}" specific-use="preview"/>
                        <graphic xlink:href="https://iiif.ub.unibe.ch/presentation/v2.1/berner-inkunabeln/manifest/{{value[:-4]}}" specific-use="iiif-viewer"/>
                  </fig>
                {% endfor %}
            </fig-group>
            {% endif %}
        </app>
      </back>
    </book-part>
</book-part-wrapper>'''


# In[6]:


for item in os.listdir(data_path):

    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()

        s_1_1 = "<-1-1-START->\n"
        st_1_1 = "<-1-1-STOP->\n"

        s_1_2 = "<-1-2-START->\n"
        st_1_2 = "<-1-2-STOP->\n"

        s_2_1 = "<-2-1-START->\n"
        st_2_1 = "<-2-1-STOP->\n"

        s_3_1 = "<-3-1-START->\n"
        st_3_1 = "<-3-1-STOP->\n"

        s_4_1 = "<-4-1-START->\n"
        st_4_1 = "<-4-1-STOP->\n"

        s_5_1 = "<-5-1-START->\n"
        st_5_1 = "<-5-1-STOP->\n"

        s_6_1 = "<-6-1-START->\n"
        st_6_1 = "<-6-1-STOP->\n"

        s_7_1 = "<-7-1-START->\n"
        st_7_1 = "<-7-1-STOP->\n"

        s_8_1 = "<-8-1-START->\n"
        st_8_1 = "<-8-1-STOP->\n"

        s_9_1 = "<-9-1-START->\n"
        st_9_1 = "<-9-1-STOP->\n"

        s_10_1 = "<-10-1-START->\n"
        st_10_1 = "<-10-1-STOP->\n"

        s_11_1 = "<-11-1-START->\n"
        st_11_1 = "<-11-1-STOP->\n"

        s_12_1 = "<-12-1-START->\n"
        st_12_1 = "<-12-1-STOP->\n"

        s_b_l = "<-BILDINFORMATIONEN-START->\n"
        st_b_l = "<-BILDINFORMATIONEN-STOP->\n"
        
        s_reg = "<-REGISTER-REF-START->\n"
        st_reg = "<-REGISTER-REF-STOP->\n"

        start_1_1 = lines.find(s_1_1)
        stop_1_1 = lines.find(st_1_1)
        start_1_2 = lines.find(s_1_2)
        stop_1_2 = lines.find(st_1_2)
        start_2_1 = lines.find(s_2_1)
        stop_2_1 = lines.find(st_2_1)
        start_3_1 = lines.find(s_3_1)
        stop_3_1 = lines.find(st_3_1)
        start_4_1 = lines.find(s_4_1)
        stop_4_1 = lines.find(st_4_1)
        start_5_1 = lines.find(s_5_1)
        stop_5_1 = lines.find(st_5_1)
        start_6_1 = lines.find(s_6_1)
        stop_6_1 = lines.find(st_6_1)
        start_7_1 = lines.find(s_7_1)
        stop_7_1 = lines.find(st_7_1)
        start_8_1 = lines.find(s_8_1)
        stop_8_1 = lines.find(st_8_1)
        start_9_1 = lines.find(s_9_1)
        stop_9_1 = lines.find(st_9_1)
        start_10_1 = lines.find(s_10_1)
        stop_10_1 = lines.find(st_10_1)
        start_11_1 = lines.find(s_11_1)
        stop_11_1 = lines.find(st_11_1)
        start_12_1 = lines.find(s_12_1)
        stop_12_1 = lines.find(st_12_1)

        start_bildinfo = lines.find(s_b_l)
        stop_bildinfo = lines.find(st_b_l)
        
        start_inc_ref = lines.find(s_reg)
        stop_inc_ref = lines.find(st_reg)
        
        p_1_1 = lines[start_1_1 + len(s_1_1) : stop_1_1]
        p_1_1 = p_1_1.replace("\n", "").replace("&", "&amp;").replace("<<", "").replace(">>", "")
        p_1_2 = lines[start_1_2 + len(s_1_2) : stop_1_2]
        p_1_2 = p_1_2.replace("\n", "").replace("&", "&amp;").replace("<<", "").replace(">>", "")
        p_2_1 = lines[start_2_1 + len(s_2_1) : stop_2_1]
        p_2_1 = p_2_1.replace("&", "&amp;").replace("<<", "").replace(">>", "")

        p_2_500 = re.findall("<-500-START->(.*?)<-500-STOP->", p_2_1)
        p_2_700 = re.findall("<-700-START->(.*?)<-700-STOP->", p_2_1)
        p_2_710 = re.findall("<-710-START->(.*?)<-710-STOP->", p_2_1)
        p_2_730 = re.findall("<-730-START->(.*?)<-730-STOP->", p_2_1)

        p_3_1 = lines[start_3_1 + len(s_3_1) : stop_3_1]
        p_3_1 = p_3_1.replace("\n", "").replace("&", "&amp;").replace("<<", "").replace(">>", "")
        if "-STOP->" in p_3_1:
            main = re.search("(.*?)<-", p_3_1)
            p_3_main = main.group(1)
        else:
            p_3_main = p_3_1
        p_3_500 = re.findall("<-500-START->(.*?)<-500-STOP->", p_3_1)
        p_3_700 = re.findall("<-700-START->(.*?)<-700-STOP->", p_3_1)
        p_3_710 = re.findall("<-710-START->(.*?)<-710-STOP->", p_3_1)
        p_3_730 = re.findall("<-730-START->(.*?)<-730-STOP->", p_3_1)

        p_4_1 = lines[start_4_1 + len(s_4_1) : stop_4_1]
        p_4_1 = p_4_1.replace("\n", "").replace("&", "&amp;").replace("<<", "").replace(">>", "")
        if "-STOP->" in p_4_1:
            main = re.search("(.*?)<-", p_4_1)
            p_4_main = main.group(1)
        else:
            p_4_main = p_4_1
        p_4_500 = re.findall("<-500-START->(.*?)<-500-STOP->", p_4_1)
        p_4_700 = re.findall("<-700-START->(.*?)<-700-STOP->", p_4_1)
        p_4_710 = re.findall("<-710-START->(.*?)<-710-STOP->", p_4_1)
        p_4_730 = re.findall("<-730-START->(.*?)<-730-STOP->", p_4_1)
    
        p_5_1 = lines[start_5_1 + len(s_5_1) : stop_5_1]
        p_5_1 = p_5_1.replace("\n", "").replace("&", "&amp;").replace("<<", "").replace(">>", "")
        p_5_1 = p_5_1.replace("<-L-5-START->", "<ext-link xlink:href='")
        p_5_1 = p_5_1.replace("<-L-5-STOP->", "'")
        p_5_1 = p_5_1.replace("<-VI-5-START->", " ext-link-type=\"url\">")
        p_5_1 = p_5_1.replace("<-VI-5-STOP->", "</ext-link>")
        p_6_1 = lines[start_6_1 + len(s_6_1) : stop_6_1]
        p_6_1 = p_6_1.replace("\n", "").replace("&", "&amp;").replace("<<", "").replace(">>", "")
        p_7_1 = lines[start_7_1 + len(s_7_1) : stop_7_1]
        p_7_1 = p_7_1.replace("\n", "").replace("&", "&amp;").replace("<<", "").replace(">>", "")
        p_8_1 = lines[start_8_1 + len(s_8_1) : stop_8_1]
        p_8_1 = p_8_1.replace("\n", "").replace("&", "&amp;").replace("<<", "").replace(">>", "")
        p_9_1 = lines[start_9_1 + len(s_9_1) : stop_9_1]
        p_9_1 = p_9_1.replace("\n", "").replace("&", "&amp;").replace("<<", "").replace(">>", "")
        p_10_1 = lines[start_10_1 + len(s_10_1) : stop_10_1]
        p_10_1 = p_10_1.replace("\n", "").replace("&", "&amp;").replace("<<", "").replace(">>", "")
        p_11_1 = lines[start_11_1 + len(s_11_1) : stop_11_1]
        p_11_1 = p_11_1.replace("\n", "").replace("&", "&amp;").replace("<<", "").replace(">>", "")
        p_11_1 = p_11_1.replace("<-L-11-START->", "<ext-link xlink:href='")
        p_11_1 = p_11_1.replace("<-L-11-STOP->", "'")
        p_11_1 = p_11_1.replace("<-VI-11-START->", " ext-link-type=\"url\">")
        p_11_1 = p_11_1.replace("<-VI-11-STOP->", "</ext-link>")
        p_12_1 = lines[start_12_1 + len(s_12_1) : stop_12_1]
        p_12_1 = p_12_1.replace("\n", "").replace("&", "&amp;").replace("<<", "").replace(">>", "")

        if (start_bildinfo >= 0) and (stop_bildinfo >= 0):
            image_legend = lines[start_bildinfo + len(s_b_l) : stop_bildinfo]
            image_legend = image_legend.replace("&", "&amp;").replace("<<", "").replace(">>", "")
            images = re.findall("<-BILD-START->(.*?)<-BILD-STOP->", image_legend)
            legends = re.findall("<-LEGENDE-START->(.*?)<-LEGENDE-STOP->", image_legend)
        else:
            image_legend = []
            images = []
            legends = []
            
        inc_refs = lines[start_inc_ref + len(s_reg) : stop_inc_ref]
        inc_number = re.findall("<-Nr-START->(.*?)<-Nr-STOP->", inc_refs)[0]
        inc_doi = re.findall("<-DOI-START->(.*?)<-DOI-STOP->", inc_refs)[0]

    figures = {}
    for index, element in enumerate(legends):
        try:
            figures.update({element: images[index]})
        except:
            pass

    data = {
        "title": p_1_1,
        "subtitle": p_1_2,
        "mms_id": p_12_1,
        "sequential_number": inc_number,
        "footnotes_500": p_2_500,
        "footnotes_700": p_2_700,
        "footnotes_710": p_2_710,
        "footnotes_730": p_2_730,
        "p_3_main": p_3_main,
        "p_3_footnotes_500" : p_3_500,
        "p_3_footnotes_700": p_3_700,
        "p_3_footnotes_710": p_3_710,
        "p_3_footnotes_730": p_3_730,
        "p_4_main": p_4_main,
        "p_4_footnotes_500" : p_4_500,
        "p_4_footnotes_700": p_4_700,
        "p_4_footnotes_710": p_4_710,
        "p_4_footnotes_730": p_4_730,
        "links_cats": p_5_1,
        "block": p_6_1,
        "cover": p_7_1,
        "p_8_1": p_8_1,
        "binding_information": p_9_1,
        "provenience": p_10_1,
        "links_swisscoll": p_11_1,
        "figures": figures,
        "inc_nr": inc_number,
        "doi": inc_doi
    }

    t = Template(template, trim_blocks=True, lstrip_blocks=True)
    bits = t.render(data)
    
    output_filename = item[:-4].replace("(","").replace(")","").replace("<<","").replace(">>","").replace(" ","_").replace("&","").replace("'", "")

    with open(output_path + output_filename + ".xml", 'w', encoding='utf8') as file:
        file.write(bits)


# ---

# In[ ]:




