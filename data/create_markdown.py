import queries #all the functions i just made to get the info
import os
import datetime
import re
#get master_list
master_list = queries.extract_data()
bib_database = queries.parse('slr.bib')
queries.extract_bibfile(bib_database, master_list)

def delete_all(): # for when you make so many mistakes with the naming
    file_path = "../_posts/"
    pattern = re.compile(r"2025-04-01-25-.*\.markdown")

    for filename in os.listdir(file_path):
        if pattern.fullmatch(filename):
            full_path = os.path.join(file_path, filename)
            os.remove(full_path)
            print(f"Deleted: {full_path}")

        
#iteratre though every name in master_list


# #for article in master_list:
delete_all()

languages_all = set()
tasks_all = set()
models_all = set()
representations_all = set()

for title, info in master_list.items():
   
    file_path = "../_posts/" 
    with open(f"{file_path}2025-01-01-25-{title.replace(' ', '')}.markdown", 'w') as f:

        f.write("---\n")
        #layout
       # values = master_list[title]
        
        #_, values = master_list.items()
        f.write("layout: post\n")
        f.write(f"title : '{title.strip()}'\n")
        f.write("date: 2025-01-01 10:03:19 -0500\n")
        
        #for loop to get all of the tags.
        tags = []
        #
    # for i in values:
        languages = info['language']
        tasks = info['task']
        models = info['model']
        representations = info['representation']

        if languages:
            for val in languages:
                if val != 'not specified':
                    tags.append(val.replace(" (final)", "")) # removes the final from each value
                    languages_all.add(val)
        if tasks:
            for val in tasks:
                if val != 'not specified':
                    tags.append(val.replace(" (final)", ""))
                    tasks_all.add(val)
        if models:
            for val in models:
                if val != 'not specified':
                    tags.append(val.replace(" (final)", ""))
                    models_all.add(val)

        if representations:
            for val in representations:
                if val != 'not specified':
                    tags.append(val.replace(" (final)", ""))
                    representations_all.add(val)


        
        f.write(f"tags: {tags}\n") # unpack the list
        f.write("---\n")
        #article name
        
        f.write(f"Paper: [{title}]({info['url'][0]})\n\n")

        f.write(f"Author: {info['author']}\n\n")

        f.write('\n\n\n')
        f.write('')
        f.write('')
        f.write(""" Tags:  
        <span>{% for tag in page.tags %}<a href="/tags/#{{ tag | slugify }}">{{ tag }}</a>{% if forloop.last == false %}, {% endif %}{% endfor %}</span>\n""")

