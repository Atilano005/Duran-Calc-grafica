import tkinter as tk
from tkinter import ttk
import math
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class ScientificCalculatorWithGraph(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Duran 1.0")
        self.geometry("700x400")
        self.history = ""

        # Layout:
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        calc_frame = tk.Frame(main_frame)
        calc_frame.pack(side="left", fill="y", expand=False, padx=10, pady=10)

        graph_frame = tk.Frame(main_frame)
        graph_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # ----- Calc -----
        self.history_var = tk.StringVar()
        tk.Label(calc_frame, textvariable=self.history_var, anchor="e", font=("Arial", 12), bg="#e0e0e0").pack(fill="x")

        self.input_var = tk.StringVar()
        entry = tk.Entry(calc_frame, textvariable=self.input_var, font=("Arial", 16), justify="right")
        entry.pack(fill="x", padx=5, pady=5)
        entry.bind("<Return>", self.on_return)

        btn_frame = tk.Frame(calc_frame)
        btn_frame.pack(expand=True, fill="both")

        # botones
        self.buttons = {}

        buttons = [
            ('7', '8', '9', '/', 'sin', 'cos'),
            ('4', '5', '6', '*', 'tan', 'log'),
            ('1', '2', '3', '-', 'ln', 'sqrt'),
            ('0', '.', '!', '+', '^', 'exp'),
            ('(', ')', 'pi', 'e', 'C', '='),
        ]
        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                btn = tk.Button(btn_frame, text=char, font=("Arial", 14), command=lambda ch=char: self.on_button(ch))
                btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
                self.buttons[char] = btn  # referencia
        for i in range(6):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(len(buttons)):
            btn_frame.rowconfigure(i, weight=1)

        # Plot boton
        plot_btn = tk.Button(calc_frame, text="Plot", font=("Arial", 14), bg="#6fa8dc", fg="white", command=self.plot_graph)
        plot_btn.pack(fill="x", pady=8)
        self.buttons["Plot"] = plot_btn  # 'Plot' 

        # ----- Grafico -----
        self.fig, self.ax = plt.subplots(figsize=(5, 3.5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # colores
        self.set_button_color('=', '#ffd966')      # 
        self.set_button_color('C', '#ffd966')      # 

    def set_button_color(self, button_text, color):
        """Cambio color."""
        btn = self.buttons.get(button_text)
        if btn:
            btn.config(bg=color)

    def on_button(self, char):
        if char == 'C':
            self.input_var.set("")
        elif char == '=':
            self.calculate()
        elif char == 'pi':
            self.input_var.set(self.input_var.get() + str(math.pi))
        elif char == 'e':
            self.input_var.set(self.input_var.get() + str(math.e))
        else:
            self.input_var.set(self.input_var.get() + char)

    def on_return(self, event):
        self.calculate()

    def calculate(self):
        expr = self.input_var.get().replace('^', '**')
        expr = expr.replace('ln', 'math.log')
        expr = expr.replace('log', 'math.log10')
        expr = expr.replace('sqrt', 'math.sqrt')
        expr = expr.replace('sin', 'math.sin')
        expr = expr.replace('cos', 'math.cos')
        expr = expr.replace('tan', 'math.tan')
        expr = expr.replace('exp', 'math.exp')
        expr = expr.replace('pi', str(math.pi))
        expr = expr.replace('e', str(math.e))
        expr = expr.replace('!', 'math.factorial')
        import re
        if 'math.factorial' in expr:
            expr = re.sub(r'(\d+)math\.factorial', r'math.factorial(\1)', expr)
        try:
            result = str(eval(expr, {"math": math}))
            self.history += self.input_var.get() + " = " + result + "\n"
            self.history_var.set(self.history.splitlines()[-1] if self.history else "")
            self.input_var.set(result)
        except Exception:
            self.input_var.set("Error")

    def plot_graph(self):
        expr = self.input_var.get()
        allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
        allowed_names['x'] = None
        expr_plot = expr.replace('^', '**')
        expr_plot = expr_plot.replace('ln', 'np.log')
        expr_plot = expr_plot.replace('log', 'np.log10')
        expr_plot = expr_plot.replace('sqrt', 'np.sqrt')
        expr_plot = expr_plot.replace('sin', 'np.sin')
        expr_plot = expr_plot.replace('cos', 'np.cos')
        expr_plot = expr_plot.replace('tan', 'np.tan')
        expr_plot = expr_plot.replace('exp', 'np.exp')
        expr_plot = expr_plot.replace('pi', 'np.pi')
        expr_plot = expr_plot.replace('e', 'np.e')
        expr_plot = expr_plot.replace('!', '')  
        x = np.linspace(-10, 10, 400)
        try:
            allowed_names['x'] = x
            y = eval(expr_plot, {"np": np, **allowed_names})
            self.ax.clear()
            self.ax.plot(x, y)
            self.ax.set_title(f"y = {expr}")
            self.ax.grid(True)
            self.canvas.draw()
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Error plotting:\n{e}", ha='center', va='center', fontsize=12)
            self.ax.set_title("Plot Error")
            self.canvas.draw()

if __name__ == "__main__":
    ScientificCalculatorWithGraph().mainloop()