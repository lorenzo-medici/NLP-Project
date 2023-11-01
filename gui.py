# This file contains the user interface. The GUI should contain two text
#    boxes, a way to select which of the four method to use, and an output
#    field for the semantic similarity using the selected method
# It shall import the similarity functions file but not the dataset

import tkinter as tk
import tkinter.ttk as ttk

from similarity_calculators import *


def draw_gui():
    window = tk.Tk()

    window.geometry('570x230')

    # Style

    ttk.Style().configure('pad.TEntry', padding='10 10 10 10')

    # Layout
    window.title("Semantic Similarity Calculator")
    s1_label = tk.Label(window, text="Sentence 1")
    s2_label = tk.Label(window, text="Sentence 2")

    S1 = tk.StringVar()
    S2 = tk.StringVar()

    s1_text = ttk.Entry(window, textvariable=S1, width=50, style='pad.TEntry')
    s2_text = ttk.Entry(window, textvariable=S2, width=50, style='pad.TEntry')

    s1_label.grid(row=0, column=0, pady=10)
    s1_text.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
    s2_label.grid(row=1, column=0, pady=10)
    s2_text.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    m_label = tk.Label(window, text="Select similarity method:")
    m_label.grid(row=2, column=0, sticky=tk.W, padx=10)

    methodChoice = tk.IntVar()
    m1_radio = tk.Radiobutton(window, text="Mihalcea et al.", variable=methodChoice, value=0, )
    m1_radio.grid(row=3, column=0, sticky=tk.W, ipadx=10, columnspan=2)
    m2_radio2 = tk.Radiobutton(window, text="WuPalmer average", variable=methodChoice, value=1)
    m2_radio2.grid(row=4, column=0, sticky=tk.W, ipadx=10, columnspan=2)
    m1_radio = tk.Radiobutton(window, text="Hyper- and Hyponyms", variable=methodChoice, value=2)
    m1_radio.grid(row=5, column=0, sticky=tk.W, ipadx=10, columnspan=2)
    m1_radio = tk.Radiobutton(window, text="SOC PMI Short Text Similarity", variable=methodChoice, value=3)
    m1_radio.grid(row=6, column=0, sticky=tk.W, ipadx=10, columnspan=2)

    frm_entry = tk.Frame(master=window)

    calc_button = tk.Button(master=frm_entry, text="Analyze sentences")
    calc_button.grid(row=0, column=0, sticky=tk.W + tk.N, padx=50)

    result_label = tk.Label(master=frm_entry, text="Result: NaN")
    result_label.grid(row=0, column=1, sticky=tk.E)

    frm_entry.grid(row=4, column=2, rowspan=4, sticky=tk.N + tk.S + tk.E + tk.W)

    # Event binds

    methods = [method_1_wordnet, method_2_wupalmer, method_3_hypernyms, method_4_library]

    def run_similarity(event):
        S1_input, S2_input = S1.get().strip(), S2.get().strip()
        if S1_input == "" or S2_input == "":
            result_label.config(text="Result: NaN")
            return

        result_label.config(text=f"Result: {methods[methodChoice.get()](S1_input, S2_input):.2f}")

    calc_button.bind("<Button-1>", run_similarity)

    window.mainloop()


if __name__ == '__main__':
    draw_gui()
