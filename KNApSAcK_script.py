#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple script to perform general searches on KNApSAcK web database 
http://www.knapsackfamily.com/knapsack_core/top.php
by metabolite or organism. 
It creates a csv file with Name, CAS ID, KNApSAcK ID, and SMILES 
for each compound found by the user specified keyword. The file 
is saved to the current folder.

Created on Wed Jul 27 15:48:39 2022

@author: Dr. Freddy Bernal
"""
# Import essentials
import argparse
import requests 
from bs4 import BeautifulSoup 
import pandas as pd
import time
import sys

#####################
#  Argument parser  #
#####################

def arg_parser():
    script_usage = """{}""".format(sys.argv[0][2:])
    
    parser = argparse.ArgumentParser(usage=script_usage, description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('-st', 
                        dest='searchtype',
                        help='Type of search ("metabolite" or "organism").')
    parser.add_argument('-k', 
                        dest='keyword', 
                        help='Term to search for (e.g. "Bacillus").')
    args = parser.parse_args()
    
    return args    


################
#  MAIN CLASS  #
################

class KNApSAcKSearch():
    progress = 0

    def __init__(self, searchtype, keyword):
        # self.progress = 0
        self.base_url = 'http://www.knapsackfamily.com/knapsack_core/top.php'
        self.searchtype = searchtype
        self.keyword = keyword
        
        
    # Define function to get links for compounds resulting from search
    def get_cmpds(self, sname: str, word: str)-> list:
        """
        Retrieve list of compounds from user defined input by 
        scraping KNApSAcK database
    
        Parameters
        ----------
        sname : str
            type of search (either metabolite or organism).
        word : str
            keyword search (e.g. isoflavone, bacillus).
    
        Returns
        -------
        links : list
            links to compounds from search results.
    
        """
        
        # transform user input into url chunk
        search_val = f'/result.php?sname={sname}&word={word}'
        # Remove last part of base url and add user defined url
        # (taken from https://stackoverflow.com/questions/54961679/python-removing-the-last-part-of-an-url)
        search_url = self.base_url[:self.base_url.rfind('/')] + search_val
        
        # get html content of results page
        page = requests.get(search_url)
        # parse the content
        soup = BeautifulSoup(page.content, 'html.parser')
        # extract links (corresponding to compounds)
        links = []
        for element in soup.find_all('a', href=True):
            links.append(element['href'])
    
        return links


    # Define function to search for each indivual link and retrieve important information
    def retrieve_data(self, links: list)-> pd.DataFrame:
        """
        Search each link provided and retrieve basic compound information.
    
        Parameters
        ----------
        links : list
            url links resulting from customized search with get_cmpds.
    
        Returns
        -------
        res : pd.DataFrame
            Matrix with name(s), CAS ID, KNApSAcK ID and SMILES
            for all the compounds obtained by the search.
    
        """
        # Retrieve data from each link
        res = pd.DataFrame(columns=['names', 'cas', 'id', 'smiles'])
        for link in links[1:]:
            # define url
            url = self.base_url[:self.base_url.rfind('/')] + '/' + link
            # get html and parse the content
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            # filter to compounds' information
            data = soup.find_all('td', {'colspan': 4})
            # extract name(s), CAS ID, KNApSAcK ID, and SMILES
            names = list(data[0].stripped_strings)
            cas = data[3].text
            dbid = data[4].text.split()[0]
            smi = data[7].text
            
            # Store to dataframe   
            res.loc[len(res)] = [names, cas, dbid, smi]
            KNApSAcKSearch.progress += 1
            spinner = self.spinning_cursor()
            for _ in range(12):
                sys.stdout.write(next(spinner))
                sys.stdout.flush()
                time.sleep(0.1)
                sys.stdout.write('\b')
            
            
        KNApSAcKSearch.progress = -1
            
        return res



    # Define execution function
    def execute(self):
        """
        Creates global variables for user input entries and 
        run search
    
        Returns
        -------
        None.
    
        """
        
        # Search for compounds using user input
        links = self.get_cmpds(self.searchtype, self.keyword)
        if len(links) > 1: 
            print('Successfull search!!!')
            print(f'Number of compounds found: {len(links[1:])}')
            filename = f'results_KNApSAcK_{self.searchtype}_{self.keyword}.csv'
            print('Retrieving data ...')
            results = self.retrieve_data(links) 
            results.to_csv(filename, index=False)
            print('Done')
        else:
            print('No results were found!')
        
    
    
    def spinning_cursor(self):
        while True:
            for cursor in '|/-\\':
                yield cursor
    
    
    
    
    
    
if __name__ == '__main__':
    args = arg_parser()
    if args.searchtype not in ['metabolite', 'organism']:
        print('Type of search not recognized.')
        print('Please specify either "metabolite" or "organism".')
    app = KNApSAcKSearch(searchtype=args.searchtype, keyword=args.keyword)
    app.execute()
    
    
