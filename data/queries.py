import sqlite3
from collections import defaultdict
import bibtexparser
from bibtexparser.bparser import BibTexParser
import os
import re
# Connect to the SQLite database

import re

def latex_to_unicode(text):
    latex_replacements = {
        r"{\\'a}": "á", r"{\\'e}": "é", r"{\\'i}": "í", r"{\\'o}": "ó", r"{\\'u}": "ú",
        r"{\\`a}": "à", r"{\\`e}": "è", r"{\\`i}": "ì", r"{\\`o}": "ò", r"{\\`u}": "ù",
        r'{\\"a}': "ä", r'{\\"o}': "ö", r'{\\"u}': "ü",
        r'{\\H{o}}': "ő", r'{\\H{u}}': "ű",
        r"{\\'O}": "Ó", r"{\\H{O}}": "Ő",
        r"{\\'U}": "Ú", r"{\\H{U}}": "Ű",
        r"{\\c{c}}": "ç",
        r"{\\~n}": "ñ",
        r"\\textmu": "μ",
        r"\$\\mu\$": "μ",
        r"\$\\mu\$μ": "μ",  # handle special case in your manual patch
        r"{\{\\'n\}}": "ń",  # Doma{'{n}}ska
        r"{'\{n\}}": "ń",    # catch weird versions
        r"{'\{n}}": "ń",     # alternate malformed
            # existing mappings...
        r"{\\'n}": "ń",
        r"{\\'{n}}": "ń",  # optional catch
        r"{\\'{n}}": "ń",  # extra safety for nested ones
    }
    
    for latex, uni in latex_replacements.items():
        text = re.sub(latex, uni, text)
    return text
def normalize_text(text):
    return ' '.join(text.split())
def extract_data():
    conn = sqlite3.connect('db_survey_representations.sqlite3')

    # Create a cursor object
    cursor = conn.cursor()

    # query from last meeting
    query = 'select * from survey_representations_analysis \
    INNER join survey_representations_paper ON survey_representations_analysis.paper_id = survey_representations_paper.id \
    INNER JOIN  survey_representations_analysis_languages ON survey_representations_analysis_languages.analysis_id = survey_representations_analysis.id \
    INNER JOIN  survey_representations_language ON survey_representations_analysis_languages.language_id = survey_representations_language.id \
    WHERE user_id = 10;'

    cursor.execute(query) 

    results = cursor.fetchall()

    master_list = defaultdict(lambda: defaultdict(list))
    #ge
    for row in results:
        #add name 
        name = list(row)[6]

        #add lanuage
        language = list(row)[16]

        #add link
        link = list(row)[8]
       
        
        master_list[name]["language"].append(language)
        if not master_list[name]["url"]:
            master_list[name]["url"].append(link)
       # print(f"{name}, {language}, {link}")
        

    #query to find the cyberscurit tasks
    query = """SELECT * FROM survey_representations_analysis
    INNER JOIN survey_representations_paper 
        ON survey_representations_analysis.paper_id = survey_representations_paper.id
    INNER JOIN survey_representations_analysis_tasks 
        ON survey_representations_analysis_tasks.analysis_id = survey_representations_analysis.id
    INNER JOIN survey_representations_cybersecuritytask 
        ON survey_representations_analysis_tasks.cybersecuritytask_id = survey_representations_cybersecuritytask.id
    WHERE survey_representations_analysis.user_id = 10;
    """
    
    cursor.execute(query) 

    results = cursor.fetchall()
    for row in results:
        #add name 
        name = list(row)[6]
        task = list(row)[16]
        master_list[name]["task"].append(task)
        #print(f"{name}, {task}")

    
    #todo ml model
    query ="""select * from survey_representations_analysis 
    INNER join survey_representations_paper ON survey_representations_analysis.paper_id = survey_representations_paper.id
    INNER JOIN  survey_representations_analysis_ml_models ON survey_representations_analysis_ml_models.analysis_id = survey_representations_analysis.id
    INNER JOIN  survey_representations_machinelearningmodel ON survey_representations_analysis_ml_models.machinelearningmodel_id = survey_representations_machinelearningmodel.id
    WHERE user_id = 10;
    """
    cursor.execute(query) 

    results = cursor.fetchall()
    for row in results:
        #add name 
        name = list(row)[6]
        model = list(row)[16]
        master_list[name]["model"].append(model)
        #print(f"{name}, {model}")
    
    #todo representation
    query ="""select * from survey_representations_analysis 
    INNER join survey_representations_paper ON survey_representations_analysis.paper_id = survey_representations_paper.id
    INNER JOIN  survey_representations_analysis_representations ON survey_representations_analysis_representations.analysis_id = survey_representations_analysis.id
    INNER JOIN  survey_representations_representation ON survey_representations_analysis_representations.representation_id = survey_representations_representation.id
    WHERE user_id = 10;
    """
    cursor.execute(query) 

    results = cursor.fetchall()
    for row in results:
        #add name 
        name = list(row)[6]
        representation = list(row)[16]
        master_list[name]["representation"].append(representation)
        #print(f"{name}, {representation}")
    #print(master_list["Malware Classification Based on Graph Convolutional Neural Networks and Static Call Graph Features"])
    conn.close()
    print(len(master_list))
    return master_list 

def parse(filename):
    # Parse the uploaded .bib file
    parser = BibTexParser()
    parser.ignore_nonstandard_types = False  # <--- This is the key line
    with open(filename, 'r', encoding='utf-8') as bib_file:
        return bibtexparser.load(bib_file,parser=parser)
    
def extract_bibfile(bib_database, master_list):
    #each entry is a dictionary
    count = 0
 
    #gets every 
    for entry in bib_database.entries:
        count += 1
        title = normalize_text(entry['title'])
        for name in master_list:
            name = normalize_text(name)
            if title.lower() == name.lower():
                author = latex_to_unicode(entry['author'])
                print(author)
                year = entry['year']
                master_list[name]['author'] = author
                master_list[name]['year'] = year
                
    #had to manually input these since the names were slightly different in the database thanthe bibtext file
    master_list['VulRepair: A T5-Based Automated Software Vulnerability Repair']['author'] = 'Fu, M. and Tantithamthavorn, C. and Le, T. and Nguyen, V. and Phung, D.'
    master_list['GraphEye: A Novel Solution for Detecting Vulnerable Functions Based on Graph Attention Network [C]']['author'] = 'Zhou, L. and Huang, M. and Li, Y. and Nie, Y. and Li, J. and Liu, Y.'
    master_list['Using complexity coupling and cohesion metrics as early indicators of vulnerabilities']['author'] = 'I. Chowdhury and M. Zulkernine'
    master_list['$\mu$μVulDeePecker: A Deep Learning-Based System for Multiclass Vulnerability Detection']['author'] = 'Zou, D. and Wang, S. and Xu, S. and Li, Z. and Jin, H.'
    master_list['VulDeePecker: A deep learning-based system for multiclass vulnerability detection']['author'] = 'Zou, D. and Wang, S. and Xu, S. and Li, Z. and Jin, H.'

    #seems to be an extra corrupted name in the file so i delete it
    del master_list['$\mu$μVulDeePecker: A Deep Learning-Based System for Multiclass Vulnerability Detection']
    #Malware Classification Based on Graph Convolutional Neural Networks and Static Call Graph Features
        #publisher
        #author



#extracts data from the main sql database
if __name__ == '__main__':
    master_list = extract_data()

    #extracts data from the bibtext - author
    filename = 'slr.bib'
    bib_database = parse(filename)
    extract_bibfile(bib_database, master_list)


    #checking if everything is right:
    count = 0
    unauthored_articles = []
    for num, i in enumerate(master_list):
        # print(f'{num}: {master_list[i]["year"]}') 
        # print(f'{num}: {master_list[i]["author"]}')
        print(type(master_list[i]["year"]))
        # if master_list[i]["author"] == []:
        #     unauthored_articles.append(i)


    print(len(unauthored_articles))







