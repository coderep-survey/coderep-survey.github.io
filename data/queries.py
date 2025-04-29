import sqlite3
from collections import defaultdict
import bibtexparser
from bibtexparser.bparser import BibTexParser
import os
import re 
from pybtex.database.input import bibtex as pb
import requests
import time
# Connect to the SQLite database

import re

# function from prof santos

def doi_to_bibtex(doi: str) -> str:
    """
    Fetches the BibTeX entry for a given DOI using an online service.
    """
    url = f"https://doi.org/{doi}"
    headers = {'Accept': 'application/x-bibtex'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"An error occurred when retrieving BibTeX: {e}"
def doi_to_abstract(doi: str) -> str:
    """
    Attempts to retrieve an abstract using the CrossRef API and falls back to 
    BibTeX parsing if necessary.  Cleans up common HTML/XML tags from abstracts.
    """
    if not doi:
        return "No DOI provided."

    # --- Try CrossRef API First ---
    api_url = f"https://api.crossref.org/works/{doi}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        abstract = data.get('message', {}).get('abstract')
        if abstract:
            print(abstract)
            return ' '.join(abstract.split()).strip()
        else:
                # Optionally, parse the BibTeX to extract the abstract (simple string search)
                bibtex = doi_to_bibtex(doi)
                abstract_start = bibtex.find("abstract = {")
                if abstract_start != -1:
                    abstract_start += len("abstract = {")
                    abstract_end = bibtex.find("}", abstract_start)
                    abstract = bibtex[abstract_start:abstract_end]
                    print(abstract)
                    return abstract
                print("no abstract for this doi")
                return "No abstract available for this DOI."
    except requests.exceptions.RequestException as e:
        print("no abstract")
        return f"An error occurred when retrieving abstract: {e}"
        


def get_abstracts(master_list, bib_database):
    """
    Iterates through bib_database, finds matching titles in master_list,
    fetches abstracts using DOI, and adds the abstract directly to the master_list entry.
    """

    for entry in bib_database.entries:
        if 'title' not in entry:
            continue

        bib_title_normalized = ' '.join(entry['title'].split()).lower()
        doi = entry.get('doi')

        for name in list(master_list.keys()):
            master_name_normalized = ' '.join(name.split()).lower()

            if bib_title_normalized == master_name_normalized:
                if doi:
                    abstract = doi_to_abstract(doi)
                    master_list[name]['abstract'] = abstract
                    
                else:
                    master_list[name]['abstract'] = "No DOI found in BibTeX."
                break

    # Handle entries without abstracts after processing
    for name, data in master_list.items():
        if 'abstract' not in data:
            master_list[name]['abstract'] = "Title not matched in BibTeX."
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
               # print(author)
                year = entry['year']
                master_list[name]['author'] = author
                master_list[name]['year'] = year
                
    #had to manually input these since the names were slightly different in the database thanthe bibtext file
    master_list['VulRepair: A T5-Based Automated Software Vulnerability Repair']['author'] = 'Fu, M. and Tantithamthavorn, C. and Le, T. and Nguyen, V. and Phung, D.'
    master_list['GraphEye: A Novel Solution for Detecting Vulnerable Functions Based on Graph Attention Network [C]']['author'] = 'Zhou, L. and Huang, M. and Li, Y. and Nie, Y. and Li, J. and Liu, Y.'
    master_list['Using complexity coupling and cohesion metrics as early indicators of vulnerabilities']['author'] = 'I. Chowdhury and M. Zulkernine'
    master_list[r'$\mu$μVulDeePecker: A Deep Learning-Based System for Multiclass Vulnerability Detection']['author'] = 'Zou, D. and Wang, S. and Xu, S. and Li, Z. and Jin, H.'
    master_list['VulDeePecker: A deep learning-based system for multiclass vulnerability detection']['author'] = 'Zou, D. and Wang, S. and Xu, S. and Li, Z. and Jin, H.'

    #seems to be an extra corrupted name in the file so i delete it
    del master_list[r'$\mu$μVulDeePecker: A Deep Learning-Based System for Multiclass Vulnerability Detection']
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
    get_abstracts(master_list, bib_database)

    #checking if everything is right:
    count = 0
    unauthored_articles = []
    # for num, i in enumerate(master_list):
    #     # print(f'{num}: {master_list[i]["year"]}') 
    #     # print(f'{num}: {master_list[i]["author"]}')
    #     print(type(master_list[i]["year"]))
    #     # if master_list[i]["author"] == []:
    #     #     unauthored_articles.append(i)

    for title, data in master_list.items():
        # Safely get the abstract, providing a default message if the key is missing
        abstract = data.get('abstract', 'Abstract not found or key missing.')
        print(f"\nTitle: {title}")
        print(f"Abstract: {abstract}")
    print("\n--- End of Abstracts ---")
   # print(len(unauthored_articles))







