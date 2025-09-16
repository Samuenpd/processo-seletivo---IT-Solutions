import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import requests

def baixar_imagem(url, nome_arquivo):
    if not os.path.exists("imagens"):
        os.makedirs("imagens")

    caminho = os.path.join("imagens", nome_arquivo)

    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(caminho, "wb") as f:
            f.write(r.content)
        print(f"Imagem salva em: {caminho}")
        return caminho
    else:
        print("Erro ao baixar imagem")
        return None

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
        self.principal.geometry("950x600")
        self.principal.config(bg="#34495e")
        self.principal.protocol("WM_DELETE_WINDOW", self.confirmar_sair)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 11), padding=6)
        style.configure("Treeview", font=("Arial", 10), rowheight=24)
        style.map("TButton", background=[("active", "#2980b9")])

        self.top_frame = tk.Frame(self.principal, height=60, bg="#2c3e50")
        self.top_frame.pack(side="top", fill="x")
        tk.Label(self.top_frame, text="  IT Solutions - Sistema de Chamados",
                 bg="#2c3e50", fg="white", font=("Arial", 18, "bold")).pack(pady=10)

        self.menu_frame = tk.Frame(principal, width=200, bg="#2c3e50")
        self.menu_frame.pack(side="left", fill="y")

        url = "https://raw.githubusercontent.com/Samuenpd/processo-seletivo---IT-Solutions/refs/heads/main/user.png"

        caminho_img = baixar_imagem(url, "user.png")

        if caminho_img:
            img = Image.open(caminho_img).convert("RGBA")

            bg_color = (44, 62, 80, 255)
            bg = Image.new("RGBA", img.size, bg_color)
            img = Image.alpha_composite(bg, img)
            img = img.resize((80, 80))
            img = img.convert("RGB")

            self.user_icon = ImageTk.PhotoImage(img)

            self.user_label = tk.Label(self.menu_frame, image=self.user_icon, bg="#2c3e50")
            self.user_label.pack(pady=20)

            self.user_label.bind("<Button-1>", lambda e: self.mostrar_frame("perfil"))

        ttk.Button(self.menu_frame, text="Painel",
                   command=lambda: self.mostrar_frame("painel")).pack(pady=10, fill="x")
        ttk.Button(self.menu_frame, text="Abrir Chamado",
                   command=lambda: self.mostrar_frame("abrir")).pack(pady=10, fill="x")
        ttk.Button(self.menu_frame, text="Listar Chamados",
                   command=lambda: self.mostrar_frame("listar")).pack(pady=10, fill="x")
        ttk.Button(self.menu_frame, text="Alterar Status",
                   command=lambda: self.mostrar_frame("alterar")).pack(pady=10, fill="x")
        ttk.Button(self.menu_frame, text="Sair",
                   command=self.confirmar_sair).pack(pady=20, fill="x")

        self.conteudo = tk.Frame(principal, bg="#ecf0f1")
        self.conteudo.pack(side="right", expand=True, fill="both")

        self.frames = {}
        self.criar_frames()
        self.mostrar_frame("painel")

    def criar_frames(self):
        # === PAINEL ===
        painel = tk.Frame(self.conteudo, bg="#ecf0f1")
        tk.Label(painel, text="📊 Painel", font=("Arial", 20, "bold"),
                 bg="#ecf0f1").pack(pady=20)

        self.cards_frame = tk.Frame(painel, bg="#ecf0f1")
        self.cards_frame.pack(pady=10)

        self.card_abertos = tk.Label(self.cards_frame, text="Abertos: 0",
                                     bg="#e74c3c", fg="white", font=("Arial", 14, "bold"),
                                     width=20, height=4)
        self.card_abertos.grid(row=0, column=0, padx=15)

        self.card_andamento = tk.Label(self.cards_frame, text="Em Andamento: 0",
                                       bg="#f39c12", fg="white", font=("Arial", 14, "bold"),
                                       width=20, height=4)
        self.card_andamento.grid(row=0, column=1, padx=15)

        self.card_fechados = tk.Label(self.cards_frame, text="Fechados: 0",
                                      bg="#27ae60", fg="white", font=("Arial", 14, "bold"),
                                      width=20, height=4)
        self.card_fechados.grid(row=0, column=2, padx=15)

        self.frames["painel"] = painel

        frame_abrir = tk.Frame(self.conteudo, bg="#ecf0f1")
        tk.Label(frame_abrir, text="Novo Chamado", font=("Arial", 18, "bold"),
                 bg="#ecf0f1").pack(pady=20)

        form = tk.Frame(frame_abrir, bg="#ecf0f1")
        form.pack(pady=10)

        tk.Label(form, text="Título:", bg="#ecf0f1").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_titulo = tk.Entry(form, width=50)
        self.entry_titulo.grid(row=0, column=1, padx=3, pady=5)

        tk.Label(form, text="Descrição:", bg="#ecf0f1").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_motivo = tk.Text(form, width=50, height=6)
        self.entry_motivo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_abrir, text="Salvar", command=self.salvar).pack(pady=20)
        self.frames["abrir"] = frame_abrir

        frame_listar = tk.Frame(self.conteudo, bg="#ecf0f1")
        tk.Label(frame_listar, text="Lista de Chamados", font=("Arial", 18, "bold"),
                 bg="#ecf0f1").pack(pady=20)

        colunas = ("ID", "Título", "Status")
        self.tree = ttk.Treeview(frame_listar, columns=colunas, show="headings", height=15)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Título", width=400, anchor="w")
        self.tree.column("Status", width=150, anchor="center")
        self.tree.bind("<Double-1>", self.mostrar_descricao)

        self.tree.tag_configure("oddrow", background="#f2f2f2")
        self.tree.tag_configure("evenrow", background="white")

        self.tree.pack(pady=10, padx=20, fill="x")
        
        tk.Label(frame_listar, text="#aperte duas vezes para obter descrição", font=("Arial", 10),
                 bg="#ecf0f1", fg="#808080" ).pack(pady=0)
        
        self.frames["listar"] = frame_listar

        frame_alterar = tk.Frame(self.conteudo, bg="#ecf0f1")
        tk.Label(frame_alterar, text="Alterar Status", font=("Arial", 18, "bold"),
                 bg="#ecf0f1").pack(pady=20)

        form_alt = tk.Frame(frame_alterar, bg="#ecf0f1")
        form_alt.pack(pady=10)

        tk.Label(form_alt, text="ID do Chamado:", bg="#ecf0f1").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_id = tk.Entry(form_alt, width=10)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_alt, text="Novo Status:", bg="#ecf0f1").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.combo_status = ttk.Combobox(form_alt, values=["Aberto", "Em Andamento", "Fechado"],
                                         state="readonly", width=20)
        self.combo_status.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_alterar, text="Alterar", command=self.alterar_status).pack(pady=20)
        self.frames["alterar"] = frame_alterar

        frame_perfil = tk.Frame(self.conteudo, bg="#ecf0f1")
        tk.Label(frame_perfil, text="Perfil do Usuário", font=("Arial", 18, "bold"),
                 bg="#ecf0f1").pack(pady=20)

        tk.Label(frame_perfil, text="Nome: Usuário Padrão", font=("Arial", 14),
                 bg="#ecf0f1").pack(pady=5)
        tk.Label(frame_perfil, text="Email: usuario@gmail.com", font=("Arial", 14),
                 bg="#ecf0f1").pack(pady=5)
        tk.Label(frame_perfil, text="Cargo: Analista de TI", font=("Arial", 14),
                 bg="#ecf0f1").pack(pady=5)

        self.frames["perfil"] = frame_perfil

    def mostrar_descricao(self, event):
        item_selecionado = self.tree.focus()
        if item_selecionado:
            valores = self.tree.item(item_selecionado, 'values')
            id_chamado = int(valores[0])
            chamado = self.sistema.buscar(id_chamado)
            if chamado:
                desc_window = tk.Toplevel(self.principal)
                desc_window.title(f"Chamado {chamado.id} - Detalhes")
                desc_window.geometry("500x350")
                desc_window.config(bg="#ecf0f1")
                desc_window.resizable(False, False)

                tk.Label(desc_window, text=f"Chamado {chamado.id}",
                         font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)

                tk.Label(desc_window, text=f"{chamado.titulo}",
                         font=("Arial", 12), bg="#ecf0f1", wraplength=480,
                         justify="left").pack(pady=5)

                tk.Label(desc_window, text="Descrição:",
                         font=("Arial", 12, "bold"), bg="#ecf0f1").pack(pady=5)

                text_box = tk.Text(desc_window, wrap="word", height=10, width=58)
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
        self.atualizar_painel()

    def salvar(self):
        titulo = self.entry_titulo.get()
        motivo = self.entry_motivo.get("1.0", tk.END).strip()
        if titulo and motivo:
            chamado = self.sistema.abrir(titulo, motivo)
            messagebox.showinfo("Sucesso", f"Chamado {chamado.id} aberto")
            self.entry_titulo.delete(0, tk.END)
            self.entry_motivo.delete("1.0", tk.END)
            self.atualizar_lista()
            self.atualizar_painel()
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos")

    def atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        chamados = self.sistema.listar()
        if chamados:
            for i, c in enumerate(chamados):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=(c.id, c.titulo, c.status), tags=(tag,))
        self.atualizar_painel()

    def atualizar_painel(self):
        abertos = len([c for c in self.sistema.chamados if c.status == "Aberto"])
        andamento = len([c for c in self.sistema.chamados if c.status == "Em Andamento"])
        fechados = len([c for c in self.sistema.chamados if c.status == "Fechado"])

        self.card_abertos.config(text=f"Abertos: {abertos}")
        self.card_andamento.config(text=f"Em Andamento: {andamento}")
        self.card_fechados.config(text=f"Fechados: {fechados}")

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
                    self.atualizar_painel()
                else:
                    messagebox.showwarning("Erro", "Selecione um status.")
            else:
                messagebox.showerror("Erro", "Chamado não encontrado.")
        except ValueError:
            messagebox.showwarning("Erro", "ID inválido.")

    def confirmar_sair(self):
        resposta = messagebox.askyesno("Confirmar saída", "Tem certeza que deseja sair?")
        if resposta:
            self.principal.destroy()

if __name__ == "__main__":
    principal = tk.Tk()
    app = ITsolutions(principal)
    principal.mainloop()