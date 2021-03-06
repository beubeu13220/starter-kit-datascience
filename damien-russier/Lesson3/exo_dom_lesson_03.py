# -*- coding: utf-8 -*-
'''
Created on 6 oct. 2016

@author: utilisateur
'''


'''
L'exercice pour le cours prochain est le suivant: 
- Récupérer via crawling la liste des 256 top contributors sur cette page
https://gist.github.com/paulmillr/2657075 
- En utilisant l'API github https://developer.github.com/v3/
récupérer pour chacun de ces users le nombre moyens de stars des
repositories qui leur appartiennent. Pour finir classer ces 256
contributors par leur note moyenne.﻿
'''

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from pprint import pprint

import json
import os

def decode_row(row):
    rank = int(row.find("th").text.strip('#'))
    cells = row.find_all("td")
    loginname = cells[0].get_text()
    login = loginname.split('(')[0].strip()
    try:
        name = loginname.split('(')[1].split(')')[0].strip()
    except IndexError:
        name = None
    return login, name, rank
    

def get_users(maxnb=256):
    '''returns maxnb contributors'''
    url = 'https://gist.github.com/paulmillr/2657075'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.find("table").find("tbody").find_all("tr")
    users = {}
    count = 0
    for row in rows:
        count += 1
        if count > maxnb:
            break
        login, name, rank = decode_row(row)
        if login in users:
            print "problem"
        else:
            users[login] = {'name': name, 'rank': rank}
    return users

def get_users_avg3(users):
    '''github token + json'''
    # authentification
    token = os.environ.get('GITHUB_TOKEN')
    # print "token ", token
    auth_tuple = ('drussier', token)

    ranking = pd.DataFrame()
    for user in users:
        # list repositories for another user:
        url = "https://api.github.com/users/%s/repos" % (user)
        r = requests.get(url, auth=auth_tuple)
        # print r.json()

        avg = 0.
        count = 0
        data = r.json()
        # pprint(data)
        for d in data:
            note = d['stargazers_count']
            avg += note
            count += 1
        if count > 0:
            avg /= count
        else:
            avg = 0.
        ranking = ranking.append({'login': user,
                                  'note': avg},
                                 ignore_index=True)
    ranking = ranking.sort_values(['note'], ascending=False)
    ranking = ranking.reset_index(drop=True)
    ranking.to_csv('ranking3.csv', sep=',')
    return ranking


users = get_users()
# print users

ranking = get_users_avg3(users)



