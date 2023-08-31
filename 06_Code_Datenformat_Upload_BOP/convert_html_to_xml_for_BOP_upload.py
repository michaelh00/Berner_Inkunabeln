#!/usr/bin/env python
# coding: utf-8

# In[1]:


from platform import python_version
import os

import jinja2
from jinja2 import Template
import regex as re
import pybase64


# In[2]:


print("Python version: " + python_version())
print("Jinja2 version: " + jinja2.__version__)
print("Regex version: " + re.__version__)
print("Pybase64 version: " + pybase64.__version__)


# In[3]:


# Pfad zum Ordner, in dem sich die Inkunabeldatensätze im HTML-Ausgabeformat befinden
data_path = r"..."


# In[4]:


# Pfad zum Ordner, in dem die mit diesem Script erstellten xml-Datensätze 
# für den automatisierten Upload in BOP abgelegt werden sollen
output_path = r"..."


# In[5]:


template ='''<?xml version="1.0"?>
<monograph xmlns="http://pkp.sfu.ca" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" locale="en" date_submitted="2023-06-14" status="3" submission_progress="" current_publication_id="1" stage="production" work_type="1" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
  <id type="internal" advice="ignore">1</id>
  
   <!-- HTMLS -->
  {% for key, value in categories.items() %}
  <submission_file xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="{{value[0]}}" created_at="2023-06-15" date_created="" file_id="{{value[0]}}" stage="proof" updated_at="2023-06-15" viewable="true" direct_sales_price="0" genre="Chapter Manuscript" sales_type="openAccess" source_submission_file_id="1" uploader="ator" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
    <name locale="en">chapter{{value[0]}}.html</name>
    <file id="{{value[0]}}" filesize="1943" extension="html">
      <embed encoding="base64">{{value[8]}}</embed>
    </file>
  </submission_file>
  {% endfor %}
    
 <!-- Authors and Volume Editors -->
  <publication xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1" status="3" primary_contact_id="1" url_path="" seq="0" access_status="0" date_published="2023-06-15" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
    <id type="internal" advice="ignore">1</id>
    <title locale="en">Inkunabel Katalog</title>
    <abstract locale="en">&lt;p&gt;Inkunabeln&lt;/p&gt;</abstract>
    <copyrightHolder locale="en">TEST Press</copyrightHolder>
    <copyrightYear>2023</copyrightYear>
    <authors xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
      <author include_in_browse="true" user_group_ref="Author" seq="0" id="1">
        <givenname locale="en">Au</givenname>
        <familyname locale="en">Tor</familyname>
        <country>BY</country>
        <email>autor@mailinator.com</email>
      </author>
      <author include_in_browse="true" user_group_ref="Author" seq="0" id="2">
        <givenname locale="en">Au</givenname>
        <familyname locale="en">Tor 2</familyname>
        <country>BY</country>
        <email>autor2@mailinator.com</email>
      </author>
      <author include_in_browse="true" user_group_ref="Volume editor" seq="0" id="3">
        <givenname locale="en">Sabine</givenname>
        <familyname locale="en">Schl&#xFC;ter</familyname>
        <country>CH</country>
        <email>sb@mailinator.com</email>
      </author>
      <author include_in_browse="true" user_group_ref="Volume editor" seq="0" id="4">
        <givenname locale="en">Ulrike</givenname>
        <familyname locale="en">B&#xFC;rger</familyname>
        <country>CH</country>
        <email>ub@mailinator.com</email>
      </author>
    </authors>
    
    <!-- HTML Galleys -->
    
    {% for key, value in categories.items() %}   
    <publication_format xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" locale="" url_path="" approved="true" available="true" physical_format="false" entry_key="DA" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
      <id type="internal" advice="ignore">{{value[0]}}</id>
      <name locale="en">HTML</name>
      <seq>0</seq>
      <submission_file_ref id="{{value[0]}}"/>
    </publication_format>
    {% endfor %}

    <!-- Chapters -->

    <chapters xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
    {% for key, value in categories.items() %}
      <chapter seq="{{value[0]}}" id="{{value[0]}}">
        <id type="internal" advice="ignore">{{value[0]}}</id>
        <id type="doi" advice="update">{{value[7]}}</id>
        <title locale="en">{{value[0]}} {{value[1]}}{{value[2]}}</title>
        <abstract locale="en">&lt;p&gt;{{value[4]}}&lt;/p&gt;&#xD;
         &lt;p&gt;{{value[5]}}&lt;/p&gt;</abstract>
        <subtitle locale="en">{{value[3]}}</subtitle>
        <submission_file_ref id="{{value[0]}}"/>
      </chapter>
      {% endfor %} 
    </chapters>
  </publication>
</monograph>'''


# ---

# ### A (1 - 49)

# In[5]:


item_list = []
item_parameter_list = []

for item in os.listdir(data_path)[0:49]:

    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()
    
    number = re.findall("<span class=\"label\">(.*?)</span>", lines)
    title = re.findall("<span class=\"title\">(.*?)</span>", lines)
    subtitle = re.findall("<span class=\"subtitle\">(.*?)</span>", lines)
    separator = re.findall("<span class=\"title-subtitle-sep\">(.*?)</span>", lines)
    signatur = re.findall("<p class=\"position-11\">Signatur: <span class=\"ext-ref\"><a href='(.*?)' target=_blank>(.*?)</a></span></p>", lines)
    druck_ort = re.findall("<p class=\"p-3-main\">(.*?)</p>", lines)
    doi = re.findall("target=_blank>https://doi.org/(.*?)</a>", lines)

    
    item_label = number[0]                    
    item_title = title[0]                       
    item_separator = separator[0]
    item_subtitle = subtitle[0]
    item_signature_link = signatur[0][0]
    item_signature = signatur[0][1]
    item_druck_ort = druck_ort[0]
    item_doi = doi[0]
    
    s_1_1 = "<!DOCTYPE HTML>\n"
    st_1_1 = "</html>"
    start_1_1 = lines.find(s_1_1)
    stop_1_1 = lines.find(st_1_1)
    html_content_str = lines[start_1_1 : stop_1_1 + len(st_1_1)]
    html_content_b64 = pybase64.b64encode(bytes(html_content_str, "utf8"))
    html_content = html_content_b64.decode("utf-8") 
    
    
    item_list.append(item)
    item_parameter_list.append([item_label, item_title, item_separator, item_subtitle, item_druck_ort,                                 item_signature, item_signature_link, item_doi, html_content])
    
    
katlist_dict = {}
for index, item in enumerate(item_list):
    katlist_dict.update({item : item_parameter_list[index]})
    
data = {
    "categories" : katlist_dict,
}    

t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)

output_filename = "Ink_Kat_A"

with open(output_path + output_filename + ".xml", 'w', encoding='utf8') as file:
    file.write(bits)


# ### B (49 - 100)

# In[6]:


item_list = []
item_parameter_list = []

for item in os.listdir(data_path)[49:100]:

    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()
    
    number = re.findall("<span class=\"label\">(.*?)</span>", lines)
    title = re.findall("<span class=\"title\">(.*?)</span>", lines)
    subtitle = re.findall("<span class=\"subtitle\">(.*?)</span>", lines)
    separator = re.findall("<span class=\"title-subtitle-sep\">(.*?)</span>", lines)
    signatur = re.findall("<p class=\"position-11\">Signatur: <span class=\"ext-ref\"><a href='(.*?)' target=_blank>(.*?)</a></span></p>", lines)
    druck_ort = re.findall("<p class=\"p-3-main\">(.*?)</p>", lines)
    doi = re.findall("target=_blank>https://doi.org/(.*?)</a>", lines)
    
    item_label = number[0]                    
    item_title = title[0]                       
    item_separator = separator[0]
    item_subtitle = subtitle[0]
    item_signature_link = signatur[0][0]
    item_signature = signatur[0][1]
    item_druck_ort = druck_ort[0]
    item_doi = doi[0]
    
    s_1_1 = "<!DOCTYPE HTML>\n"
    st_1_1 = "</html>"
    start_1_1 = lines.find(s_1_1)
    stop_1_1 = lines.find(st_1_1)
    html_content_str = lines[start_1_1 : stop_1_1 + len(st_1_1)]
    html_content_b64 = pybase64.b64encode(bytes(html_content_str, "utf8"))
    html_content = html_content_b64.decode("utf-8") 
    
    
    item_list.append(item)
    item_parameter_list.append([item_label, item_title, item_separator, item_subtitle, item_druck_ort,                                 item_signature, item_signature_link, item_doi, html_content])
    
    
katlist_dict = {}
for index, item in enumerate(item_list):
    katlist_dict.update({item : item_parameter_list[index]})
    
data = {
    "categories" : katlist_dict,
}    

t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)

output_filename = "Ink_Kat_B"

with open(output_path + output_filename + ".xml", 'w', encoding='utf8') as file:
    file.write(bits)


# ### CDE (101 - 145)

# In[7]:


item_list = []
item_parameter_list = []

for item in os.listdir(data_path)[100:145]:

    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()
    
    number = re.findall("<span class=\"label\">(.*?)</span>", lines)
    title = re.findall("<span class=\"title\">(.*?)</span>", lines)
    subtitle = re.findall("<span class=\"subtitle\">(.*?)</span>", lines)
    separator = re.findall("<span class=\"title-subtitle-sep\">(.*?)</span>", lines)
    signatur = re.findall("<p class=\"position-11\">Signatur: <span class=\"ext-ref\"><a href='(.*?)' target=_blank>(.*?)</a></span></p>", lines)
    druck_ort = re.findall("<p class=\"p-3-main\">(.*?)</p>", lines)
    doi = re.findall("target=_blank>https://doi.org/(.*?)</a>", lines)
    
    item_label = number[0]                    
    item_title = title[0]                       
    item_separator = separator[0]
    item_subtitle = subtitle[0]
    item_signature_link = signatur[0][0]
    item_signature = signatur[0][1]
    item_druck_ort = druck_ort[0]
    item_doi = doi[0]
    
    s_1_1 = "<!DOCTYPE HTML>\n"
    st_1_1 = "</html>"
    start_1_1 = lines.find(s_1_1)
    stop_1_1 = lines.find(st_1_1)
    html_content_str = lines[start_1_1 : stop_1_1 + len(st_1_1)]
    html_content_b64 = pybase64.b64encode(bytes(html_content_str, "utf8"))
    html_content = html_content_b64.decode("utf-8") 
    
    
    item_list.append(item)
    item_parameter_list.append([item_label, item_title, item_separator, item_subtitle, item_druck_ort,                                 item_signature, item_signature_link, item_doi, html_content])
    
    
katlist_dict = {}
for index, item in enumerate(item_list):
    katlist_dict.update({item : item_parameter_list[index]})
    
data = {
    "categories" : katlist_dict,
}    

t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)

output_filename = "Ink_Kat_CDE"

with open(output_path + output_filename + ".xml", 'w', encoding='utf8') as file:
    file.write(bits)


# ### FGH (146 - 198)

# In[8]:


item_list = []
item_parameter_list = []

for item in os.listdir(data_path)[145:198]:

    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()
    
    number = re.findall("<span class=\"label\">(.*?)</span>", lines)
    title = re.findall("<span class=\"title\">(.*?)</span>", lines)
    subtitle = re.findall("<span class=\"subtitle\">(.*?)</span>", lines)
    separator = re.findall("<span class=\"title-subtitle-sep\">(.*?)</span>", lines)
    signatur = re.findall("<p class=\"position-11\">Signatur: <span class=\"ext-ref\"><a href='(.*?)' target=_blank>(.*?)</a></span></p>", lines)
    druck_ort = re.findall("<p class=\"p-3-main\">(.*?)</p>", lines)
    doi = re.findall("target=_blank>https://doi.org/(.*?)</a>", lines)
    
    item_label = number[0]                    
    item_title = title[0]                       
    item_separator = separator[0]
    item_subtitle = subtitle[0]
    item_signature_link = signatur[0][0]
    item_signature = signatur[0][1]
    item_druck_ort = druck_ort[0]
    item_doi = doi[0]
    
    s_1_1 = "<!DOCTYPE HTML>\n"
    st_1_1 = "</html>"
    start_1_1 = lines.find(s_1_1)
    stop_1_1 = lines.find(st_1_1)
    html_content_str = lines[start_1_1 : stop_1_1 + len(st_1_1)]
    html_content_b64 = pybase64.b64encode(bytes(html_content_str, "utf8"))
    html_content = html_content_b64.decode("utf-8") 
    
    
    item_list.append(item)
    item_parameter_list.append([item_label, item_title, item_separator, item_subtitle, item_druck_ort,                                 item_signature, item_signature_link, item_doi, html_content])
    
    
katlist_dict = {}
for index, item in enumerate(item_list):
    katlist_dict.update({item : item_parameter_list[index]})
    
data = {
    "categories" : katlist_dict,
}    

t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)

output_filename = "Ink_Kat_FGH"

with open(output_path + output_filename + ".xml", 'w', encoding='utf8') as file:
    file.write(bits)


# ### IJK (199 - 251)

# In[9]:


item_list = []
item_parameter_list = []

for item in os.listdir(data_path)[198:251]:

    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()
    
    number = re.findall("<span class=\"label\">(.*?)</span>", lines)
    title = re.findall("<span class=\"title\">(.*?)</span>", lines)
    subtitle = re.findall("<span class=\"subtitle\">(.*?)</span>", lines)
    separator = re.findall("<span class=\"title-subtitle-sep\">(.*?)</span>", lines)
    signatur = re.findall("<p class=\"position-11\">Signatur: <span class=\"ext-ref\"><a href='(.*?)' target=_blank>(.*?)</a></span></p>", lines)
    druck_ort = re.findall("<p class=\"p-3-main\">(.*?)</p>", lines)
    doi = re.findall("target=_blank>https://doi.org/(.*?)</a>", lines)
    
    item_label = number[0]                    
    item_title = title[0]                       
    item_separator = separator[0]
    item_subtitle = subtitle[0]
    item_signature_link = signatur[0][0]
    item_signature = signatur[0][1]
    item_druck_ort = druck_ort[0]
    item_doi = doi[0]
    
    s_1_1 = "<!DOCTYPE HTML>\n"
    st_1_1 = "</html>"
    start_1_1 = lines.find(s_1_1)
    stop_1_1 = lines.find(st_1_1)
    html_content_str = lines[start_1_1 : stop_1_1 + len(st_1_1)]
    html_content_b64 = pybase64.b64encode(bytes(html_content_str, "utf8"))
    html_content = html_content_b64.decode("utf-8") 
    
    
    item_list.append(item)
    item_parameter_list.append([item_label, item_title, item_separator, item_subtitle, item_druck_ort,                                 item_signature, item_signature_link, item_doi, html_content])
    
    
katlist_dict = {}
for index, item in enumerate(item_list):
    katlist_dict.update({item : item_parameter_list[index]})
    
data = {
    "categories" : katlist_dict,
}    

t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)

output_filename = "Ink_Kat_IJK"

with open(output_path + output_filename + ".xml", 'w', encoding='utf8') as file:
    file.write(bits)


# ### LMN (252 - 305)

# In[10]:


item_list = []
item_parameter_list = []

for item in os.listdir(data_path)[251:305]:

    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()
    
    number = re.findall("<span class=\"label\">(.*?)</span>", lines)
    title = re.findall("<span class=\"title\">(.*?)</span>", lines)
    subtitle = re.findall("<span class=\"subtitle\">(.*?)</span>", lines)
    separator = re.findall("<span class=\"title-subtitle-sep\">(.*?)</span>", lines)
    signatur = re.findall("<p class=\"position-11\">Signatur: <span class=\"ext-ref\"><a href='(.*?)' target=_blank>(.*?)</a></span></p>", lines)
    druck_ort = re.findall("<p class=\"p-3-main\">(.*?)</p>", lines)
    doi = re.findall("target=_blank>https://doi.org/(.*?)</a>", lines)
    
    item_label = number[0]                    
    item_title = title[0]                       
    item_separator = separator[0]
    item_subtitle = subtitle[0]
    item_signature_link = signatur[0][0]
    item_signature = signatur[0][1]
    item_druck_ort = druck_ort[0]
    item_doi = doi[0]
    
    s_1_1 = "<!DOCTYPE HTML>\n"
    st_1_1 = "</html>"
    start_1_1 = lines.find(s_1_1)
    stop_1_1 = lines.find(st_1_1)
    html_content_str = lines[start_1_1 : stop_1_1 + len(st_1_1)]
    html_content_b64 = pybase64.b64encode(bytes(html_content_str, "utf8"))
    html_content = html_content_b64.decode("utf-8") 
    
    
    item_list.append(item)
    item_parameter_list.append([item_label, item_title, item_separator, item_subtitle, item_druck_ort,                                 item_signature, item_signature_link, item_doi, html_content])
    
    
katlist_dict = {}
for index, item in enumerate(item_list):
    katlist_dict.update({item : item_parameter_list[index]})
    
data = {
    "categories" : katlist_dict,
}    

t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)

output_filename = "Ink_Kat_LMN"

with open(output_path + output_filename + ".xml", 'w', encoding='utf8') as file:
    file.write(bits)


# ### OP (306 - 357)

# In[11]:


item_list = []
item_parameter_list = []

for item in os.listdir(data_path)[305:357]:

    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()
    
    number = re.findall("<span class=\"label\">(.*?)</span>", lines)
    title = re.findall("<span class=\"title\">(.*?)</span>", lines)
    subtitle = re.findall("<span class=\"subtitle\">(.*?)</span>", lines)
    separator = re.findall("<span class=\"title-subtitle-sep\">(.*?)</span>", lines)
    signatur = re.findall("<p class=\"position-11\">Signatur: <span class=\"ext-ref\"><a href='(.*?)' target=_blank>(.*?)</a></span></p>", lines)
    druck_ort = re.findall("<p class=\"p-3-main\">(.*?)</p>", lines)
    doi = re.findall("target=_blank>https://doi.org/(.*?)</a>", lines)
    
    item_label = number[0]                    
    item_title = title[0]                       
    item_separator = separator[0]
    item_subtitle = subtitle[0]
    item_signature_link = signatur[0][0]
    item_signature = signatur[0][1]
    item_druck_ort = druck_ort[0]
    item_doi = doi[0]
    
    s_1_1 = "<!DOCTYPE HTML>\n"
    st_1_1 = "</html>"
    start_1_1 = lines.find(s_1_1)
    stop_1_1 = lines.find(st_1_1)
    html_content_str = lines[start_1_1 : stop_1_1 + len(st_1_1)]
    html_content_b64 = pybase64.b64encode(bytes(html_content_str, "utf8"))
    html_content = html_content_b64.decode("utf-8") 
    
    
    item_list.append(item)
    item_parameter_list.append([item_label, item_title, item_separator, item_subtitle, item_druck_ort,                                 item_signature, item_signature_link, item_doi, html_content])
    
    
katlist_dict = {}
for index, item in enumerate(item_list):
    katlist_dict.update({item : item_parameter_list[index]})
    
data = {
    "categories" : katlist_dict,
}    

t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)

output_filename = "Ink_Kat_OP"

with open(output_path + output_filename + ".xml", 'w', encoding='utf8') as file:
    file.write(bits)


# ### QRS (358 - 410)

# In[12]:


item_list = []
item_parameter_list = []

for item in os.listdir(data_path)[357:410]:

    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()
    
    number = re.findall("<span class=\"label\">(.*?)</span>", lines)
    title = re.findall("<span class=\"title\">(.*?)</span>", lines)
    subtitle = re.findall("<span class=\"subtitle\">(.*?)</span>", lines)
    separator = re.findall("<span class=\"title-subtitle-sep\">(.*?)</span>", lines)
    signatur = re.findall("<p class=\"position-11\">Signatur: <span class=\"ext-ref\"><a href='(.*?)' target=_blank>(.*?)</a></span></p>", lines)
    druck_ort = re.findall("<p class=\"p-3-main\">(.*?)</p>", lines)
    doi = re.findall("target=_blank>https://doi.org/(.*?)</a>", lines)
    
    item_label = number[0]                    
    item_title = title[0]                       
    item_separator = separator[0]
    item_subtitle = subtitle[0]
    item_signature_link = signatur[0][0]
    item_signature = signatur[0][1]
    item_druck_ort = druck_ort[0]
    item_doi = doi[0]
    
    s_1_1 = "<!DOCTYPE HTML>\n"
    st_1_1 = "</html>"
    start_1_1 = lines.find(s_1_1)
    stop_1_1 = lines.find(st_1_1)
    html_content_str = lines[start_1_1 : stop_1_1 + len(st_1_1)]
    html_content_b64 = pybase64.b64encode(bytes(html_content_str, "utf8"))
    html_content = html_content_b64.decode("utf-8") 
    
    
    item_list.append(item)
    item_parameter_list.append([item_label, item_title, item_separator, item_subtitle, item_druck_ort,                                 item_signature, item_signature_link, item_doi, html_content])
    
    
katlist_dict = {}
for index, item in enumerate(item_list):
    katlist_dict.update({item : item_parameter_list[index]})
    
data = {
    "categories" : katlist_dict,
}    

t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)

output_filename = "Ink_Kat_QRS"

with open(output_path + output_filename + ".xml", 'w', encoding='utf8') as file:
    file.write(bits)


# ### TUVWZ (411 - 461)

# In[13]:


item_list = []
item_parameter_list = []

for item in os.listdir(data_path)[410:]:

    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()
    
    number = re.findall("<span class=\"label\">(.*?)</span>", lines)
    title = re.findall("<span class=\"title\">(.*?)</span>", lines)
    subtitle = re.findall("<span class=\"subtitle\">(.*?)</span>", lines)
    separator = re.findall("<span class=\"title-subtitle-sep\">(.*?)</span>", lines)
    signatur = re.findall("<p class=\"position-11\">Signatur: <span class=\"ext-ref\"><a href='(.*?)' target=_blank>(.*?)</a></span></p>", lines)
    druck_ort = re.findall("<p class=\"p-3-main\">(.*?)</p>", lines)
    doi = re.findall("target=_blank>https://doi.org/(.*?)</a>", lines)
    
    item_label = number[0]                    
    item_title = title[0]                       
    item_separator = separator[0]
    item_subtitle = subtitle[0]
    item_signature_link = signatur[0][0]
    item_signature = signatur[0][1]
    item_druck_ort = druck_ort[0]
    item_doi = doi[0]
    
    s_1_1 = "<!DOCTYPE HTML>\n"
    st_1_1 = "</html>"
    start_1_1 = lines.find(s_1_1)
    stop_1_1 = lines.find(st_1_1)
    html_content_str = lines[start_1_1 : stop_1_1 + len(st_1_1)]
    html_content_b64 = pybase64.b64encode(bytes(html_content_str, "utf8"))
    html_content = html_content_b64.decode("utf-8") 
    
    
    item_list.append(item)
    item_parameter_list.append([item_label, item_title, item_separator, item_subtitle, item_druck_ort,                                 item_signature, item_signature_link, item_doi, html_content])
    
    
katlist_dict = {}
for index, item in enumerate(item_list):
    katlist_dict.update({item : item_parameter_list[index]})
    
data = {
    "categories" : katlist_dict,
}    

t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)

output_filename = "Ink_Kat_TUVWZ"

with open(output_path + output_filename + ".xml", 'w', encoding='utf8') as file:
    file.write(bits)


# ---

# ### ALL DATA

# In[14]:


item_list = []
item_parameter_list = []

for item in os.listdir(data_path):

    with open(data_path + item, "r", encoding='utf8') as file:
        lines = file.read()
    
    number = re.findall("<span class=\"label\">(.*?)</span>", lines)
    title = re.findall("<span class=\"title\">(.*?)</span>", lines)
    subtitle = re.findall("<span class=\"subtitle\">(.*?)</span>", lines)
    separator = re.findall("<span class=\"title-subtitle-sep\">(.*?)</span>", lines)
    signatur = re.findall("<p class=\"position-11\">Signatur: <span class=\"ext-ref\"><a href='(.*?)' target=_blank>(.*?)</a></span></p>", lines)
    druck_ort = re.findall("<p class=\"p-3-main\">(.*?)</p>", lines)
    doi = re.findall("target=_blank>https://doi.org/(.*?)</a>", lines)
    
    item_label = number[0]                    
    item_title = title[0]                       
    item_separator = separator[0]
    item_subtitle = subtitle[0]
    item_signature_link = signatur[0][0]
    item_signature = signatur[0][1]
    item_druck_ort = druck_ort[0]
    item_doi = doi[0]
    
    s_1_1 = "<!DOCTYPE HTML>\n"
    st_1_1 = "</html>"
    start_1_1 = lines.find(s_1_1)
    stop_1_1 = lines.find(st_1_1)
    html_content_str = lines[start_1_1 : stop_1_1 + len(st_1_1)]
    html_content_b64 = pybase64.b64encode(bytes(html_content_str, "utf8"))
    html_content = html_content_b64.decode("utf-8") 
    
    
    item_list.append(item)
    item_parameter_list.append([item_label, item_title, item_separator, item_subtitle, item_druck_ort,                                 item_signature, item_signature_link, item_doi, html_content])
    
    
katlist_dict = {}
for index, item in enumerate(item_list):
    katlist_dict.update({item : item_parameter_list[index]})
    
data = {
    "categories" : katlist_dict,
}    

t = Template(template, trim_blocks=True, lstrip_blocks=True)
bits = t.render(data)

output_filename = "Ink_Kat_ALL_DATA"

with open(output_path + output_filename + ".xml", 'w', encoding='utf8') as file:
    file.write(bits)


# In[ ]:




