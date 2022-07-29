# KNApSAcK search utility

KNApSAcK search utility is a Python script and GUI to look for natural compounds in the KNApSAcK database (http://www.knapsackfamily.com/knapsack_core/top.php).
The application is based on scrapping of the original web database and limited to search only by `metabolite` and `organism`. A `csv` file containing SMILES strings, common name(s), CAS number, and KNApSAcK ID is returned. The application is ideal for Virtual Screening endeavors. 

## Requirements
___
KNApSAcK search utility makes use of: 
* Requests 
* Beautiful Soup
* Pandas

## Usage
___
To run the GUI 

```bash
$ python KNApSAcK_GUI.py
``` 

## License
___
[MIT](https://choosealicense.com/licenses/mit/)