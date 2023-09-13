#!/usr/bin/env python3

# wiki_city_scrapping.py

"""
Description: This script performs data scrapping tasks in wikipedia to extract summary data from Brazil states capitals
Author: Dante de Araújo Clementino
Date Created: September 14, 2023
Date Modified: September 14, 2023
Version: 1.0
Python Version: 3.11.5
Dependencies: pandas, requests, wikipedia, bs4
License: MIT License
"""

# Standard Library Imports
# Third Party Library Imports
import requests
import wikipedia
import pandas as pd
from bs4 import BeautifulSoup

# Local imports
# I've created some utilities functions to handle some string treatment
from utils import transform




if __name__ == "__main__":
    wikipedia.set_lang("pt")


    '''
    Querying "Lista de capitais do Brasil" and the page that i want is the third
    page of my query results, after that i get the page html and parse using
    BeautifulSoup so i can look for tbody and tha data that i want
    '''
    query = wikipedia.search("Lista de capitais do Brasil")
    page = wikipedia.WikipediaPage(query[2])
    html = page.html()
    parsed = BeautifulSoup(html,"html.parser")
    table = parsed.find("tbody")
    rows =  table.find_all("tr")
    capitals = []
    dicts = {}
    '''
    This for loops loops thru all "rows" in my table and
    gets the a tag href attribute and the text content of the
    second "row"
    '''
    for i in rows:
        row = i.find_all("td")
        try:
            capitals.append([row[1].a['href'],row[1].text,row[1].a['title']])
        except:
            print("No data in this line")

    for i in range(len(capitals)):
        try:
            capital = capitals[i][1]
            page_path = capitals[i][0]

            if capital == "Salvador[nota 1]":
                capital = capital.replace("[nota 1]","")

            page = requests.get("https://pt.wikipedia.org" + page_path)

            '''
            Here i got a best name for going directly to get the summary for
            a page and storing it in summary so i can add to my data dictionary
            later in the code
            '''
            summary = wikipedia.summary(capitals[i][2])

            capital_parsed = BeautifulSoup(page.text,"html.parser")

            '''
            For performance reasons i didn't opt for this approach
            page.html() takes a lot of time and query[0] doesn't always
            get a good result such as Natal being the Christmas Page
            instead o Natal City

            query = wikipedia.search(capital)
            page = wikipedia.WikipediaPage(query[0])
            capital_parsed = BeautifulSoup(page.html(),"html.parser")
            '''

            '''
            Here we look for a table that has a class attribute with
            infobox infobox_v2 that contais a lot of condensed
            information about the city, get the first one that
            we've encountered
            '''
            summary_table = capital_parsed.find_all("table", "infobox infobox_v2")
            summary_rows  =  summary_table[0].find_all("tr")

            data = {}
            data["Summary"] = summary

            '''
            In each row from 16 to the end we will get each column of
            data and inserting in a data dictionary that will have
            the key as the first column and the value as the second
            each column data will be transformed using a util function
            called transform in the end we store/copy this data
            dictionary inside a dictionary called dicts to create our
            future DataFrame
            '''
            for i in range(16,len(summary_rows)):
                columns = summary_rows[i].find_all("td")

                for x in range(len(columns)-1):
                    key = transform(columns[x].text)
                    value = transform(columns[x+1].text)
                    data[key] = value
            dicts[capital] = data.copy()
        except:
            print("No data in this line")

    '''
    Creating DataFrame using pandas, transposing and priting on console
    and saving to a comma separated value file
    '''
    dfCapitals = pd.DataFrame.from_dict(dicts).T
    print(dfCapitals)
    dfCapitals.to_csv("capitais.csv")
