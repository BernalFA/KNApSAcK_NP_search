#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple GUI to perform general searches on KNApSAcK web database 
http://www.knapsackfamily.com/knapsack_core/top.php 
by metabolite or organism. 
It creates a csv file with Name, CAS ID, KNApSAcK ID, and SMILES
for each compound found by a user specified keyword. The file is
saved to the current folder.

Created on Wed Jul 27 15:48:39 2022

@author: Dr. Freddy Bernal
"""
# Import essentials
import tkinter as tk
from tkinter import Tk#, ttk
import webbrowser
import requests 
from bs4 import BeautifulSoup 
import pandas as pd
import time
from itertools import cycle
# import os


###############
#  FUNCTIONS  #
###############

class KNApSAcKSearch(Tk):
    progress = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('KNApSAcK')
        self.geometry('300x180')
        self.resizable(width=False, height=False)
        
        self.base_url = 'http://www.knapsackfamily.com/knapsack_core/top.php'
        
        # self.progress = 0
        
        self.values = [0, 20, 40, 60, 80, 100, 80, 60, 40, 20]
        self.values_cycle = cycle(self.values)
        
    def makeform(self):
        # Create frame for title
        self.frm_title = tk.Frame(self, height=50, width=300, 
                                  padx=5, pady=5, bg='#deebf7')
        self.frm_title.pack(side='top', fill='x')
        self.frm_title.pack_propagate(0) # To ensure dimensions
        # Create label for title
        self.lbl_title1 = tk.Label(self.frm_title, 
                                   text='KNApSAcK Simple Searching Tool', 
                                   font=('Arial', 22, 'bold'), 
                                   cursor='hand2',
                                   bg='#deebf7')
        # Add hyperlink to original website
        self.lbl_title1.bind('<Button-1>', lambda e: self.hyperlink)
        self.lbl_title1.pack()

        # Create frame for user input information
        self.frm_input = tk.Frame(self, height=100, width=300, 
                                  padx=5, pady=5)
        self.frm_input.pack(fill='x')
        self.frm_input.pack_propagate(0)
        # Create label for search type
        self.lbl_type = tk.Label(self.frm_input, 
                                 text='Search by:',
                                 font=('Arial', 16),
                                 )
        # Create radio buttons to select type
        self.radio = tk.IntVar()
        self.radio.set(1)
        self.R1 = tk.Radiobutton(self.frm_input, text="Metabolite", 
                                 variable=self.radio, value=1,
                                 font=('Arial', 16))
        self.R2 = tk.Radiobutton(self.frm_input, text="Organism", 
                                 variable=self.radio, value=2,
                                 font=('Arial', 16))
        # Organize by grid
        self.lbl_type.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.R1.grid(row=0, column=1)
        self.R2.grid(row=0, column=2)

        # Create label for keyword
        self.lbl_key = tk.Label(self.frm_input, 
                                text='Keyword:',
                                font=('Arial', 16), 
                                )
        # Create text input
        self.ent_key = tk.Entry(self.frm_input, width=25, font=('Arial', 16))
        # Organize by grid 
        self.lbl_key.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.ent_key.grid(row=1, column=1, columnspan=3, sticky='w', padx=5, pady=5)

        # Create frame for search button
        self.frm_btn = tk.Frame(self, height=100, width=300, padx=5, pady=5)
        self.frm_btn.pack()
        # Create search button
        self.btn_search = tk.Button(self.frm_btn, 
                                    text='Search',
                                    # command=lambda: [self.execute(), self.progressbar()],
                                    command=self.execute,
                                    font=('Arial', 18, 'bold'),
                                    bg='#3182bd', 
                                    fg='white')
        self.btn_search.pack()


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
        self.update_idletasks()
        self.frm_pro = tk.Frame(self, height=100, width=300, 
                                padx=5, pady=5)
        self.frm_pro.pack(fill='x')
        
        # pb = ttk.Progressbar(self.frm_pro, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
        # pb.grid(row=0, column=1)
        
        # progressbar = self.progressbar()
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
            
            for i in '|/-\\'*2:
                msg = tk.Label(self.frm_pro, text='Processing ' + i, font=('Arial', 14))
                msg.grid(row=0, column=0, sticky='w', padx=5, pady=5)
                self.update_idletasks()
                time.sleep(0.1)
                    
            KNApSAcKSearch.progress += 1
            print(KNApSAcKSearch.progress)
        # progressbar.quit()
        
        KNApSAcKSearch.progress = -1
            
        return res


    # Define callback function directed to KNApSAcK website
    def hyperlink(self):
        webbrowser.open_new(self.base_url)


    

    # Define execution function
    def execute(self):
        """
        Creates global variables for user input entries and 
        run search
    
        Returns
        -------
        None.
    
        """
        
        # Make globals for user input
        keyword = self.ent_key.get()
        searchtype = self.radio.get()
        if searchtype == 1:
            searchtype = 'metabolite'
        elif searchtype == 2:
            searchtype = 'organism'
        
        
        
        
        
        # Search for compounds using user input
        links = self.get_cmpds(searchtype, keyword)
        if len(links) > 1: 
            print(len(links[1:]))
            filename = f'results_KNApSAcK_{searchtype}_{keyword}.csv'
            # progressbar = self.progressbar()
            results = self.retrieve_data(links) 
            
            # progressbar.quit()
            
            results.to_csv(filename, index=False)
            self.quit()
        else:
            top = tk.Toplevel()
            top.title('Result')
            top.geometry('120x90')
            msg = tk.Message(top, text='No results found', font=('Arial', 18, 'bold'))
            msg.pack()
            button = tk.Button(top, text='Dismiss', command=top.destroy)
            button.pack()
        
    
    def next_value(self):
        
        return next(self.values_cycle)
            
    

    
    
    
if __name__ == '__main__':
    app = KNApSAcKSearch()
    app.makeform()
    
    app.mainloop()
    
