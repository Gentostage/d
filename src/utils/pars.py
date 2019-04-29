from bs4 import BeautifulSoup
import os
import csv

def read_file(filename):
    with open(filename,  encoding='utf-8') as input_file:
        text = input_file.read()
    return text

def parse_user_datafile_bs(filename):
    results = []
    text = read_file(filename)
    soup = BeautifulSoup(text, 'html.parser')
    
    film_list = soup.find('div', {'id': 'content'})

    items = film_list.find_all('div', {'class': ['views-row']})
    
    for item in items:
        print('item')

        quest = item.find('div', {'class': 'views-field-field-faq-ext'})
        if quest:
            quest=quest.find('div', {'class': 'field-content'}).text
        else:
            quest='NULL'

        answer = item.find('div', {'class': 'views-field-field-faqanswer'}).find_all('p')
        textanswer = ''
        for i in answer:
            textanswer =textanswer + i.text

        results.append({
                'quest': quest,
                'answer':textanswer,
            })


    return results

results = []
for filename in os.listdir('./user_data/'):
    print(filename)
    results.extend(parse_user_datafile_bs('./user_data/'+filename))

print(len(results))

listdata=[]
for tmp in results:
    templist =[]

    tmpa=tmp['quest']
    tmpq=tmp['answer']

    tmpa=tmpa.replace(u'Здравствуйте! ', u'')
    tmpq=tmpq.replace(u'Здравствуйте! ', u'') 

    tmpa=tmpa.replace(u'Здравствуйте. ', u'')
    tmpq=tmpq.replace(u'Здравствуйте. ', u'') 
    
    tmpa=tmpa.replace(u'Добрый день. ', u'')
    tmpq=tmpq.replace(u'Добрый день. ', u'')

    tmpa=tmpa.replace(u'Добрый день! ', u'')
    tmpq=tmpq.replace(u'Добрый день! ', u'')
    
    tmpa=tmpa.replace(u'"', u"'")
    tmpq=tmpq.replace(u'"', u"'")

    tmpa=tmpa.replace(u'\n', u' ')
    tmpq=tmpq.replace(u'\n', u' ')

    templist.append(tmpa.replace(u'\xa0', u' '))
    templist.append(tmpq.replace(u'\xa0', u' '))
    if (tmp['answer']==''):
        continue
    listdata.append(templist)
    
with open('dataset.csv', 'w+', encoding="utf-8", newline='') as fp:
    writer = csv.writer(fp, delimiter=',')
    writer.writerow(["Question", "Answer"])  # Записать заголовок
    writer.writerows(listdata) 
