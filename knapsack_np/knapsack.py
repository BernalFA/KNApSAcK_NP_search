"""
Utility classes to perform searches on the KNApSAcK web database
(http://www.knapsackfamily.com/knapsack_core/top.php) using a metabolite or organism
as keyword.
A dataframe containing Name, CAS ID, KNApSAcK ID, and SMILES for each compound found by
the user specified keyword.

Modified on Wed Jul 21 2025

@author: Dr. Freddy Bernal
"""
# Import essentials
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys


class KNApSAcKSearch():
    progress = 0

    def __init__(self, searchtype: str, keyword: str):
        """
        Args:
            searchtype (str): whether to search for 'metabolite' or 'organism'.
            keyword (str): specific name to search for.
        """
        self.base_url = 'http://www.knapsackfamily.com/knapsack_core/top.php'
        self.searchtype = searchtype
        self.keyword = keyword

    def _fetch(self, url: str, compound=False) -> list:
        """Download KNApSAcK website information for given url. If url for compound,
        extract must be set to True in order to retrieve data.

        Args:
            url (str): url to search content
            compound (bool): whether to extract compound information. Only useful
                             if the url contains compound information.

        Returns:
            list: downloaded website information. Either links to compounds or compound
                  information.
        """
        # get html content of results page
        page = requests.get(url)
        # parse the content
        soup = BeautifulSoup(page.content, 'html.parser')
        if compound:
            # extract compounds' information
            data = soup.find_all('td', {'colspan': 4})
        else:
            # extract links (corresponding to compounds)
            data = [element['href'] for element in soup.find_all('a', href=True)]
            data = [link for link in data if "information" in link]
        return data

    def get_links(self) -> list:
        """Retrieve list of url links to compounds from user defined input by scraping
        the KNApSAcK website.

        Returns:
            list: url links to compounds obtained as result from specified search.
        """
        # transform user input into url chunk
        search_val = f'/result.php?sname={self.searchtype}&word={self.keyword}'
        # Remove last part of base url and add user defined url
        # (taken from https://stackoverflow.com/questions/54961679/python-removing-the-last-part-of-an-url) # noqa: E501
        search_url = self.base_url[:self.base_url.rfind('/')] + search_val
        # get html content of results page
        links = self._fetch(search_url)

        return links

    def retrieve_data(self, links: list) -> pd.DataFrame:
        """
        Search each link provided and retrieve predefined compound information.

        Parameters
        ----------
        links : list
            url links resulting from customized search with get_cmpds().

        Returns
        -------
        res : pd.DataFrame
            Matrix with Name(s), CAS ID, KNApSAcK ID and SMILES strings for all the
            compounds obtained by the search.
        """
        # Retrieve data from each link
        res = pd.DataFrame(columns=['Names', 'CAS', 'KNApSAcK_ID', 'smiles'])
        for link in links[1:]:
            # define url
            url = self.base_url[:self.base_url.rfind('/')] + '/' + link
            # get html and parse the content
            data = self._fetch(url, compound=True)
            # extract name(s), CAS ID, KNApSAcK ID, and SMILES
            names = list(data[0].stripped_strings)
            cas = data[3].get_text()
            dbid = data[4].get_text().split()[0]
            smi = data[7].get_text()

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

    def execute(self) -> None:
        """
        Creates global variables for user input entries and run search

        Returns
        -------
        None.
        """
        # Search for compounds using user input
        links = self.get_links()
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
        """Simple utility to show progress of the process while running under CLI.

        Yields:
            str: alternating symbol.
        """
        while True:
            for cursor in '|/-\\':
                yield cursor
