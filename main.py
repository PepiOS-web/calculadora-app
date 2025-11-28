import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CalculadoraApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CalculadoraApp")
        self.geometry("340x430")
        self.resizable(False,False)
        
        self.bg_color = '#111827'
        self.btn_color = "#1f2937"
        self.op_color = "#f59e0b"
        self.eq_color ="#10b981" 
        self.text_color = "#f9fafb"
        
        self.configure(bg=self.bg_color)
        
        self.expression = ""
        
        self._create_display()
        self._create_buttons()
        self._create_style()
        
    def _create_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "TButton",
            font=("Segoe UI", 14),
            padding=8,
            background=self.btn_color,
            foreground=self.text_color,
            borderwidth=0
        )        
        
        style.map(
            "TButton",
            background=[("active", "#374151")]
        )

        style.configure(
            "Op.TButton",
            background=self.op_color,
            foreground="#111827"
        )
        style.map(
            "Op.TButton",
            background=[("active", "#d97706")]
        )

        style.configure(
            "Eq.TButton",
            background=self.eq_color,
            foreground="#111827"
        )
        style.map(
            "Eq.TButton",
            background=[("active", "#059669")]
        )

    def _create_display(self):
        frame_display = tk.Frame(self, bg=self.bg_color)
        frame_display.pack(fill="x", padx=10, pady=10)

        # Campo de texto
        self.display_var = tk.StringVar()
        self.display = tk.Entry(
            frame_display,
            textvariable=self.display_var,
            font=("Segoe UI", 22),
            justify="right",
            bd=0,
            bg=self.bg_color,
            fg=self.text_color,
            insertbackground=self.text_color
        )
        self.display.pack(fill="x")

    def _create_buttons(self):
        frame_buttons = tk.Frame(self, bg=self.bg_color)
        frame_buttons.pack(expand=True, fill="both", padx=10, pady=(0, 10))

        # Diseño de botones: texto, fila, columna, estilo
        buttons = [
            ("C", 0, 0, "Op"), ("⌫", 0, 1, "Op"), ("%", 0, 2, "Op"), ("/", 0, 3, "Op"),
            ("7", 1, 0, None), ("8", 1, 1, None), ("9", 1, 2, None), ("*", 1, 3, "Op"),
            ("4", 2, 0, None), ("5", 2, 1, None), ("6", 2, 2, None), ("-", 2, 3, "Op"),
            ("1", 3, 0, None), ("2", 3, 1, None), ("3", 3, 2, None), ("+", 3, 3, "Op"),
            ("0", 4, 0, None), (".", 4, 1, None), ("=", 4, 2, "Eq"),
        ]

        # Ajustar columnas para que se expandan
        for i in range(4):
            frame_buttons.columnconfigure(i, weight=1)
        for i in range(5):
            frame_buttons.rowconfigure(i, weight=1)

        for (text, row, col, style) in buttons:
            if text == "=":
                btn = ttk.Button(
                    frame_buttons,
                    text=text,
                    style="Eq.TButton",
                    command=self.calculate
                )
                # Que el "=" ocupe dos columnas
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=4, pady=4)
            else:
                if style == "Op":
                    btn_style = "Op.TButton"
                else:
                    btn_style = "TButton"

                btn = ttk.Button(
                    frame_buttons,
                    text=text,
                    style=btn_style,
                    command=lambda t=text: self.on_button_click(t)
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

    def on_button_click(self, char: str):
        """Gestiona la pulsación de botones numéricos y de operación."""
        if char == "C":
            self.clear()
        elif char == "⌫":
            self.backspace()
        else:
            self.expression += char
            self.display_var.set(self.expression)

    def clear(self):
        """Limpia la pantalla."""
        self.expression = ""
        self.display_var.set("")

    def backspace(self):
        """Borra el último caracter."""
        self.expression = self.expression[:-1]
        self.display_var.set(self.expression)

    def calculate(self):
        """Evalúa la expresión actual de forma segura."""
        if not self.expression:
            return

        try:
            # Reemplazar % por /100 para porcentajes
            expr = self.expression.replace("%", "/100")

            # Evaluar expresión
            result = eval(expr, {"__builtins__": None}, {})
            self.expression = str(result)
            self.display_var.set(self.expression)
        except Exception:
            messagebox.showerror("Error", "Expresión inválida")
            self.clear()


if __name__ == "__main__": 
    app = CalculadoraApp()
    app.mainloop()
