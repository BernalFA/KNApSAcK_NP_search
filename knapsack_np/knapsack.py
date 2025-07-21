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
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class KNApSAcKSearch():
    def __init__(self, searchtype: str, keyword: str):
        """
        Args:
            searchtype (str): whether to search for 'metabolite' or 'organism'.
            keyword (str): specific name to search for.
        """
        self._base_url = 'http://www.knapsackfamily.com/knapsack_core/top.php'
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
        try:
            # get html content of results page
            page = requests.get(url)
            # parse the content
            soup = BeautifulSoup(page.content, 'html.parser')
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

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
        search_url = self._base_url[:self._base_url.rfind('/')] + search_val
        # get html content of results page
        links = self._fetch(search_url)

        return links

    def _get_compound_data(self, link: str) -> dict:
        """Fetch and extract compound information from the provided link.

        Args:
            link (str): url fragment for a compound as provided by get_links()

        Returns:
            dict: compound information, including Name(s), CAS number, KNApSAcK ID,
                  and SMILES strings.
        """
        # define url
        url = self._base_url[:self._base_url.rfind('/')] + '/' + link
        # get html and parse the content
        data = self._fetch(url, compound=True)
        # extract name(s), CAS ID, KNApSAcK ID, and SMILES
        info = {
            "Names": ", ".join(list(data[0].stripped_strings)),
            "CAS No.": data[3].get_text(),
            "KNApSAcK ID": data[4].get_text().split()[0],
            "SMILES": data[7].get_text()
        }
        return info

    def search(self, max_workers=10) -> pd.DataFrame:
        """Perform complete search and information retrieval for keyword and searchtype.

        Args:
            max_workers (int, optional): number of simultaneous access to the KNApSAcK
                                         website. Defaults to 10 (higher values might
                                         cause conflicts).

        Returns:
            pd.DataFrame: compound information (Name(s), CAS number, KNApSAcK ID,
                          and SMILES strings) for all the results from the search.
        """
        links = self.get_links()
        if len(links) > 1:
            print('Successfull search!!!')
            print(f'Number of compounds found: {len(links)}')
            print('Retrieving data ...')
            results = []
            # for link in tqdm(links, desc="Compounds"):
            #     results.append(self.get_compound_data(link))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [
                    executor.submit(self._get_compound_data, link) for link in links
                ]
                for future in tqdm(
                    as_completed(futures), total=len(futures), desc="Compounds"
                ):
                    res = future.result()
                    if res:
                        results.append(res)
            results = pd.DataFrame(results)
            print('Done')
            return results
        else:
            print('No results were found!')
