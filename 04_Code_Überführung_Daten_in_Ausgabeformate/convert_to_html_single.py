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


# Pfad zum Ordner, in dem die mit diesem Script erstellten html-Datensätze abgelegt werden sollen
output_path = r"..."


# In[5]:


template ='''
<!DOCTYPE HTML>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>{{title}}:{{subtitle}}</title>
        <link rel="stylesheet" type="text/css" href="_galley.css" media="screen">
    </head>
    <body>
        <h1>
            <span class="label">{{sequential_number}}</span> 
            <span class="title">{{title}}</span>{% if subtitle == "" %}<span class="title-subtitle-sep"></span>{% elif subtitle.startswith(".") %}<span class="title-subtitle-sep"></span>{% else %}<span class="title-subtitle-sep">: </span>{% endif %}<span class="subtitle">{{subtitle}}</span>
        </h1>
        <div class="position-2">
          {% for item in footnotes_500 %}
            <p class="p-2-500">{{item}}</p>
          {% endfor %}
          {% for item in footnotes_700 %}
            <p class="p-2-700">{{item}}</p>
          {% endfor %}
          {% for item in footnotes_710 %}
            <p class="p-2-710">{{item}}</p>
          {% endfor %}
          {% for item in footnotes_730 %}
            <p class="p-2-730">{{item}}</p>
          {% endfor %}
        </div>
        <div class="position-3">
            <p class="p-3-main">{{p_3_main}}</p>
          {% for item in p_3_footnotes_500 %}
            <p class="p-3-500">{{item}}</p>
          {% endfor %}
          {% for item in p_3_footnotes_700 %}
            <p class="p-3-700">{{item}}</p>
          {% endfor %}
          {% for item in p_3_footnotes_710 %}
            <p class="p-3-710">{{item}}</p>
          {% endfor %}
          {% for item in p_3_footnotes_730 %}
            <p class="p-3-730">{{item}}</p>
          {% endfor %}
        </div> 
        <div class="position-4">
            <p class="p-4-main">{{p_4_main}}</p>
          {% for item in p_4_footnotes_500 %}
            <p class="p-4-500">{{item}}</p>
          {% endfor %}
          {% for item in p_4_footnotes_700 %}
            <p class="p-4-700">{{item}}</p>
          {% endfor %}
          {% for item in p_4_footnotes_710 %}
            <p class="p-4-710">{{item}}</p>
          {% endfor %}
          {% for item in p_4_footnotes_730 %}
            <p class="p-4-730">{{item}}</p>
          {% endfor %}
        </div>
        <p class="position-5">{{links_cats}}</p>
        <p class="position-6">{{block}}</p>
        <p class="position-7">{{cover}}</p>
        <p class="position-8">{{p_8_1}}</p>
        <p class="position-9">{{binding_information}}</p>
        <p class="position-10">{{provenience}}</p>
        <p class="position-11">{{links_swisscoll}}</p>
        {% if figures != {} %}
            <div class="figure-group">
                <div class="figure-row">
                {% for key, value in figures.items() %}
                  <figure>
                      <p><a target="_blank" href="https://uv-v4.netlify.app/#?manifest=https://iiif.ub.unibe.ch/presentation/v2.1/berner-inkunabeln/manifest/{{value[:-4]}}">
                         <img src="https://iiif.ub.unibe.ch/image/v3/berner-inkunabeln/{{value}}/full/,400/0/default.jpg"></a></p>
                      <div class=legend>
                          <label>Abbildung {{loop.index}}</label>
                          <p>{{key}}</p>
                      </div> 
                  </figure>
                {% endfor %}
                </div>
            </div>
        {% endif %}
        <div class="impressum-title">Die Inkunabeln in der Universitätsbibliothek Bern</div>
        <div class="impressum-author-publisher">Sabine Schlüter (ed.), BOP Books 2023</div>
        <div class="doi"><span class="ext-ref"><a href='{{doi}}' target=_blank>{{doi}}</a></span></div>
      </body>
</html>'''


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
        
        p_5_1_nolink = re.findall("<-L-5-START-><-L-5-STOP-><-VI-5-START->(.*?)<-VI-5-STOP->", p_5_1)
        for element in p_5_1_nolink:
            p_5_1 = p_5_1.replace(f"<-L-5-START-><-L-5-STOP-><-VI-5-START->{element}<-VI-5-STOP->", 
                                  f"<span class=\"ext-ref\">{element}</span>")
            
        p_5_1 = p_5_1.replace("<-L-5-START->", "<span class=\"ext-ref\"><a href='")
        p_5_1 = p_5_1.replace("<-L-5-STOP->", "' target=_blank")
        p_5_1 = p_5_1.replace("<-VI-5-START->", ">")
        p_5_1 = p_5_1.replace("<-VI-5-STOP->", "</a></span>")

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
        p_11_1 = p_11_1.replace("<-L-11-START->", "<span class=\"ext-ref\"><a href='")
        p_11_1 = p_11_1.replace("<-L-11-STOP->", "' target=_blank")
        p_11_1 = p_11_1.replace("<-VI-11-START->", ">")
        p_11_1 = p_11_1.replace("<-VI-11-STOP->", "</a></span>")
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

    with open(output_path + output_filename + ".html", 'w', encoding='utf8') as file:
        file.write(bits)


# ---
