"""
Simple GUI to perform general searches on KNApSAcK web database
http://www.knapsackfamily.com/knapsack_core/top.php by metabolite or organism.

It creates a csv file with Name, CAS ID, KNApSAcK ID, and SMILES for each compound
found by a user specified keyword. The file is saved to the current folder.

Modified on Jul 21 2025

@author: Dr. Freddy Bernal
"""
# Import essentials
import threading
import tkinter as tk
import webbrowser
from tkinter import ttk

from knapsack_np import KNApSAcKSearch


class KNApSAcKGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('KNApSAcK_NP_Search')
        self.geometry('600x260')
        self.resizable(width=False, height=False)
        self._base_url = 'http://www.knapsackfamily.com/knapsack_core/top.php'

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
        self.lbl_title1.bind('<Button-1>', lambda e: self.hyperlink())
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
        # Instantiate a progress bar
        self.progress_frame = tk.Frame(self)
        self.lbl_progress = tk.Label(self.progress_frame, text="Progress",
                                     font=('Arial', 14))
        self.lbl_progress.grid(row=0, column=0, padx=(0, 10))
        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal",
                                        length=300, mode="determinate")
        self.progress.grid(row=0, column=1)
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
        webbrowser.open_new(self._base_url)

    def execute(self):
        # Make globals for user input
        keyword = self.ent_key.get()
        searchtype = self.radio.get()
        if searchtype == 1:
            searchtype = 'metabolite'
        elif searchtype == 2:
            searchtype = 'organism'

        # run process as a thread to avoid blocking GUI (and refreshing progress bar)
        threading.Thread(
            target=self.run_search,
            args=(searchtype, keyword),
            daemon=True
        ).start()

    def show_progress_bar(self, total):
        self.progress["maximum"] = total
        self.progress["value"] = 0
        self.progress_frame.pack(pady=10)

    def run_search(self, searchtype, keyword):
        # Search for compounds using user input
        collector = KNApSAcKSearch(searchtype, keyword)
        total = len(collector.get_links())

        self.after(0, lambda: self.show_progress_bar(total))

        results = collector.search_with_progress(self.safe_callback)

        def show_results():
            self.progress_frame.pack_forget()
            if results is not None:
                self.quit()
            else:
                top = tk.Toplevel()
                top.title('Result')
                top.geometry('120x90')
                msg = tk.Message(top, text='No results found',
                                 font=('Arial', 18, 'bold'))
                msg.pack()
                button = tk.Button(top, text='Dismiss', command=top.destroy)
                button.pack()

        self.after(0, show_results)

    def safe_callback(self, value):
        self.after(0, self.update_progress, value)

    def update_progress(self, value):
        self.progress["value"] = value
        self.update_idletasks()


if __name__ == '__main__':
    app = KNApSAcKGUI()
    app.makeform()

    app.mainloop()
