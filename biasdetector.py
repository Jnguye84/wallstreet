import pandas as pd

dataset = pd.read_csv('fake.csv') #reading csv
keywords = ['cryptocurrency','financial','finance','finances', 'money', 'wealth', 'stocks']

#START data cleaning the fake.csv file

dataset = dataset.drop(dataset[dataset['type'] == 'conspiracy'].index) #got rid of conspiracy and bs articles
dataset = dataset.drop(dataset[dataset['type'] == 'bs'].index)
new_dataset = pd.DataFrame(columns = ['Text','Title'])
rowIndex = 0

#for each variable, we need to create a new list in order to add as the new column
text_col = []
title_col = []
author_col = []

for i in dataset['text']:
  for k in keywords: #if there is at least one k keyword in the article, then add it.
    if k in str(i):
      text_col.append(i)
      rowIndex = dataset.index[dataset['text']== i].tolist() #gets the index of the text column to then get the same title and author
      title_col.append(dataset['title'][rowIndex])
      author_col.append(dataset['author'][rowIndex])
      break #prevents duplicate articles from showing up

new_dataset['Text']=text_col
new_dataset['Title']= title_col
new_dataset['author']= author_col

dataset = new_dataset #I've now filtered out all the articles that don't include finance keywords
dataset.to_excel('fake_edited.xlsx')
#END data cleaning fake.csv file. All done!