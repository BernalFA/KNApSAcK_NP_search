"""
Simple GUI to perform general searches on KNApSAcK web database
http://www.knapsackfamily.com/knapsack_core/top.php by metabolite or organism.

It creates a csv file with Name, CAS ID, KNApSAcK ID, and SMILES for each compound
found by a user specified keyword. The file is saved to the current folder.

Modified on Jul 21 2025

@author: Dr. Freddy Bernal
"""
# Import essentials
import tkinter as tk
import webbrowser
import time

from knapsack_np import KNApSAcKSearch


###############
#  FUNCTIONS  #
###############
class KNApSAcKGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('KNApSAcK_NP_Search')
        self.geometry('600x260')
        self.resizable(width=False, height=False)
        # self.values = [0, 20, 40, 60, 80, 100, 80, 60, 40, 20]
        # self.values_cycle = cycle(self.values)

    def makeform(self):
        # Create frame for title
        self.frm_title = tk.Frame(self, height=50, width=300,
                                  padx=5, pady=5, bg='#deebf7')
        self.frm_title.pack(side='top', fill='x')
        self.frm_title.pack_propagate(0)  # To ensure dimensions
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
                                    command=self.execute,
                                    font=('Arial', 18, 'bold'),
                                    bg='#3182bd',
                                    fg='white')
        self.btn_search.pack()

    # Define callback function directed to KNApSAcK website
    def hyperlink(self):
        webbrowser.open_new(self.base_url)

    # Define execution function
    def execute(self):
        # Make globals for user input
        keyword = self.ent_key.get()
        searchtype = self.radio.get()
        if searchtype == 1:
            searchtype = 'metabolite'
        elif searchtype == 2:
            searchtype = 'organism'

        self.update_idletasks()
        self.frm_pro = tk.Frame(self, height=100, width=300, 
                                padx=5, pady=5)
        self.frm_pro.pack(fill='x')
        # Search for compounds using user input
        collector = KNApSAcKSearch(searchtype, keyword)
        results = collector.search()
        if len(results) > 1:
            # filename = f'results_KNApSAcK_{searchtype}_{keyword}.csv'
            # results.to_csv(filename, index=False)
            self.quit()
        else:
            top = tk.Toplevel()
            top.title('Result')
            top.geometry('120x90')
            msg = tk.Message(top, text='No results found', font=('Arial', 18, 'bold'))
            msg.pack()
            button = tk.Button(top, text='Dismiss', command=top.destroy)
            button.pack()


if __name__ == '__main__':
    app = KNApSAcKGUI()
    app.makeform()

    app.mainloop()
