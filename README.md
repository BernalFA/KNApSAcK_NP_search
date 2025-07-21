# KNApSAcK search utility

KNApSAcK search utility is a Python script and GUI to look for natural compounds in the KNApSAcK database (http://www.knapsackfamily.com/knapsack_core/top.php).
The application is based on scrapping of the original web database and limited to search only by `metabolite` and `organism`. A `csv` file containing SMILES strings, common name(s), CAS number, and KNApSAcK ID is returned. The application is ideal for Virtual Screening endeavors. 

## Requirements

KNApSAcK search utility makes use of:
* Python > 3.9
* Requests 
* Beautiful Soup
* Pandas
* tqdm

## Usage

To run as python package, create a separate environment first

```bash
conda create -n knapsack
conda install -c conda-forge requests, beautifulsoup4, pandas, tqdm
```

```python
from knapsack_np import KNApSAcKSearch

collector = KNApSAcKSearch(searchtype="organism", keyword="Baccharis")
results = collector.search()
```


To run the GUI 

```bash
$ python KNApSAcK_GUI.py
``` 

## License

The content of this project is licensed under [MIT license](https://choosealicense.com/licenses/mit/)
