import tkinter as tk
from tkinter import messagebox, ttk

class Chamado:
    id = 1

    def __init__(self, titulo, motivo):
        self.id = Chamado.id
        self.titulo = titulo
        self.motivo = motivo
        self.status = "Aberto"
        Chamado.id += 1

    def alterar_status(self, novo_status):
        self.status = novo_status

class Sistema:
    def __init__(self):
        self.chamados = []

    def abrir(self, titulo, descricao):
        chamado = Chamado(titulo, descricao)
        self.chamados.append(chamado)
        return chamado
    
    def listar(self):
        return self.chamados
    
    def buscar(self, id_chamado):
        for chamado in self.chamados:
            if chamado.id == id_chamado:
                return chamado
        return None

class ITsolutions:
    def __init__(self, principal):
        self.sistema = Sistema()
        self.principal = principal
        self.principal.title("IT Solutions - Sistema de Chamados")
        self.principal.geometry("800x500")
        self.principal.config(bg="#34495e")
        self.principal.protocol("WM_DELETE_WINDOW", self.confirmar_sair)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 11), padding=6)
        style.configure("Treeview", font=("Arial", 10), rowheight=24)
        style.map("TButton", background=[("active", "#2980b9")])

        self.menu_frame = tk.Frame(principal, width=200, bg="#2c3e50")
        self.menu_frame.pack(side="left", fill="y")

        tk.Label(self.menu_frame, text="MENU", fg="white", bg="#2c3e50", font=("Arial", 14, "bold")).pack(pady=20)

        ttk.Button(self.menu_frame, text="Abrir Chamado", command=lambda: self.mostrar_frame("abrir")).pack(pady=10, fill="x")
        ttk.Button(self.menu_frame, text="Listar Chamados", command=lambda: self.mostrar_frame("listar")).pack(pady=10, fill="x")
        ttk.Button(self.menu_frame, text="Alterar Status", command=lambda: self.mostrar_frame("alterar")).pack(pady=10, fill="x")
        ttk.Button(self.menu_frame, text="Sair", command=self.confirmar_sair).pack(pady=20, fill="x")

        self.conteudo = tk.Frame(principal, bg="#ecf0f1")
        self.conteudo.pack(side="right", expand=True, fill="both")

        self.frames = {}
        self.criar_frames()
        self.mostrar_frame("abrir")

    def criar_frames(self):
        frame_abrir = tk.Frame(self.conteudo, bg="#ecf0f1")
        tk.Label(frame_abrir, text="Novo Chamado", font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=20)

        form = tk.Frame(frame_abrir, bg="#ecf0f1")
        form.pack(pady=10)

        tk.Label(form, text="Título:", bg="#ecf0f1").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_titulo = tk.Entry(form, width=40)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Descrição:", bg="#ecf0f1").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_motivo = tk.Entry(form, width=40)
        self.entry_motivo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_abrir, text="Salvar", command=self.salvar).pack(pady=20)
        self.frames["abrir"] = frame_abrir

        frame_listar = tk.Frame(self.conteudo, bg="#ecf0f1")
        tk.Label(frame_listar, text="Lista de Chamados", font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=20)

        colunas = ("ID", "Título", "Status")
        self.tree = ttk.Treeview(frame_listar, columns=colunas, show="headings", height=12)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Título", width=300, anchor="w")
        self.tree.column("Status", width=120, anchor="center") 
        self.tree.bind("<Double-1>", self.mostrar_descricao)

        self.tree.pack(pady=10, padx=20, fill="x")
        ttk.Button(frame_listar, text="Atualizar", command=self.atualizar_lista).pack(pady=10)
        self.frames["listar"] = frame_listar

        frame_alterar = tk.Frame(self.conteudo, bg="#ecf0f1")
        tk.Label(frame_alterar, text="Alterar Status", font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=20)

        form_alt = tk.Frame(frame_alterar, bg="#ecf0f1")
        form_alt.pack(pady=10)

        tk.Label(form_alt, text="ID do Chamado:", bg="#ecf0f1").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_id = tk.Entry(form_alt, width=10)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_alt, text="Novo Status:", bg="#ecf0f1").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.combo_status = ttk.Combobox(form_alt,values=["Aberto", "Em Andamento", "Fechado"], state="readonly", width=20)
        self.combo_status.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_alterar, text="Alterar", command=self.alterar_status).pack(pady=20)
        self.frames["alterar"] = frame_alterar

    def mostrar_descricao(self, event):
        item_selecionado = self.tree.focus()
        if item_selecionado:
            valores = self.tree.item(item_selecionado, 'values')
            id_chamado = int(valores[0])
            chamado = self.sistema.buscar(id_chamado)
            if chamado:
                desc_window = tk.Toplevel(self.principal)
                desc_window.title(f"Chamado {chamado.id} - Detalhes")
                desc_window.geometry("400x300")
                desc_window.resizable(False, False)
                desc_window.config(bg="#ecf0f1")

                tk.Label(desc_window, text=f"Chamado {chamado.id}", font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)

                tk.Label(desc_window, text=f"{chamado.titulo}", font=("Arial", 12), bg="#ecf0f1", wraplength=380, justify="left").pack(pady=5)

                tk.Label(desc_window, text="Descrição:", font=("Arial", 12, "bold"), bg="#ecf0f1").pack(pady=5)

                text_box = tk.Text(desc_window, wrap="word", height=10, width=40)
                text_box.pack(padx=10, pady=5, fill="both", expand=True)
                text_box.insert("1.0", chamado.motivo)
                text_box.config(state="disabled")

                ttk.Button(desc_window, text="Fechar", command=desc_window.destroy).pack(pady=10)

            else:
                messagebox.showerror("Erro", "Chamado não encontrado.")

    def mostrar_frame(self, nome):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[nome].pack(expand=True, fill="both")

    def salvar(self):
        titulo = self.entry_titulo.get()
        motivo = self.entry_motivo.get()
        if titulo and motivo:
            chamado = self.sistema.abrir(titulo, motivo)
            messagebox.showinfo("Sucesso", f"Chamado {chamado.id} aberto")
            self.entry_titulo.delete(0, tk.END)
            self.entry_motivo.delete(0, tk.END)
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos")

    def atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        chamados = self.sistema.listar()
        if chamados:
            for c in chamados:
                self.tree.insert("", "end", values=(c.id, c.titulo, c.status))
        else:
            messagebox.showinfo("Aviso", "Nenhum chamado cadastrado.")

    def alterar_status(self):
        try:
            id_chamado = int(self.entry_id.get())
            chamado = self.sistema.buscar(id_chamado)
            if chamado:
                novo_status = self.combo_status.get()
                if novo_status:
                    chamado.alterar_status(novo_status)
                    messagebox.showinfo("Sucesso", f"Chamado {id_chamado} atualizado para {novo_status}")
                    self.atualizar_lista()
                else:
                    messagebox.showwarning("Erro", "Selecione um status.")
            else:
                messagebox.showerror("Erro", "Chamado não encontrado.")
        except ValueError:
            messagebox.showwarning("Erro", "ID inválido.")

    def confirmar_sair(self):
        resposta = messagebox.askyesno("confirmar saída", "Tem certeza que deseja sair?")
        if resposta:
            self.principal.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ITsolutions(root)
    root.mainloop()