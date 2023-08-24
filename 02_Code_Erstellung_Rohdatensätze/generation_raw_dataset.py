#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from platform import python_version

import os
import regex as re


# In[ ]:


print("Python version: " + python_version())
print("regex version: " + re.__version__)


# In[ ]:


# Pfad zum Ordner, der die heruntergeladenen Inkunabel-Metadaten enthält (siehe Ordner "01_Code_Download_Metadaten_Inkunabeln")
data_path = r"..."


# In[ ]:


# Pfad zum Ordner, in welchem die mit diesem Script automatisiert erstellten Datensätze abgelegt werden sollen 
output_path = r"..."


# In[ ]:


for index, filename in enumerate(os.listdir(data_path)):
    
    pos_1_1 = []
    pos_1_2 = []
    pos_2_1 = []
    pos_3_1 = []
    pos_4_1 = []
    pos_5_1 = []
    pos_6_1 = []
    pos_7_1 = []
    pos_8_1 = []
    pos_9_1 = []
    pos_10_1 = []
    pos_11_1 = []
    
    author_dataset = []
    author_dataset_clean = []
    place_dataset = []
    printer_dataset = []
    place_dataset_clean = []
    printer_dataset_clean = []
    bookbinder_dataset = []
    bookbinder_dataset_clean = []
    
    owner_dataset = []
    owner_dataset_clean = []
    
    mms_id = None
    doi = None
    signatur = None
    nummer = None
    


    dictionary_fields = {
                         "001": [],
                         "008": [], 

                         "100_$a" : [],
                         "100_$b" : [],
                         "100_$c" : [],
                         "100_$abc" : [], 

                         "110_$a" : [],
                         "110_$b" : [],
                         "110_$g" : [],
                         "110_$agb" : [], 

                         "130_$a" : [],
                         "130_$g" : [],
                         "130_$p" : [],
                         "130_$agp" : [],

                         "240_$a" : [],

                         "264_$a" : [],
                         "264_$b" : [],
                         "264_$c" : [],

                         "264_$a_alle" : [],
                         "264_$b_alle" : [],

                         "300_$a" : [],
                         "300_$b" : [],
                         "300_$c" : [],

                         "500_$a" : [],

                         "510_$a" : [],
                         "510_$c" : [],
                         "510_$u" : [],

                         "510_$acu": [],

                         "563_$a" : [],

                         "590_$a" : [],

                         "700_$a" : [],
                         "700_$a_umgestellt" : [],
                         "700_$b" : [],
                         "700_$c" : [],
                         "700_$4" : [],
                         "700_$abc" : [],

                         "700_$a_nicht_umgestellt_bc" : [], 

                         "700X2_$a" : [],
                         "700X2_$b" : [],
                         "700X2_$c" : [],
                         "700X2_$t" : [],

                         "700X2_$abc" : [], 

                         "710_$a" : [],
                         "710_$b" : [],
                         "710_$g" : [],

                         "710_$4" : [],

                         "710_$agb" : [], 

                         "710X2_$a" : [],
                         "710X2_$b" : [],
                         "710X2_$g" : [],
                         "710X2_$t" : [],

                         "710X2_$agb" : [], 

                         "730_$a" : [],
                         "730_$g" : [],
                         "730_$p" : [],

                         "730_$agp" : [],

                         "751_$a" : [],

                         "852_$j" : [],
                         "852_$9" : [],
                         }

    def feldfilter (feld, unterfeld):
        m_feld_unterfeld = re.search("\|" + str(unterfeld) + " (.+?)  \|", line)
        if m_feld_unterfeld != None :
            f_feld_unterfeld = m_feld_unterfeld.group(1)
            dictionary_fields[str(feld) + "_$" + str(unterfeld)].append(f_feld_unterfeld)
        else:
            m_feld_unterfeld_2 = re.search("\|" + str(unterfeld) +" (.+?)$", line)
            if m_feld_unterfeld_2 != None :
                f_feld_unterfeld_2 = m_feld_unterfeld_2.group(1)
                dictionary_fields[str(feld) + "_$" + str(unterfeld)].append(f_feld_unterfeld_2)
            else:
                dictionary_fields[str(feld) + "_$" + str(unterfeld)].append('')

        for x in range (0, len(dictionary_fields[str(feld) + "_$" + str(unterfeld)])):
            if dictionary_fields[str(feld) + "_$" + str(unterfeld)][x].endswith(" "):
                dictionary_fields[str(feld) + "_$" + str(unterfeld)][x] = dictionary_fields[str(feld) + "_$" + str(unterfeld)][x].rstrip()

        return dictionary_fields 

    def feldfilter_mehrfach_7Y0_4(feld, unterfeld):
        m_feld_unterfelder = re.findall("\|" + str(unterfeld) + " (.+?) ", line)
        if m_feld_unterfelder != [] :
            dictionary_fields[str(feld) + "_$" + str(unterfeld)].append(m_feld_unterfelder)
        else:
            dictionary_fields[str(feld) + "_$" + str(unterfeld)].append([''])
        return dictionary_fields

    def feldfilter_mehrfach_264_ab(feld, unterfeld):

        gleiche_unterfelder = re.findall("\|" + str(unterfeld) + " (.+?)  ", line)

        gleiche_unterfelder_alle = re.findall("\|" + str(unterfeld) + " (.+?)", line)

        if gleiche_unterfelder_alle != [] :

            if len(gleiche_unterfelder_alle) > len(gleiche_unterfelder):

                index = line.rfind("|" + str(unterfeld))
                letztes_unterfeld = re.findall("\|" + str(unterfeld) + " (.+?) $", line[index:])
                gleiche_unterfelder.append(letztes_unterfeld[0])

            else:
                pass

            dictionary_fields[str(feld) + "_$" + str(unterfeld)].append(gleiche_unterfelder)  

        else:
            dictionary_fields[str(feld) + "_$" + str(unterfeld)].append([''])

        return dictionary_fields
    
    
    try:
        with open(data_path + filename, encoding="utf8") as ft:
            lines = ft.readlines()

        for line in lines:    
            if "001" in line[0:3]:
                dictionary_fields["001"].append(line[4:-1])
            if "008" in line[0:3]:
                dictionary_fields["008"].append(line[11:15])
            if "100" in line[0:3]:
                feldfilter (100, "a")
                feldfilter (100, "b")
                feldfilter (100, "c")
            if "110" in line[0:3]:
                feldfilter (110, "a")
                feldfilter (110, "b")
                feldfilter (110, "g")
            if "130" in line[0:3]:
                feldfilter (130, "a")
                feldfilter (130, "g")
                feldfilter (130, "p")
            if "240" in line[0:3]:
                feldfilter (240, "a")
            if "264" in line[0:3]:
                feldfilter_mehrfach_264_ab (264, "a")
                feldfilter_mehrfach_264_ab (264, "b")
                feldfilter (264, "c")
            if "300" in line[0:3]:
                feldfilter (300, "a")
                feldfilter (300, "b")
                feldfilter (300, "c")
            if "500" in line[0:3]:
                feldfilter (500, "a")
            if "510" in line[0:3]:
                feldfilter (510, "a")
                feldfilter (510, "c")
                feldfilter (510, "u")
            if "563" in line[0:3]:
                feldfilter (563, "a")
            if "590" in line[0:3]:
                feldfilter (590, "a")
            if "700" in line[0:3] and not "2" in line[6]:
                feldfilter (700, "a")
                feldfilter (700, "b")
                feldfilter (700, "c") 
                feldfilter_mehrfach_7Y0_4 (700, "4") 
            if "700" in line[0:3] and "2" in line[6]:
                feldfilter ("700X2", "a")
                feldfilter ("700X2", "b")
                feldfilter ("700X2", "c")
                feldfilter ("700X2", "t")
            if "710" in line[0:3] and not "2" in line[6]:
                feldfilter (710, "a")
                feldfilter (710, "b")
                feldfilter (710, "g")  
                feldfilter_mehrfach_7Y0_4 (710, "4")
            if "710" in line[0:3] and "2" in line[6]:
                feldfilter ("710X2", "a")
                feldfilter ("710X2", "b")
                feldfilter ("710X2", "g")
                feldfilter ("710X2", "t")
            if "730" in line[0:3]:
                feldfilter (730, "a")
                feldfilter (730, "g")
                feldfilter (730, "p") 
            if "751" in line[0:3]:
                feldfilter (751, "a")   
            if "852" in line[0:3]:
                feldfilter (852, "j")
                feldfilter (852, "9")

        if dictionary_fields["100_$a"] != []:
            for x in range(0, len(dictionary_fields["100_$a"])):
                if dictionary_fields["100_$b"][x] == "" and dictionary_fields["100_$c"][x] != "":
                    dictionary_fields["100_$abc"].append(str(dictionary_fields["100_$a"][x] + " " + dictionary_fields["100_$c"][x]))
                elif dictionary_fields["100_$c"][x] == "" and dictionary_fields["100_$b"][x] != "":
                    dictionary_fields["100_$abc"].append(str(dictionary_fields["100_$a"][x] + " " + dictionary_fields["100_$b"][x]))
                elif dictionary_fields["100_$b"][x] == "" and dictionary_fields["100_$c"][x] == "":
                    dictionary_fields["100_$abc"].append(str(dictionary_fields["100_$a"][x]))
                else:
                    dictionary_fields["100_$abc"].append(str(dictionary_fields["100_$a"][x] + " " + dictionary_fields["100_$b"][x] + " " + dictionary_fields["100_$c"][x]))

        if dictionary_fields["110_$a"] != []:
            for x in range(0, len(dictionary_fields["110_$a"])):
                if dictionary_fields["110_$g"][x] == "" and dictionary_fields["110_$b"][x] != "":
                    dictionary_fields["110_$agb"].append(str(dictionary_fields["110_$a"][x] + " " + dictionary_fields["110_$b"][x]))
                elif dictionary_fields["110_$b"][x] == "" and dictionary_fields["110_$g"][x] != "":
                    dictionary_fields["110_$agb"].append(str(dictionary_fields["110_$a"][x] + " " + dictionary_fields["110_$g"][x]))
                elif dictionary_fields["110_$b"][x] == "" and dictionary_fields["110_$g"][x] == "":
                    dictionary_fields["110_$agb"].append(str(dictionary_fields["110_$a"][x]))
                else:
                    dictionary_fields["110_$agb"].append(str(dictionary_fields["110_$a"][x] + " " + dictionary_fields["110_$g"][x] + " " + dictionary_fields["110_$b"][x]))

        # Zusammenführung der Felder 130_$a, 130_$g und 130_$p zu 130_$agp
        if dictionary_fields["130_$a"] != []:
            for x in range(0, len(dictionary_fields["130_$a"])):
                if dictionary_fields["130_$p"][x] == "" and dictionary_fields["130_$g"][x] != "":
                    dictionary_fields["130_$agp"].append(str(dictionary_fields["130_$a"][x] + ". " + dictionary_fields["130_$g"][x]))
                elif dictionary_fields["130_$g"][x] == "" and dictionary_fields["130_$p"][x] != "":
                    dictionary_fields["130_$agp"].append(str(dictionary_fields["130_$a"][x] + ". " + dictionary_fields["130_$p"][x]))
                elif dictionary_fields["130_$g"][x] == "" and dictionary_fields["130_$p"][x] == "":
                    dictionary_fields["130_$agp"].append(str(dictionary_fields["130_$a"][x]))
                else:
                    dictionary_fields["130_$agp"].append(str(dictionary_fields["130_$a"][x] + ". " + dictionary_fields["130_$g"][x] + ". " + dictionary_fields["130_$p"][x]))

        # Zusammenführung aller Felder 264_$a zu 264_$a_alle
        if dictionary_fields["264_$a"] != []:
            for x in range(0, len(dictionary_fields["264_$a"][0])):
                dictionary_fields["264_$a_alle"].append(str(dictionary_fields["264_$a"][0][x]))
                dictionary_fields["264_$a_alle"].append(" und ")

            del dictionary_fields["264_$a_alle"][-1]

            dictionary_fields["264_$a_alle"] = [" ".join(dictionary_fields["264_$a_alle"])]

        # Zusammenführung aller Felder 264_$b zu 264_$b_alle
        if dictionary_fields["264_$b"] != []:
            for x in range(0, len(dictionary_fields["264_$b"][0])):
                dictionary_fields["264_$b_alle"].append(str(dictionary_fields["264_$b"][0][x]))
                dictionary_fields["264_$b_alle"].append(" und ")

            del dictionary_fields["264_$b_alle"][-1]

            dictionary_fields["264_$b_alle"] = [" ".join(dictionary_fields["264_$b_alle"])]

        # Zusammenführung der Felder 510_$a, 510_$c und 510_$u zu 510_$acu
        # Mit Auszeichnung der Verlinkungen: 
        # VI: Verlinkter Inhalt
        # L: Link

        if dictionary_fields["510_$a"] != []:
            for x in range(0, len(dictionary_fields["510_$a"])):
                if dictionary_fields["510_$c"][x] == "" and dictionary_fields["510_$u"][x] != "":
                    dictionary_fields["510_$acu"].append(str("<-L-5-START->" + dictionary_fields["510_$u"][x] + "<-L-5-STOP->" +                                                             "<-VI-5-START->" + dictionary_fields["510_$a"][x] + "<-VI-5-STOP->"))

                elif dictionary_fields["510_$u"][x] == "" and dictionary_fields["510_$c"][x] != "":
                    dictionary_fields["510_$acu"].append(str("<-VI-5-START->" + dictionary_fields["510_$a"][x] +                                                             dictionary_fields["510_$c"][x] + "<-VI-5-STOP->")) 

                elif dictionary_fields["510_$c"][x] == "" and dictionary_fields["510_$u"][x] == "":
                    dictionary_fields["510_$acu"].append(str("<-VI-5-START->" + dictionary_fields["510_$a"][x] + "<-VI-5-STOP->"))

                else:
                    dictionary_fields["510_$acu"].append(str("<-L-5-START->" + dictionary_fields["510_$u"][x] + "<-L-5-STOP->" +                                                             "<-VI-5-START->" + dictionary_fields["510_$a"][x] + " " + dictionary_fields["510_$c"][x] + "<-VI-5-STOP->"))



        if dictionary_fields["700_$a"] != []:

            for x in range(0, len(dictionary_fields["700_$a"])):

                if "," in dictionary_fields["700_$a"][x]:

                    nachname = re.search("(.+?), ", dictionary_fields["700_$a"][x])
                    nachname_extract = nachname.group(1)

                    vorname = re.search(", (.+?)$", dictionary_fields["700_$a"][x])
                    vorname_extract = vorname.group(1)

                    dictionary_fields["700_$a_umgestellt"].append(str(vorname_extract + " " + nachname_extract))

                else:
                    dictionary_fields["700_$a_umgestellt"].append(dictionary_fields["700_$a"][x])

        # Zusammenführung der Felder 700_$a, 700_$b und 700_$c zu 700_$abc mit innerer Umstellung 700_$a
        if dictionary_fields["700_$a_umgestellt"] != []:
            for x in range(0, len(dictionary_fields["700_$a_umgestellt"])):
                if dictionary_fields["700_$b"][x] == "" and dictionary_fields["700_$c"][x] != "":
                    dictionary_fields["700_$abc"].append(str(dictionary_fields["700_$a_umgestellt"][x] + " " + dictionary_fields["700_$c"][x]))
                elif dictionary_fields["700_$c"][x] == "" and dictionary_fields["700_$b"][x] != "":
                    dictionary_fields["700_$abc"].append(str(dictionary_fields["700_$a_umgestellt"][x] + " " + dictionary_fields["700_$b"][x]))
                elif dictionary_fields["700_$b"][x] == "" and dictionary_fields["700_$c"][x] == "":
                    dictionary_fields["700_$abc"].append(str(dictionary_fields["700_$a_umgestellt"][x]))
                else:
                    dictionary_fields["700_$abc"].append(str(dictionary_fields["700_$a_umgestellt"][x] + " " + dictionary_fields["700_$b"][x] + " " + dictionary_fields["700_$c"][x]))   

        # Zusammenführung der Felder 700_$a, 700_$b und 700_$c zu 700_$abc ohne innere Umstellung 700_$a
        if dictionary_fields["700_$a"] != []:
            for x in range(0, len(dictionary_fields["700_$a"])):
                if dictionary_fields["700_$b"][x] == "" and dictionary_fields["700_$c"][x] != "":
                    dictionary_fields["700_$a_nicht_umgestellt_bc"].append(str(dictionary_fields["700_$a"][x] + " " + dictionary_fields["700_$c"][x]))
                elif dictionary_fields["700_$c"][x] == "" and dictionary_fields["700_$b"][x] != "":
                    dictionary_fields["700_$a_nicht_umgestellt_bc"].append(str(dictionary_fields["700_$a"][x] + " " + dictionary_fields["700_$b"][x]))
                elif dictionary_fields["700_$b"][x] == "" and dictionary_fields["700_$c"][x] == "":
                    dictionary_fields["700_$a_nicht_umgestellt_bc"].append(str(dictionary_fields["700_$a"][x]))
                else:
                    dictionary_fields["700_$a_nicht_umgestellt_bc"].append(str(dictionary_fields["700_$a"][x] + " " + dictionary_fields["700_$b"][x] + " " + dictionary_fields["700_$c"][x]))   

        # Zusammenführung der Felder 700X2_$a, 700X2_$b und 700X2_$c zu 700X2_$abc
        if dictionary_fields["700X2_$a"] != []:
            for x in range(0, len(dictionary_fields["700X2_$a"])):
                if dictionary_fields["700X2_$b"][x] == "" and dictionary_fields["700X2_$c"][x] != "":
                    dictionary_fields["700X2_$abc"].append(str(dictionary_fields["700X2_$a"][x] + " " + dictionary_fields["700X2_$c"][x]))
                elif dictionary_fields["700X2_$c"][x] == "" and dictionary_fields["700X2_$b"][x] != "":
                    dictionary_fields["700X2_$abc"].append(str(dictionary_fields["700X2_$a"][x] + " " + dictionary_fields["700X2_$b"][x]))
                elif dictionary_fields["700X2_$b"][x] == "" and dictionary_fields["700X2_$c"][x] == "":
                    dictionary_fields["700X2_$abc"].append(str(dictionary_fields["700X2_$a"][x]))
                else:
                    dictionary_fields["700X2_$abc"].append(str(dictionary_fields["700X2_$a"][x] + " " + dictionary_fields["700X2_$b"][x] + " " + dictionary_fields["700X2_$c"][x]))

        # Zusammenführung der Felder 710_$a, 710_$g und 710_$b zu 710_$agb
        if dictionary_fields["710_$a"] != []:
            for x in range(0, len(dictionary_fields["710_$a"])):
                if dictionary_fields["710_$g"][x] == "" and dictionary_fields["710_$b"][x] != "":
                    dictionary_fields["710_$agb"].append(str(dictionary_fields["710_$a"][x] + ", " + dictionary_fields["710_$b"][x])) # Anpassung mit ", " gemäss Meeting vom 9.8.2022
                elif dictionary_fields["710_$b"][x] == "" and dictionary_fields["710_$g"][x] != "":
                    dictionary_fields["710_$agb"].append(str(dictionary_fields["710_$a"][x] + ", " + dictionary_fields["710_$g"][x])) # Anpassung mit ", " gemäss Meeting vom 9.8.2022
                elif dictionary_fields["710_$g"][x] == "" and dictionary_fields["710_$b"][x] == "":
                    dictionary_fields["710_$agb"].append(str(dictionary_fields["710_$a"][x]))
                else:
                    dictionary_fields["710_$agb"].append(str(dictionary_fields["710_$a"][x] + ", " + dictionary_fields["710_$g"][x] + " " + dictionary_fields["710_$b"][x])) # Anpassung mit ", " gemäss Meeting vom 9.8.2022

        # Zusammenführung der Felder 710X2_$a, 710X2_$g und 700X2_$b zu 710X2_$agb
        if dictionary_fields["710X2_$a"] != []:
            for x in range(0, len(dictionary_fields["710X2_$a"])):
                if dictionary_fields["710X2_$g"][x] == "" and dictionary_fields["710X2_$b"][x] != "":
                    dictionary_fields["710X2_$agb"].append(str(dictionary_fields["710X2_$a"][x] + ", " + dictionary_fields["710X2_$b"][x])) # Anpassung mit ", " gemäss Meeting vom 9.8.2022
                elif dictionary_fields["710X2_$b"][x] == "" and dictionary_fields["710X2_$g"][x] != "":
                    dictionary_fields["710X2_$agb"].append(str(dictionary_fields["710X2_$a"][x] + ", " + dictionary_fields["710X2_$g"][x])) # Anpassung mit ", " gemäss Meeting vom 9.8.2022
                elif dictionary_fields["710X2_$g"][x] == "" and dictionary_fields["710X2_$b"][x] == "":
                    dictionary_fields["710X2_$agb"].append(str(dictionary_fields["710X2_$a"][x]))
                else:
                    dictionary_fields["710X2_$agb"].append(str(dictionary_fields["710X2_$a"][x] + ", " + dictionary_fields["710X2_$g"][x] + " " + dictionary_fields["710X2_$b"][x])) # Anpassung mit ", " gemäss Meeting vom 9.8.2022

        # Zusammenführung der Felder 730_$a, 730_$g und 730_$p zu 730_$agp
        if dictionary_fields["730_$a"] != []:
            for x in range(0, len(dictionary_fields["730_$a"])):
                if dictionary_fields["730_$p"][x] == "" and dictionary_fields["730_$g"][x] != "":
                    dictionary_fields["730_$agp"].append(str(dictionary_fields["730_$a"][x] + ". " + dictionary_fields["730_$g"][x]))
                elif dictionary_fields["730_$g"][x] == "" and dictionary_fields["730_$p"][x] != "":
                    dictionary_fields["730_$agp"].append(str(dictionary_fields["730_$a"][x] + ". " + dictionary_fields["730_$p"][x]))
                elif dictionary_fields["730_$g"][x] == "" and dictionary_fields["730_$p"][x] == "":
                    dictionary_fields["730_$agp"].append(str(dictionary_fields["730_$a"][x]))
                else:
                    dictionary_fields["730_$agp"].append(str(dictionary_fields["730_$a"][x] + ". " + dictionary_fields["730_$g"][x] + ". " + dictionary_fields["730_$p"][x]))

        if dictionary_fields["100_$a"] != []:

            for x in range(0, len(dictionary_fields["100_$a"])):

                if "<<" and ">>" in dictionary_fields["100_$a"][x]:
                    dictionary_fields["100_$a"][x] = dictionary_fields["100_$a"][x].replace("<<", "").replace(">>", "")
                else:
                    pass

        if dictionary_fields["100_$abc"] != []:

            for x in range(0, len(dictionary_fields["100_$abc"])):

                if "<<" and ">>" in dictionary_fields["100_$abc"][x]:
                    dictionary_fields["100_$abc"][x] = dictionary_fields["100_$abc"][x].replace("<<", "").replace(">>", "")
                else:
                    pass

        if dictionary_fields["700_$abc"] != []:

            for x in range(0, len(dictionary_fields["700_$abc"])):

                if "<<" and ">>" in dictionary_fields["700_$abc"][x]:
                    dictionary_fields["700_$abc"][x] = dictionary_fields["700_$abc"][x].replace("<<", "").replace(">>", "")
                else:
                    pass

        if dictionary_fields["700_$a_nicht_umgestellt_bc"] != []:

            for x in range(0, len(dictionary_fields["700_$a_nicht_umgestellt_bc"])):

                if "<<" and ">>" in dictionary_fields["700_$a_nicht_umgestellt_bc"][x]:
                    dictionary_fields["700_$a_nicht_umgestellt_bc"][x] = dictionary_fields["700_$a_nicht_umgestellt_bc"][x].replace("<<", "").replace(">>", "")
                else:
                    pass

        if dictionary_fields["700X2_$abc"] != []:

            for x in range(0, len(dictionary_fields["700X2_$abc"])):

                if "<<" and ">>" in dictionary_fields["700X2_$abc"][x]:
                    dictionary_fields["700X2_$abc"][x] = dictionary_fields["700X2_$abc"][x].replace("<<", "").replace(">>", "")
                else:
                    pass
                                
        for key, value in dictionary_fields.copy().items():
            if value == []:
                pass
            else:
                arbeitsliste = value.copy()
                if any(isinstance(el, list) for el in arbeitsliste):
                    arbeitsliste.sort(key=lambda x: x[0], reverse=True)
                else:
                    arbeitsliste.sort(key=len, reverse=True)
                for a in arbeitsliste:
                    if a == "" or a == [""]:
                        newvalue = []
                        dictionary_fields[key] = newvalue
                    else:
                        break

#####################################################################################################

        ### Datensatz Inkunabel

        def pos_4_to_11():

            pos_4_1 = []

            ### Schritt 1
            if dictionary_fields["300_$a"] != []:
                pos_4_1.append(dictionary_fields["300_$a"][0])
                
                ### Schritt 2
                if dictionary_fields["300_$b"] != []:
                    pos_4_1.append(": ")
                    pos_4_1.append(dictionary_fields["300_$b"][0])

                ### Schritt 3
                if dictionary_fields["300_$c"] != []:
                    pos_4_1.append("; ")
                    pos_4_1.append(dictionary_fields["300_$c"][0])

            else:
                pass ### weiter mit Position 5.1

            if pos_4_1 != []:
                pos_4_1.append("\n")

        ###############################################################################################    

            pos_5_1 = []

            ### Schritte 1, 2, 3, 4, 5, 6
            if dictionary_fields["510_$a"] != []:
                for x in range(0, len(dictionary_fields["510_$acu"])):
                    pos_5_1.append(dictionary_fields["510_$acu"][x])
                    pos_5_1.append("; ")
                del pos_5_1[-1]
            else:
                pass ### weiter mit Position 6.1

            if pos_5_1 != []:
                pos_5_1.append("\n")

        #################################################################################################

            pos_6_1 = []

            ### Schritt 1
            if dictionary_fields["590_$a"] != []:
                for x in range(0, len(dictionary_fields["590_$a"])):
                    if dictionary_fields["590_$a"][x].startswith("Buchblockbeschreibung:"):
                        inhalt = dictionary_fields["590_$a"][x].split("Buchblockbeschreibung: ", 1)[1]
                        pos_6_1.append(inhalt)
            else:
                pass ### weiter mit Position 7.1

            if pos_6_1 != []:
                pos_6_1.append("\n")

        ###################################################################################################    

            pos_7_1 = []

            ### Schritt 1
            if dictionary_fields["563_$a"] != []:
                for x in range(0, len(dictionary_fields["563_$a"])):
                    if dictionary_fields["563_$a"][x].startswith("Einbandbeschreibung:"):
                        inhalt = dictionary_fields["563_$a"][x].split("Einbandbeschreibung: ", 1)[1]
                        pos_7_1.append(inhalt)
            else:
                pass ### weiter mit Position 8.1

            if pos_7_1 != []:
                pos_7_1.append("\n")

        ######################################################################################################    

            pos_8_1 = []

            ### Schritte 1, 2, 3, 4, 5, 6, 7, 8
            if dictionary_fields["700_$abc"] != [] and dictionary_fields["700_$4"] != []:
                for x in range (0, len(dictionary_fields["700_$abc"])):
                    if (("fmo" in dictionary_fields["700_$4"][x]) or ("fmo " in dictionary_fields["700_$4"][x])                     or ("dnr" in dictionary_fields["700_$4"][x]) or ("dnr " in dictionary_fields["700_$4"][x])):
                        if pos_8_1 == []:
                            pos_8_1.append("Provenienz: ")            
                        else:
                            pos_8_1.append("; ")

                        pos_8_1.append(dictionary_fields["700_$abc"][x])

        ### Schritte 9, 10, 11, 12, 13, 14, 15
            if dictionary_fields["710_$agb"] != [] and dictionary_fields["710_$4"] != []:
                for x in range (0, len(dictionary_fields["710_$agb"])):
                    if (("fmo" in dictionary_fields["710_$4"][x]) or ("fmo " in dictionary_fields["710_$4"][x])                     or ("dnr" in dictionary_fields["710_$4"][x]) or ("dnr " in dictionary_fields["710_$4"][x])):
                        if pos_8_1 == []:
                            pos_8_1.append("Provenienz: ")            
                        else:
                            pos_8_1.append("; ")

                        pos_8_1.append(dictionary_fields["710_$agb"][x])

            else:
                pass ### weiter mit Position 9.1

            if pos_8_1 != []:
                pos_8_1.append("\n")

        ##############################################################################################################

            pos_9_1 = []

            ### Schritt 1
            if dictionary_fields["590_$a"] != []:
                for x in range(0, len(dictionary_fields["590_$a"])):
                    if dictionary_fields["590_$a"][x].startswith("Zusammengebunden"):
                        inhalt = dictionary_fields["590_$a"][x]
                        pos_9_1.append(inhalt)
            else:
                pass ### weiter mit Position 10.1

            if pos_9_1 != []:
                pos_9_1.append("\n")

        ################################################################################################################    

            pos_10_1 = []

            ### Schritt 1
            if dictionary_fields["590_$a"] != []:
                for x in range(0, len(dictionary_fields["590_$a"])):
                    if dictionary_fields["590_$a"][x].startswith("Unvollständig"):
                        inhalt = dictionary_fields["590_$a"][x]
                        pos_10_1.append(inhalt)
            else:
                pass ### weiter mit Position 11.1

            if pos_10_1 != []:
                pos_10_1.append("\n")

        #################################################################################################################    

            pos_11_1 = []
            # VI: Verlinkter Inhalt
            # L: Link

            ### Schritt 1 und 2
            if dictionary_fields["852_$j"] != [] and dictionary_fields["852_$9"] != []:
                pos_11_1.append("Signatur: ")
                pos_11_1.append("<-L-11-START->")
                pos_11_1.append("https://swisscollections.ch/Record/")
                inhalt = dictionary_fields["852_$9"][0].split("(41SLSP_UBE)", 1)[1]
                pos_11_1.append(inhalt)
                pos_11_1.append("<-L-11-STOP->")
                pos_11_1.append(str("<-VI-11-START->" + dictionary_fields["852_$j"][0] + "<-VI-11-STOP->"))

            if pos_11_1 != []:
                pos_11_1.append("\n")

            return pos_4_1, pos_5_1, pos_6_1, pos_7_1, pos_8_1, pos_9_1, pos_10_1, pos_11_1

        pos_4_to_11 = pos_4_to_11()

        def pos_3():

            pos_3_1 = []

            ### Schritt 1
            if dictionary_fields["264_$a_alle"] != [] and dictionary_fields["264_$b_alle"] != [] and dictionary_fields["264_$c"] != []                 and ("[" in dictionary_fields["264_$a_alle"][0][0] and "]" in dictionary_fields["264_$a_alle"][0][-1])                 and ("[" not in dictionary_fields["264_$a_alle"][0][1:-1])                 and ("[" in dictionary_fields["264_$b_alle"][0][0] and "]" in dictionary_fields["264_$b_alle"][0][-1])                 and ("[" not in dictionary_fields["264_$b_alle"][0][1:-1])                 and ("[" in dictionary_fields["264_$c"][0][0] and "]" in dictionary_fields["264_$c"][0][-1])                 and ("[" not in dictionary_fields["264_$c"][0][1:-1]):
                    pos_3_1.append(dictionary_fields["264_$a_alle"][0][0:-1] + ": "                                   + dictionary_fields["264_$b_alle"][0][1:-1] + ", "                                   + dictionary_fields["264_$c"][0][1:])
                    pos_3_1.append("\n")
                    # weiter mit Position 4.1: 
                    pos_4_to_11

            else:
                ### Schritt 2
                if (dictionary_fields["264_$a_alle"] != [])                 and ("[" in dictionary_fields["264_$a_alle"][0][0] and "]" in dictionary_fields["264_$a_alle"][0][-1])                 and ("[" not in dictionary_fields["264_$a_alle"][0][1:-1]):
                    pos_3_1.append(dictionary_fields["264_$a_alle"][0])
                    pos_3_1.append(": ")

                ### Schritte 3 und 4    
                elif (dictionary_fields["751_$a"] != []):
                    for x in range(0, len(dictionary_fields["751_$a"])):
                        pos_3_1.append(dictionary_fields["751_$a"][x])
                        pos_3_1.append(" oder ")

                    del pos_3_1[-1]
                    pos_3_1.append(": ")

                else:
                    pass

                ### Schritt 5
                if (dictionary_fields["264_$b_alle"] != [])                 and ("[" in dictionary_fields["264_$b_alle"][0][0] and "]" in dictionary_fields["264_$b_alle"][0][-1])                 and ("[" not in dictionary_fields["264_$b_alle"][0][1:-1]):
                    pos_3_1.append(dictionary_fields["264_$b_alle"][0])

                    ### weiter mit Schritt 35:
                    ### Schritt 35
                    if (dictionary_fields["264_$c"] != [])                     and (("[" in dictionary_fields["264_$c"][0][0] and "]" in dictionary_fields["264_$c"][0][-1])                     and ("[" not in dictionary_fields["264_$c"][0][1:-1]))                     or (dictionary_fields["264_$c"] != [] and dictionary_fields["264_$c"][0][-1].isdigit()):
                        pos_3_1.append(", ")
                        pos_3_1.append(dictionary_fields["264_$c"][0])

                    else:
                        if (dictionary_fields["264_$c"] != []):
                            index = dictionary_fields["264_$c"][0].rfind("[")
                            if index >= 0:
                                pos_3_1.append(", ")
                                pos_3_1.append(dictionary_fields["264_$c"][0][index+1:-1])
                            else:
                                pos_3_1.append(", ")
                                pos_3_1.append(dictionary_fields["264_$c"][0])
                        else:
                            pass

                    pos_3_1.append("\n")

                else:

                    ### Schritte 6, 7, 8, 9, 10, 11, 12, 13
                    if (dictionary_fields["700_$abc"] != [] and dictionary_fields["700_$4"] != [])                     and ("prt" in [item for sublist in dictionary_fields["700_$4"] for item in sublist])                     or ("prt " in [item for sublist in dictionary_fields["700_$4"] for item in sublist]):

                        for x in range (0, len(dictionary_fields["700_$abc"])):
                            if ("prt" in dictionary_fields["700_$4"][x]) or ("prt " in dictionary_fields["700_$4"][x]):
                                pos_3_1.append(dictionary_fields["700_$abc"][x])
                                pos_3_1.append(" oder ")
                        del pos_3_1[-1]

                    ### Schritte 14, 15, 16, 17, 18, 19, 20
                    if (dictionary_fields["710_$agb"] != [] and dictionary_fields["710_$4"] != [])                     and ("prt" in [item for sublist in dictionary_fields["710_$4"] for item in sublist])                     or ("prt " in [item for sublist in dictionary_fields["710_$4"] for item in sublist]):

                        for x in range (0, len(dictionary_fields["710_$agb"])):
                            if ("prt" in dictionary_fields["710_$4"][x]) or ("prt " in dictionary_fields["710_$4"][x]):
                                if pos_3_1[-1] == ": ":
                                    pos_3_1.append(dictionary_fields["710_$agb"][x])
                                else:
                                    pos_3_1.append(" oder ")
                                    pos_3_1.append(dictionary_fields["710_$agb"][x])       
                            else:
                                pass

                    ### Schritte 21, 22, 23, 24, 25, 26, 27, 28
                    if (dictionary_fields["700_$abc"] != [] and dictionary_fields["700_$4"] != [])                     and ("pbl" in [item for sublist in dictionary_fields["700_$4"] for item in sublist])                     or ("pbl " in [item for sublist in dictionary_fields["700_$4"] for item in sublist]):

                        pos_3_1.append(" für ")

                        for x in range (0, len(dictionary_fields["700_$abc"])):
                            if ("pbl" in dictionary_fields["700_$4"][x]) or ("pbl " in dictionary_fields["700_$4"][x]):
                                pos_3_1.append(dictionary_fields["700_$abc"][x])
                                pos_3_1.append(" und ")
                            else:
                                pass

                        del pos_3_1[-1] 

                    ### Schritte 29, 30, 31, 32, 33, 34
                    if (dictionary_fields["710_$agb"] != [] and dictionary_fields["710_$4"] != [])                     and ("pbl" in [item for sublist in dictionary_fields["710_$4"] for item in sublist])                     or ("pbl " in [item for sublist in dictionary_fields["710_$4"] for item in sublist]):

                        ### Fallunterscheidung, die es erlaubt, zu entscheiden, wann "für" und wann "und" einzusetzen ist. ###
                        if (dictionary_fields["700_$abc"] != [] and dictionary_fields["700_$4"] != [])                         and ("pbl" in [item for sublist in dictionary_fields["700_$4"] for item in sublist])                         or ("pbl " in [item for sublist in dictionary_fields["700_$4"] for item in sublist]):
                            pos_3_1.append(" und ")

                        else:
                            pos_3_1.append(" für ")
                        ###

                        for x in range (0, len(dictionary_fields["710_$agb"])):
                            if ("pbl" in dictionary_fields["710_$4"][x]) or ("pbl " in dictionary_fields["710_$4"][x]):
                                pos_3_1.append(dictionary_fields["710_$agb"][x])
                                pos_3_1.append(" und ")
                            else:
                                pass

                        del pos_3_1[-1] 

                    else:
                        pass

                    ### Schritt 35
                    if (dictionary_fields["264_$c"] != [])                     and (("[" in dictionary_fields["264_$c"][0][0] and "]" in dictionary_fields["264_$c"][0][-1])                     and ("[" not in dictionary_fields["264_$c"][0][1:-1]))                     or (dictionary_fields["264_$c"] != [] and dictionary_fields["264_$c"][0][-1].isdigit()):
                        pos_3_1.append(", ")
                        pos_3_1.append(dictionary_fields["264_$c"][0])

                    else:
                        if (dictionary_fields["264_$c"] != []):
                            index = dictionary_fields["264_$c"][0].rfind("[")
                            if index >= 0:
                                pos_3_1.append(", ")
                                pos_3_1.append(dictionary_fields["264_$c"][0][index+1:-1])
                            else:
                                pos_3_1.append(", ")
                                pos_3_1.append(dictionary_fields["264_$c"][0])
                        else:
                            pass

                    pos_3_1.append("\n")

            return pos_3_1

        pos_3 = pos_3()

        def pos_2():

            pos_2_1 = []

            ### Schritte 1 und 2
            if dictionary_fields["500_$a"] != []:
                for x in range (0, len(dictionary_fields["500_$a"])):
                    pos_2_1.append("<-500-START->")
                    pos_2_1.append(dictionary_fields["500_$a"][x])
                    pos_2_1.append("<-500-STOP->")
                    pos_2_1.append("\n")
            else:
                pass

            ### Schritte 3, 4, 5, 6, 7, 8, 9, 10
            if dictionary_fields["700X2_$abc"] != []:
                for x in range (0, len(dictionary_fields["700X2_$abc"])):
                    pos_2_1.append("<-700-START->")
                    pos_2_1.append(dictionary_fields["700X2_$abc"][x] + ": ")
                    if len(dictionary_fields["700X2_$t"]) > 0:
                           pos_2_1.append(dictionary_fields["700X2_$t"][x])
                    pos_2_1.append("<-700-STOP->")
                    pos_2_1.append("\n")
            else:
                pass

            ### Schritte 11, 12, 13, 14, 15, 16, 17, 18
            if dictionary_fields["710X2_$agb"] != []:
                for x in range (0, len(dictionary_fields["710X2_$agb"])):
                    pos_2_1.append("<-710-START->")
                    pos_2_1.append(dictionary_fields["710X2_$agb"][x] + ": ")
                    if len(dictionary_fields["710X2_$t"]) > 0:
                           pos_2_1.append(dictionary_fields["710X2_$t"][x])
                    pos_2_1.append("<-710-STOP->")
                    pos_2_1.append("\n")
            else:
                pass

            ### Schritte 19, 20, 21, 22  
            if dictionary_fields["730_$agp"] != []:
                for x in range (0, len(dictionary_fields["730_$agp"])):
                    pos_2_1.append("<-730-START->")
                    pos_2_1.append(dictionary_fields["730_$agp"][x])
                    pos_2_1.append("<-730-STOP->")
                    pos_2_1.append("\n")
            else:
                pass

            return pos_2_1

        pos_2 = pos_2()

        def position_1_2_fall_1():
        ### Schritte 1-5

            pos_1_2 = []
            # Schritt 1
            if dictionary_fields["240_$a"] != []:
                pos_1_2.append(dictionary_fields["240_$a"][0])
                pos_2 ### weiter mit Position 2.1

            # Schritte 2 und 3
            elif dictionary_fields["700X2_$t"] != []:
                for x in range (0, len(dictionary_fields["700X2_$t"])):
                    if dictionary_fields["100_$a"] != [] and (dictionary_fields["700X2_$a"][x] == dictionary_fields["100_$a"][0]): ### zurück für 700X2_$a
                        pos_1_2.append(dictionary_fields["700X2_$t"][x])
                        pos_1_2.append("; ")
                    else:
                        pos_2 ### weiter mit Position 2.1

                if pos_1_2 != []:
                    del pos_1_2[-1]

            # Schritte 4 und 5
            elif dictionary_fields["710X2_$t"] != []:
                for x in range (0, len(dictionary_fields["710X2_$t"])):
                    if dictionary_fields["110_$a"] != [] and dictionary_fields["710X2_$a"][x] == dictionary_fields["110_$a"][0]:
                        pos_1_2.append(dictionary_fields["710X2_$t"][x])
                        pos_1_2.append("; ")
                    else:
                        pos_2 ### weiter mit Position 2.1
                if pos_1_2 != []:
                    del pos_1_2[-1]

            else:
                pos_2 ### weiter mit Position 2.1

            return pos_1_2

        pos_1_2_fall_1 = position_1_2_fall_1()

        def pos_1_2_steps_10_23(pos_1_2): 

        ### Schritt 10ff        
            helperlist = []
            for x in range (1, len(dictionary_fields["700X2_$abc"])):

                # Schritte 10, 11, 12  
                if dictionary_fields["700X2_$abc"][x] not in helperlist:                 
                    pos_1_2.append(". — " + dictionary_fields["700X2_$abc"][x] + ": ") 

                    #Schritte 13 und 14
                    for y in range (0, len(dictionary_fields["700X2_$t"])):
                        if dictionary_fields["700X2_$abc"][y] == dictionary_fields["700X2_$abc"][x]:
                            pos_1_2.append(dictionary_fields["700X2_$t"][y])
                            pos_1_2.append("; ")

                    if pos_1_2 != []:
                        del pos_1_2[-1]   

                else:
                    pass ### gehe zu schritt 15

                helperlist.append(dictionary_fields["700X2_$abc"][x])


            ### Schritt 15 ff    
            helperlist_2 = []
            for x in range (0, len(dictionary_fields["710X2_$agb"])):
                                                                    
                # Schritt 15, 16, 17  
                if dictionary_fields["710X2_$agb"][x] not in helperlist_2:
                    pos_1_2.append(". — " + dictionary_fields["710X2_$agb"][x] + ": ")

                    #Schritte 18 und 19
                    for y in range (0, len(dictionary_fields["710X2_$t"])):
                        if dictionary_fields["710X2_$agb"][y] == dictionary_fields["710X2_$agb"][x]:
                            pos_1_2.append(dictionary_fields["710X2_$t"][y])
                            pos_1_2.append("; ")

                    if pos_1_2 != []:
                        del pos_1_2[-1]

                else:
                    pass ### gehe zu schritt 20

                helperlist_2.append(dictionary_fields["710X2_$agb"][x])


            # Schritte 20, 21, 22, 23
            for x in range (0, len(dictionary_fields['730_$agp'])):
                if (pos_1_1 != [] and dictionary_fields['730_$agp'][x] != pos_1_1[0]):
                    pos_1_2.append(". — ")
                    pos_1_2.append(dictionary_fields['730_$agp'][x])

                else:
                    pass ### gehe zu 2.1

            return pos_1_2

        def position_1_2_fall_2():
        ### Schritte 6-23
            pos_1_2 = []

            if dictionary_fields['700X2_$a'] != []:
                # Schritte 6, 7
                # Schritt 6
                if dictionary_fields["700X2_$t"] != []:
                    pos_1_2.append(dictionary_fields["700X2_$t"][0])
                    #Schritt 7
                    if len(dictionary_fields["700X2_$t"]) > 1:
                        for x in range (1, len(dictionary_fields["700X2_$t"])):
                            if dictionary_fields["700X2_$abc"][x] == dictionary_fields["700X2_$abc"][0]:
                                pos_1_2.append("; " + dictionary_fields["700X2_$t"][x])
                            else:
                                pass ### gehe zu schritt 10
                    else:
                        pass ### gehe zu schritt 10

                ### Schritte 10 - 23
                pos_1_2_steps_10_23(pos_1_2)


            # Schritte 8, 9:
            # Schritt 8
            elif dictionary_fields["710X2_$t"] != []:
                pos_1_2.append(dictionary_fields["710X2_$t"][0])
                # Schritt 9
                if len(dictionary_fields["710X2_$t"]) > 1:
                    for x in range (1, len(dictionary_fields["710X2_$t"])):
                        if dictionary_fields["710X2_$a"][x] == dictionary_fields["710X2_$a"][0]:
                            pos_1_2.append("; " + dictionary_fields["710X2_$t"][x])
                        else:
                            pass ### gehe zu schritt 10
                else:
                    pass ### gehe zu schritt 10

                pos_1_2_steps_10_23(pos_1_2)

            else:
                pos_1_2_steps_10_23(pos_1_2) ### gehe zu schritt 10

            return pos_1_2

        pos_1_1 = []

        # Schritte 1 und 2
        if dictionary_fields['130_$a'] != []:
            pos_1_1.append(dictionary_fields['130_$agp'][0])

            ### Position 1.2. bleibt leer
            pos_1_2 = []

        #########################################################################    

        # Schritte 3, 4, 5
        # Schritt 3
        elif dictionary_fields['100_$a'] != []:
            pos_1_1.append(dictionary_fields['100_$a'][0])
             # Schritt 4
            if dictionary_fields['100_$b'] != []: 
                pos_1_1.append(" " + dictionary_fields['100_$b'][0]) 
            else:
                pass
            # Schritt 5
            if dictionary_fields['100_$c'] != []: 
                pos_1_1.append(" " + dictionary_fields['100_$c'][0])
            else:
                pass

            ### weiter mit position 1.2 Schritte 1-5 (Fall 1)
            pos_1_2 = pos_1_2_fall_1


        #########################################################################

        # Schritte 6, 7, 8
        # Schritt 6
        elif dictionary_fields['110_$a'] != []:
            pos_1_1.append(dictionary_fields['110_$a'][0])
            # Schritt 7
            if dictionary_fields['110_$g'] != []:
                pos_1_1.append(" " + dictionary_fields['110_$g'][0])
            else:
                pass
            # Schritt 8
            if dictionary_fields['110_$b'] != []: 
                pos_1_1.append(" " + dictionary_fields['110_$b'][0]) 
            else:
                pass

            ### weiter mit position 1.2 Schritte 1-5 (Fall 1)
            pos_1_2 = pos_1_2_fall_1


        ####################################################################################################################

        # Schritte 9, 10, 11
        # Schritt 9
        elif dictionary_fields['700X2_$a'] != []:
            pos_1_1.append(dictionary_fields['700X2_$a'][0])
            # Schritt 10
            if dictionary_fields['700X2_$b'] != [] and dictionary_fields['700X2_$b'][0] != "":
                pos_1_1.append(" " + dictionary_fields['700X2_$b'][0])
            else:
                pass
            # Schritt 11
            if dictionary_fields['700X2_$c'] != [] and dictionary_fields['700X2_$c'][0] != "":
                pos_1_1.append(" " + dictionary_fields['700X2_$c'][0])
            else:
                pass

            ### weiter mit position 1.2 Schritte 6-... (Fall 2)
            pos_1_2 = position_1_2_fall_2()

        ##########################################################################        

        # Schritte 12, 13, 14
        # Schritt 12
        elif dictionary_fields['710X2_$a'] != []:
            pos_1_1.append(dictionary_fields['710X2_$a'][0])
            # Schritt 13
            if dictionary_fields['710X2_$g'] != [] and dictionary_fields['710X2_$g'][0] != "":
                pos_1_1.append(" " + dictionary_fields['710X2_$g'][0])
            else:
                pass
            # Schritt 14
            if dictionary_fields['710X2_$b'] != [] and dictionary_fields['710X2_$b'][0] != "": 
                pos_1_1.append(" " + dictionary_fields['710X2_$b'][0])
            else:
                pos_1_2 = position_1_2_fall_2()
        ###########################################################################

        # Schritt 15
        elif dictionary_fields['730_$a'] != []:
            pos_1_1.append(dictionary_fields['730_$agp'][0])
            pos_1_2 = position_1_2_fall_2()

        pos_1_1.append("\n")
        if pos_1_2 != []:
            pos_1_2.append("\n")
            
        ###########################################################################

        ### Register 1

        author_dataset = []

        if dictionary_fields['100_$a'] != []:
            author_dataset.append(dictionary_fields['100_$abc'][0])
        else:
            author_dataset.append("No person")

        if dictionary_fields['110_$a'] != []:
            author_dataset.append(dictionary_fields['110_$agb'][0])
        else:
            author_dataset.append("No person")

        if dictionary_fields["700_$a_nicht_umgestellt_bc"] != [] and dictionary_fields["700_$4"] != []:
            for x in range (0, len(dictionary_fields["700_$abc"])):
                if ("aft" in dictionary_fields["700_$4"][x] or "ato" in dictionary_fields["700_$4"][x]                     or "aut" in dictionary_fields["700_$4"][x] or "com" in dictionary_fields["700_$4"][x]                     or "ctb" in dictionary_fields["700_$4"][x] or "edt" in dictionary_fields["700_$4"][x]                     or "enj" in dictionary_fields["700_$4"][x] or "hnr" in dictionary_fields["700_$4"][x]                     or "ill" in dictionary_fields["700_$4"][x] or "pat" in dictionary_fields["700_$4"][x]                     or "prm" in dictionary_fields["700_$4"][x] or "trl" in dictionary_fields["700_$4"][x]                     or "wac" in dictionary_fields["700_$4"][x] or "wpr" in dictionary_fields["700_$4"][x]                     or "wst" in dictionary_fields["700_$4"][x]):

                    author_dataset.append(dictionary_fields["700_$a_nicht_umgestellt_bc"][x])
                else:
                    author_dataset.append("No person")

        if dictionary_fields["710_$agb"] != [] and dictionary_fields["710_$4"] != []:
            for x in range (0, len(dictionary_fields["710_$agb"])):
                if ("aft" in dictionary_fields["710_$4"][x] or "ato" in dictionary_fields["710_$4"][x]                     or "aut" in dictionary_fields["710_$4"][x] or "com" in dictionary_fields["710_$4"][x]                     or "ctb" in dictionary_fields["710_$4"][x] or "edt" in dictionary_fields["710_$4"][x]                     or "enj" in dictionary_fields["710_$4"][x] or "hnr" in dictionary_fields["710_$4"][x]                     or "ill" in dictionary_fields["710_$4"][x] or "pat" in dictionary_fields["710_$4"][x]                     or "prm" in dictionary_fields["710_$4"][x] or "trl" in dictionary_fields["710_$4"][x]                     or "wac" in dictionary_fields["710_$4"][x] or "wpr" in dictionary_fields["710_$4"][x]                     or "wst" in dictionary_fields["710_$4"][x]):

                    author_dataset.append(dictionary_fields["710_$agb"][x])
                else:
                    author_dataset.append("No person")

        if dictionary_fields["700X2_$abc"] != []: 
            for x in range (0, len(dictionary_fields["700X2_$abc"])):
                author_dataset.append(dictionary_fields["700X2_$abc"][x])

        if dictionary_fields["710X2_$agb"] != []: 
            for x in range (0, len(dictionary_fields["710X2_$agb"])):
                author_dataset.append(dictionary_fields["710X2_$agb"][x])


        author_dataset_clean = []
        for item in author_dataset:
            if item not in author_dataset_clean:
                author_dataset_clean.append(item)
            else:
                pass
        if "No person" in author_dataset_clean:
            author_dataset_clean.remove("No person")

        #################################################################################
            
        ### Register 2
        place_dataset = []
        printer_dataset = []

        # Schritte 1 und 2
        if (dictionary_fields["751_$a"] != []):
            for x in range(0, len(dictionary_fields["751_$a"])):
                place_dataset.append(dictionary_fields["751_$a"][x])
        else:
            place_dataset.append("No place")


        # Schritte 3, 4, 5, 6, 7 und 8
        if dictionary_fields["700_$a_nicht_umgestellt_bc"] != [] and dictionary_fields["700_$4"] != []:
            for x in range (0, len(dictionary_fields["700_$a_nicht_umgestellt_bc"])):
                if ("prt" in dictionary_fields["700_$4"][x] or "pbl" in dictionary_fields["700_$4"][x] or                     "bsl" in dictionary_fields["700_$4"][x]):
                    printer_dataset.append(dictionary_fields["700_$a_nicht_umgestellt_bc"][x])
                else:
                    printer_dataset.append("No person")


        # Schritte 9, 10, 11, 12, 13 und 14
        if dictionary_fields["710_$agb"] != [] and dictionary_fields["710_$4"] != []:
            for x in range (0, len(dictionary_fields["710_$agb"])):
                if ("prt" in dictionary_fields["710_$4"][x] or "pbl" in dictionary_fields["710_$4"][x] or                     "bsl" in dictionary_fields["710_$4"][x]):
                    printer_dataset.append(dictionary_fields["710_$agb"][x])
                else:
                    printer_dataset.append("No person")

        place_dataset_clean = []
        for item in place_dataset:
            if item not in place_dataset_clean:
                place_dataset_clean.append(item)
            else:
                pass
        if "No place" in place_dataset_clean:
            place_dataset_clean.remove("No place")

        printer_dataset_clean = []
        for item in printer_dataset:
            if item not in printer_dataset_clean:
                printer_dataset_clean.append(item)
            else:
                pass
        if "No person" in printer_dataset_clean:
            printer_dataset_clean.remove("No person")
            
        ###############################################################################    

        ### Register 3

        bookbinder_dataset = []

        if dictionary_fields["700_$a_nicht_umgestellt_bc"] != [] and dictionary_fields["700_$4"] != []:
            for x in range (0, len(dictionary_fields["700_$a_nicht_umgestellt_bc"])):
                if ("bnd" in dictionary_fields["700_$4"][x]):
                    bookbinder_dataset.append(dictionary_fields["700_$a_nicht_umgestellt_bc"][x])
                else:
                    bookbinder_dataset.append("No bookbinder")


        if dictionary_fields["710_$agb"] != [] and dictionary_fields["710_$4"] != []:
            for x in range (0, len(dictionary_fields["710_$agb"])):
                if ("bnd" in dictionary_fields["710_$4"][x]):
                    bookbinder_dataset.append(dictionary_fields["710_$agb"][x])
                else:
                    bookbinder_dataset.append("No bookbinder")

        bookbinder_dataset_clean = []
        for item in bookbinder_dataset:
            if item not in bookbinder_dataset_clean:
                bookbinder_dataset_clean.append(item)
            else:
                pass
        if "No bookbinder" in bookbinder_dataset_clean:
            bookbinder_dataset_clean.remove("No bookbinder")

        ###################################################################################    
            
        ### Register 4

        owner_dataset = []

        if dictionary_fields["700_$a_nicht_umgestellt_bc"] != [] and dictionary_fields["700_$4"] != []:
            for x in range (0, len(dictionary_fields["700_$a_nicht_umgestellt_bc"])):
                if ("fmo" in dictionary_fields["700_$4"][x] or "dnr" in dictionary_fields["700_$4"][x]):
                    owner_dataset.append(dictionary_fields["700_$a_nicht_umgestellt_bc"][x])
                else:
                    owner_dataset.append("No owner")

        # Schritte 9, 10, 11, 12, 13 und 14
        if dictionary_fields["710_$agb"] != [] and dictionary_fields["710_$4"] != []:
            for x in range (0, len(dictionary_fields["710_$agb"])):
                if ("fmo" in dictionary_fields["710_$4"][x] or "dnr" in dictionary_fields["710_$4"][x]):
                    owner_dataset.append(dictionary_fields["710_$agb"][x])
                else:
                    owner_dataset.append("No owner")

        owner_dataset_clean = []
        for item in owner_dataset:
            if item not in owner_dataset_clean:
                owner_dataset_clean.append(item)
            else:
                pass
        if "No owner" in owner_dataset_clean:
            owner_dataset_clean.remove("No owner")
        
        #######################################################################################

        ### Register Referenzdaten

        mms_id = dictionary_fields["001"][0]
        doi = ["https://doi.org/10.36950/" + str(mms_id)]
        signatur = [dictionary_fields["852_$j"][0]]
        nummer = ["LAUFNUMMER"]

        def filename_generator():

            p_1 = pos_1_1.copy()
            p_1.remove("\n")
            p_1 = "".join(p_1)    
            author_raw = p_1.replace(",", "").replace(":", "")
            author = author_raw.split()

            if len(author) < 5:
                filename_first = "_".join(author)
            else:
                filename_first = author[0] + "_" + author[1] + "_" + author[2] + "_" + author[3]

            p_1_2 = pos_1_2.copy()
            if p_1_2 != []:
                p_1_2.remove("\n")
                filename_s = p_1_2[0].split()
                if len(filename_s) > 1:
                    filename_second = filename_s[0] + "_" + filename_s[1]
                else:
                    filename_second = filename_s[0]
            else:
                filename_second = ""
        
            year = []
            if (dictionary_fields["008"] != []):
                year.append(dictionary_fields["008"][0])
            else:
                year.append("")
        

            if filename_second != "":
                filename = filename_first + "_" + filename_second + "_" + year[0] + "_" + mms_id + ".txt"
            else:
                filename = filename_first + "_" + year[0] + "_" + mms_id + ".txt"
            
            if "<<" in filename:
                filename = filename.replace("<<", "")
            if ">>" in filename:
                filename = filename.replace(">>", "")
            
            if "\t" in filename:
                filename = filename.replace("\t", "")

            return filename

        filename_output = filename_generator()


        with open(output_path + filename_output, 'w', encoding="utf8") as f:

            f.write("<-1-1-START->\n")
            for item in pos_1_1: # pos_1_1
                f.write(item)
            f.write("<-1-1-STOP->\n")
            f.write("\n")

            f.write("<-1-2-START->\n")
            for item in pos_1_2: # pos_1_2
                f.write(item)
            f.write("<-1-2-STOP->\n")
            f.write("\n")

            f.write("<-2-1-START->\n")
            for item in pos_2: # pos_2_1
                f.write(item)
            f.write("<-2-1-STOP->\n")
            f.write("\n")

            f.write("<-3-1-START->\n")
            for item in pos_3: # pos_3_1
                f.write(item)
            f.write("<-3-1-STOP->\n")
            f.write("\n")

            f.write("<-4-1-START->\n")
            for item in pos_4_to_11[0]: # pos_4_1
                f.write(item)
            f.write("<-4-1-STOP->\n")
            f.write("\n")

            f.write("<-5-1-START->\n")    
            for item in pos_4_to_11[1]: # pos_5_1
                f.write(item)
            f.write("<-5-1-STOP->\n")
            f.write("\n")    

            f.write("<-6-1-START->\n")
            for item in pos_4_to_11[2]: # pos_6_1
                f.write(item)
            f.write("<-6-1-STOP->\n")
            f.write("\n")     

            f.write("<-7-1-START->\n")
            for item in pos_4_to_11[3]: # pos_7_1
                f.write(item)
            f.write("<-7-1-STOP->\n")
            f.write("\n")         

            f.write("<-8-1-START->\n")    
            for item in pos_4_to_11[4]: # pos_8_1
                f.write(item)
            f.write("<-8-1-STOP->\n")
            f.write("\n")   

            f.write("<-9-1-START->\n")     
            for item in pos_4_to_11[5]: # pos_9_1
                f.write(item)
            f.write("<-9-1-STOP->\n")
            f.write("\n")    

            f.write("<-10-1-START->\n")      
            for item in pos_4_to_11[6]: # pos_10_1
                f.write(item)
            f.write("<-10-1-STOP->\n")
            f.write("\n")     

            f.write("<-11-1-START->\n")
            for item in pos_4_to_11[7]: # pos_11_1
                f.write(item)
            f.write("<-11-1-STOP->\n")
            f.write("\n") 
            
            f.write("<-12-1-START->\n")
            for item in mms_id:
                f.write(item)
            f.write("\n")
            f.write("<-12-1-STOP->\n")
            f.write("\n") 

            f.write(2*"\n") 
            f.write("<-REGISTER-1-START->\n")
            for item in author_dataset_clean:
                f.write("<-P-START->")
                f.write(item)
                f.write("<-P-STOP->")
                f.write("\n") 
            f.write("<-REGISTER-1-STOP->\n")
            f.write("\n") 

            f.write("<-REGISTER-2-START->\n")
            for item in place_dataset_clean:
                f.write("<-O-START->")
                f.write(item)
                f.write("<-O-STOP->")
                f.write("\n")
            for item in printer_dataset_clean:
                f.write("<-P-START->")
                f.write(item)
                f.write("<-P-STOP->")
                f.write("\n") 
            f.write("<-REGISTER-2-STOP->\n")
            f.write("\n")

            f.write("<-REGISTER-3-START->\n")
            for item in bookbinder_dataset_clean:
                f.write("<-P-START->")
                f.write(item)
                f.write("<-P-STOP->")
                f.write("\n")
            f.write("<-REGISTER-3-STOP->\n")
            f.write("\n") 

            f.write("<-REGISTER-4-START->\n")
            for item in owner_dataset_clean:
                f.write("<-P-START->")
                f.write(item)
                f.write("<-P-STOP->")
                f.write("\n")
            f.write("<-REGISTER-4-STOP->\n")
            f.write("\n") 

            f.write(2*"\n")
            f.write("<-REGISTER-REF-START->\n")
            for item in doi:
                f.write("<-DOI-START->")
                f.write(item)
                f.write("<-DOI-STOP->")
                f.write("\n") 
            for item in signatur:
                f.write("<-SIGN-START->")
                f.write(item)
                f.write("<-SIGN-STOP->")
                f.write("\n") 
            for item in nummer:
                f.write("<-Nr-START->")
                f.write(item)
                f.write("<-Nr-STOP->")
                f.write("\n")
            f.write("<-REGISTER-REF-STOP->\n")
            f.write("\n") 

            f.write(2*"\n") 
            f.write("<-ORIGINAL-MARC-DATENSATZ-SWISSCOLLECTIONS-START->\n")
            for item in lines:
                f.write(item)
            f.write("<-ORIGINAL-MARC-DATENSATZ-SWISSCOLLECTIONS-STOP->\n")
            f.write("\n")
            
        print("Datensatz " + str(index) + " bearbeitet.")
            
            
    except Exception as e:
        print(e)


# ---

# In[ ]:




