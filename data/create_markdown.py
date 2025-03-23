import queries #all the functions i just made to get the info


#get master_list
master_list = queries.extract_data()
bib_database = queries.parse('slr.bib')
queries.extract_bibfile(bib_database, master_list)

for num, i in enumerate(master_list):
        print(f'{num}: {master_list[i]["author"]}')