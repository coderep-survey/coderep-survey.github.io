import sqlite3
from collections import defaultdict
# Connect to the SQLite database

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

def extract_bibfile(master_list):
    pass

master_list = extract_data()
extract_bibfile(master_list)

