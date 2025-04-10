#Requisitos iniciais necessarios

#pip install graphviz

#instalar também no sistema https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/12.2.1/windows_10_cmake_Release_graphviz-install-12.2.1-win64.exe

import tkinter as tk
from tkinter import messagebox, simpledialog
from main import criar_afd, validar_palavra, minimizar_afd, obter_tabela_transicoes

class AFDInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de AFD")

        window_width, window_height = 800, 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        root.resizable(False, False)

        self.afd = None

        self.sidebar = tk.Frame(root, width=200, bg="#30304a")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.main_area = tk.Frame(root, bg="#d9d9d9")
        self.main_area.pack(expand=True, fill=tk.BOTH)

        button_conf = {"fill": tk.X, "padx": 10, "pady": 10}

        tk.Button(self.sidebar, text="Definir AFD", command=self.definir_afd).pack(**button_conf)
        tk.Button(self.sidebar, text="Validar Palavra", command=self.validar_palavra).pack(**button_conf)
        tk.Button(self.sidebar, text="Visualizar AFD", command=self.visualizar_afd).pack(**button_conf)
        tk.Button(self.sidebar, text="Minimizar AFD", command=self.minimizar_afd).pack(**button_conf)
        tk.Button(self.sidebar, text="Mostrar Tabela", command=self.mostrar_tabela).pack(**button_conf)

        tk.Label(self.sidebar, bg="#30304a").pack(expand=True, fill=tk.BOTH)

        tk.Button(self.sidebar, text="Sair", command=root.quit).pack(**button_conf)

        info_text = ("Projeto Feito para a disciplina de\nTeoria da Computação\n\n"
                     "Criação, validação e minização feita baseada em\n"
                     "automatos finitos determinísticos, e visualização feita\n"
                     "usando a biblioteca graphviz, que também precisa estar\n"
                     "instalado no seu computador.")

        tk.Label(self.main_area, text=info_text, bg="#d9d9d9", justify=tk.CENTER, font=("Arial", 12)).pack(expand=True)

    def definir_afd(self):
        top = tk.Toplevel(self.root)
        top.title("Definir AFD")
        top.transient(self.root)
        top.grab_set()

        entries = {}
        fields = [
            ("Alfabeto (separados por espaço)", "sigma"),
            ("Estados (separados por espaço)", "Q"),
            ("Estado inicial", "q0"),
            ("Estados finais (separados por espaço)", "F")
        ]

        for label, key in fields:
            row = tk.Frame(top)
            lab = tk.Label(row, width=30, text=label, anchor='w')
            ent = tk.Entry(row, width=50)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries[key] = ent

        def submit():
            sigma = entries["sigma"].get().split()
            Q = entries["Q"].get().split()
            q0 = entries["q0"].get()
            F = entries["F"].get().split()

            top.destroy()
            self.definir_transicoes(sigma, Q, q0, F)

        tk.Button(top, text="Próximo", command=submit).pack(pady=10)

    def definir_transicoes(self, sigma, Q, q0, F):
        top = tk.Toplevel(self.root)
        top.title("Definir Transições")
        top.transient(self.root)
        top.grab_set()

        entries = {}
        canvas = tk.Canvas(top)
        scrollbar = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for estado in Q:
            for simbolo in sigma:
                label = f"δ({estado}, {simbolo}) ="
                row = tk.Frame(scrollable_frame)
                lab = tk.Label(row, width=20, text=label, anchor='w')
                ent = tk.Entry(row, width=30)
                row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
                lab.pack(side=tk.LEFT)
                ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
                entries[(estado, simbolo)] = ent

        def submit():
            delta = {}
            for (estado, simbolo), entry in entries.items():
                delta[(estado, simbolo)] = entry.get() if entry.get() else ''

            self.afd = criar_afd(set(sigma), set(Q), q0, set(F), delta)
            messagebox.showinfo("AFD Definido", "AFD criado com sucesso!")
            top.destroy()

        tk.Button(scrollable_frame, text="Confirmar", command=submit).pack(pady=10)

    def validar_palavra(self):
        if self.afd is None:
            messagebox.showerror("Erro", "Defina um AFD primeiro.")
            return

        palavra = simpledialog.askstring("Validar Palavra", "Informe a palavra a ser validada:")
        if palavra:
            resultado, etapas = validar_palavra(self.afd, palavra)
            mensagem = "\n".join(etapas)
            messagebox.showinfo("Resultado", mensagem)

    def minimizar_afd(self):
        if self.afd is None:
            messagebox.showerror("Erro", "Defina um AFD primeiro.")
            return

        self.afd = minimizar_afd(self.afd)
        messagebox.showinfo("AFD Minimizado", "AFD minimizado com sucesso!")

    def visualizar_afd(self):
        if self.afd is None:
            messagebox.showerror("Erro", "Defina um AFD primeiro.")
            return

        self.afd.visualizar()
        messagebox.showinfo("Visualização", "Representação visual do AFD gerada com sucesso!")

    def mostrar_tabela(self):
        if self.afd is None:
            messagebox.showerror("Erro", "Defina um AFD primeiro.")
            return

        tabela = obter_tabela_transicoes(self.afd)
        messagebox.showinfo("Tabela de Transições", tabela)

if __name__ == "__main__":
    root = tk.Tk()
    app = AFDInterface(root)
    root.mainloop()
