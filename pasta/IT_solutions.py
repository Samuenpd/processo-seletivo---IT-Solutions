import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import requests

def baixar_imagem(url, nome_arquivo):
    if not os.path.exists("imagens"):
        os.makedirs("imagens")

    caminho = os.path.join("imagens", nome_arquivo)

    if os.path.exists(caminho):
        return caminho

    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(caminho, "wb") as f:
                f.write(r.content)
            print(f"Sucesso! Imagem salva em: {caminho}")
            return caminho
        else:
            print(f"Erro: Imagem não baixada. Status code: {r.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao baixar a imagem: {e}")
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
    
    def remover(self, id_chamado):
        chamado = self.buscar(id_chamado)
        if chamado:
            self.chamados.remove(chamado)
            return True
        return False

class ITsolutions:
    def __init__(self, principal):
        self.sistema = Sistema()
        self.principal = principal
        self.principal.title("IT Solutions - Sistema de Chamados")
        self.principal.geometry("950x600")
        self.principal.protocol("WM_DELETE_WINDOW", self.confirmar_sair)
        
        self.original_user_img = None 
        
        url = "https://raw.githubusercontent.com/Samuenpd/processo-seletivo---IT-Solutions/refs/heads/main/user.png"
        caminho_img = baixar_imagem(url, "user.png")

        if caminho_img:
            try:
                self.original_user_img = Image.open(caminho_img).convert("RGBA").resize((80, 80))
            except Exception as e:
                print(f"Erro ao processar a imagem: {e}")
        
        self.criar_widgets()
        self.criar_frames()

        self.aplicar_modo("claro") 
        self.mostrar_frame("painel")
        self.janela_descricao = None

    def criar_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")

        self.top_frame = tk.Frame(self.principal, height=60)
        self.top_frame.pack(side="top", fill="x")
        self.label_titulo_app = tk.Label(self.top_frame, text="  IT Solutions - Sistema de Chamados",
                                         font=("Arial", 18, "bold"))
        self.label_titulo_app.pack(pady=10)

        self.menu_frame = tk.Frame(self.principal, width=200)
        self.menu_frame.pack(side="left", fill="y")
        
        self.user_label = tk.Label(self.menu_frame)
        if self.original_user_img:
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
        ttk.Button(self.menu_frame, text="Editar Chamado",
                   command=lambda: self.mostrar_frame("editar")).pack(pady=10, fill="x")
        ttk.Button(self.menu_frame, text="Excluir Chamado",
                   command=lambda: self.mostrar_frame("excluir")).pack(pady=10, fill="x")
        ttk.Button(self.menu_frame, text="Sair",
                   command=self.confirmar_sair).pack(pady=20, fill="x")

        self.conteudo = tk.Frame(self.principal)
        self.conteudo.pack(side="right", expand=True, fill="both")

    def criar_frames(self):
        self.frames = {}
        painel = tk.Frame(self.conteudo)
        self.label_painel_titulo = tk.Label(painel, text="📊 Painel", font=("Arial", 20, "bold"))
        self.label_painel_titulo.pack(pady=20)
        cards_frame = tk.Frame(painel)
        cards_frame.pack(pady=10)
        self.card_abertos = tk.Label(cards_frame, text="Abertos: 0", fg="white", font=("Arial", 14, "bold"), width=20, height=4)
        self.card_abertos.grid(row=0, column=0, padx=15)
        self.card_andamento = tk.Label(cards_frame, text="Em Andamento: 0", fg="white", font=("Arial", 14, "bold"), width=20, height=4)
        self.card_andamento.grid(row=0, column=1, padx=15)
        self.card_fechados = tk.Label(cards_frame, text="Fechados: 0", fg="white", font=("Arial", 14, "bold"), width=20, height=4)
        self.card_fechados.grid(row=0, column=2, padx=15)
        self.frames["painel"] = painel

        frame_abrir = tk.Frame(self.conteudo)
        tk.Label(frame_abrir, text="Novo Chamado", font=("Arial", 18, "bold")).pack(pady=20)
        form = tk.Frame(frame_abrir)
        form.pack(pady=10)
        tk.Label(form, text="Título:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_titulo = tk.Entry(form, width=50)
        self.entry_titulo.grid(row=0, column=1, padx=3, pady=5)
        tk.Label(form, text="Descrição:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_motivo = tk.Text(form, width=50, height=6)
        self.entry_motivo.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame_abrir, text="Salvar", command=self.salvar).pack(pady=20)
        self.frames["abrir"] = frame_abrir

        # Frame: Listar Chamados
        frame_listar = tk.Frame(self.conteudo)
        tk.Label(frame_listar, text="Lista de Chamados", font=("Arial", 18, "bold")).pack(pady=20)
        colunas = ("ID", "Título", "Status")
        self.tree = ttk.Treeview(frame_listar, columns=colunas, show="headings", height=15)
        self.tree.heading("ID", text="ID"); self.tree.heading("Título", text="Título"); self.tree.heading("Status", text="Status")
        self.tree.column("ID", width=50, anchor="center"); self.tree.column("Título", width=400, anchor="w"); self.tree.column("Status", width=150, anchor="center")
        self.tree.bind("<Double-1>", self.mostrar_descricao)
        self.tree.pack(pady=10, padx=20, fill="x")
        tk.Label(frame_listar, text="#Clique duas vezes para ver a descrição", font=("Arial", 10), fg="#808080").pack(pady=0)
        self.frames["listar"] = frame_listar

        frame_alterar = tk.Frame(self.conteudo)
        tk.Label(frame_alterar, text="Alterar Status", font=("Arial", 18, "bold")).pack(pady=20)
        form_alt = tk.Frame(frame_alterar)
        form_alt.pack(pady=10)
        tk.Label(form_alt, text="ID do Chamado:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_id = tk.Entry(form_alt, width=10)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_alt, text="Novo Status:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.combo_status = ttk.Combobox(form_alt, values=["Aberto", "Em Andamento", "Fechado"], state="readonly", width=20)
        self.combo_status.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame_alterar, text="Alterar", command=self.alterar_status).pack(pady=20)
        self.frames["alterar"] = frame_alterar

        frame_editar = tk.Frame(self.conteudo)
        tk.Label(frame_editar, text="Editar Chamado", font=("Arial", 18, "bold")).pack(pady=20)
        form_buscar_ed = tk.Frame(frame_editar)
        form_buscar_ed.pack(pady=5)
        tk.Label(form_buscar_ed, text="ID do Chamado:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id_edit_busca = tk.Entry(form_buscar_ed, width=10)
        self.entry_id_edit_busca.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(form_buscar_ed, text="Carregar Chamado", command=self.carregar_chamado_para_edicao).grid(row=0, column=2, padx=5)

        form_editar = tk.Frame(frame_editar)
        form_editar.pack(pady=10)
        tk.Label(form_editar, text="Título:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_titulo_edit = tk.Entry(form_editar, width=50, state="disabled")
        self.entry_titulo_edit.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(form_editar, text="Descrição:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_desc_edit = tk.Text(form_editar, width=50, height=6, state="disabled")
        self.entry_desc_edit.grid(row=2, column=1, padx=5, pady=5)
        
        self.btn_salvar_edicao = ttk.Button(frame_editar, text="Salvar Alterações", command=self.salvar_edicao, state="disabled")
        self.btn_salvar_edicao.pack(pady=20)
        self.frames["editar"] = frame_editar

        frame_excluir = tk.Frame(self.conteudo)
        tk.Label(frame_excluir, text="Excluir Chamado", font=("Arial", 18, "bold")).pack(pady=20)
        form_excluir = tk.Frame(frame_excluir)
        form_excluir.pack(pady=10)
        tk.Label(form_excluir, text="ID do Chamado:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id_excluir = tk.Entry(form_excluir, width=10)
        self.entry_id_excluir.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_excluir, text="Excluir", command=self.excluir_chamado).pack(pady=20)
        self.frames["excluir"] = frame_excluir
        
        frame_perfil = tk.Frame(self.conteudo)
        tk.Label(frame_perfil, text="Perfil do Usuário", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(frame_perfil, text="Nome: Usuário Padrão", font=("Arial", 14)).pack(pady=5)
        tk.Label(frame_perfil, text="Email: usuario@gmail.com", font=("Arial", 14)).pack(pady=5)
        tk.Label(frame_perfil, text="Cargo: Analista de TI", font=("Arial", 14)).pack(pady=5)
        ttk.Button(frame_perfil, text="Modo Escuro", command=lambda: self.aplicar_modo("escuro")).pack(pady=10, fill="x", padx=150)
        ttk.Button(frame_perfil, text="Modo Claro", command=lambda: self.aplicar_modo("claro")).pack(pady=10, fill="x", padx=150)
        self.frames["perfil"] = frame_perfil
    
    def mostrar_frame(self, nome):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[nome].pack(expand=True, fill="both")
        if nome == 'listar' or nome == 'painel':
            self.atualizar_lista()
        if nome == 'editar':
            self.limpar_campos_edicao()
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
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos")

    def atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, c in enumerate(self.sistema.listar()):
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
            novo_status = self.combo_status.get()
            chamado = self.sistema.buscar(id_chamado)
            if chamado and novo_status:
                chamado.alterar_status(novo_status)
                messagebox.showinfo("Sucesso", f"Chamado {id_chamado} atualizado para {novo_status}")
                self.atualizar_lista()
                self.entry_id.delete(0, tk.END)
                self.combo_status.set('')
            elif not chamado:
                messagebox.showerror("Erro", "Chamado não encontrado.")
            else:
                messagebox.showwarning("Erro", "Selecione um status.")
        except ValueError:
            messagebox.showwarning("Erro", "O ID do chamado deve ser um número.")
    
    def carregar_chamado_para_edicao(self):
        try:
            id_chamado = int(self.entry_id_edit_busca.get())
            chamado = self.sistema.buscar(id_chamado)
            if chamado:
                self.entry_titulo_edit.config(state="normal")
                self.entry_desc_edit.config(state="normal")
                self.btn_salvar_edicao.config(state="normal")
                
                self.entry_titulo_edit.delete(0, tk.END)
                self.entry_titulo_edit.insert(0, chamado.titulo)
                self.entry_desc_edit.delete("1.0", tk.END)
                self.entry_desc_edit.insert("1.0", chamado.motivo)
            else:
                messagebox.showerror("Erro", "Chamado não encontrado.")
                self.limpar_campos_edicao()
        except ValueError:
            messagebox.showwarning("Erro", "O ID deve ser um número.")
            self.limpar_campos_edicao()
            
    def salvar_edicao(self):
        try:
            id_chamado = int(self.entry_id_edit_busca.get())
            chamado = self.sistema.buscar(id_chamado)
            if chamado:
                novo_titulo = self.entry_titulo_edit.get().strip()
                nova_descricao = self.entry_desc_edit.get("1.0", tk.END).strip()
                if not novo_titulo or not nova_descricao:
                    messagebox.showwarning("Erro", "Título e descrição não podem estar vazios.")
                    return
                chamado.titulo = novo_titulo
                chamado.motivo = nova_descricao
                messagebox.showinfo("Sucesso", f"Chamado {id_chamado} editado com sucesso.")
                self.atualizar_lista()
                self.limpar_campos_edicao()
            else:
                messagebox.showerror("Erro", "Chamado não encontrado.")
        except ValueError:
            messagebox.showwarning("Erro", "O ID deve ser um número.")

    def excluir_chamado(self):
        try:
            id_chamado = int(self.entry_id_excluir.get())
            if not self.sistema.buscar(id_chamado):
                 messagebox.showerror("Erro", "Chamado não encontrado.")
                 return
            
            if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o chamado {id_chamado}? Esta ação não pode ser desfeita."):
                if self.sistema.remover(id_chamado):
                    messagebox.showinfo("Sucesso", f"Chamado {id_chamado} excluído com sucesso.")
                    self.entry_id_excluir.delete(0, tk.END)
                    self.atualizar_lista()
        except ValueError:
            messagebox.showwarning("Erro", "O ID deve ser um número.")
    
    def limpar_campos_edicao(self):
        self.entry_id_edit_busca.delete(0, tk.END)
        self.entry_titulo_edit.delete(0, tk.END)
        self.entry_desc_edit.delete("1.0", tk.END)
        self.entry_titulo_edit.config(state="disabled")
        self.entry_desc_edit.config(state="disabled")
        self.btn_salvar_edicao.config(state="disabled")

    # -----------------------------------------------

    def mostrar_descricao(self, event):
        if self.janela_descricao and self.janela_descricao.winfo_exists():
            self.janela_descricao.lift()
            return
        
        item_selecionado = self.tree.focus()
        if not item_selecionado: return

        id_chamado = int(self.tree.item(item_selecionado, 'values')[0])
        chamado = self.sistema.buscar(id_chamado)
        if chamado:
            self.janela_descricao = tk.Toplevel(self.principal)
            self.janela_descricao.title(f"Chamado {chamado.id} - Detalhes")
            self.janela_descricao.geometry("500x350")
            self.janela_descricao.resizable(False, False)
            
            bg_color = self.principal.cget("bg")
            fg_color = self.fg_color_atual
            widget_bg = self.entry_titulo.cget("bg")

            self.janela_descricao.config(bg=bg_color)
            tk.Label(self.janela_descricao, text=f"Chamado {chamado.id}", font=("Arial", 16, "bold"), bg=bg_color, fg=fg_color).pack(pady=10)
            tk.Label(self.janela_descricao, text=f"{chamado.titulo}", font=("Arial", 12), bg=bg_color, fg=fg_color, wraplength=480, justify="left").pack(pady=5)
            tk.Label(self.janela_descricao, text="Descrição:", font=("Arial", 12, "bold"), bg=bg_color, fg=fg_color).pack(pady=5)

            text_box = tk.Text(self.janela_descricao, wrap="word", height=10, width=58, bg=widget_bg, fg=fg_color, relief="solid", bd=1)
            text_box.pack(padx=10, pady=5, fill="both", expand=True)
            text_box.insert("1.0", chamado.motivo)
            text_box.config(state="disabled")

            ttk.Button(self.janela_descricao, text="Fechar", command=self.janela_descricao.destroy).pack(pady=10)
            self.janela_descricao.protocol("WM_DELETE_WINDOW", self.fechar_janela_descricao)
        else:
            messagebox.showerror("Erro", "Chamado não encontrado.")

    def fechar_janela_descricao (self):
        if self.janela_descricao:
            self.janela_descricao.destroy()
            self.janela_descricao = None

    def aplicar_modo(self, modo):
        if modo == "escuro":
            cores = {
                "bg_principal": "#2E2E3E", "bg_top_menu": "#1E1E2E", "bg_widget": "#3B3B4A",
                "fg_texto": "#EAEAEA", "fg_titulo": "#FFFFFF", "fg_disabled": "#9E9E9E", "selecionado": "#4A4A5A",
                "card_aberto": "#c0392b", "card_andamento": "#d35400", "card_fechado": "#27ae60",
                "tree_odd": "#3B3B4A", "tree_even": "#2E2E3E", "btn_bg": "#4A4A5A", "btn_fg": "#FFFFFF", "btn_active": "#5A5A6A"
            }
        else:
            cores = {
                "bg_principal": "#ecf0f1", "bg_top_menu": "#2c3e50", "bg_widget": "#ffffff",
                "fg_texto": "#000000", "fg_titulo": "#000000", "fg_disabled": "#808080", "selecionado": "#a9cce3",
                "card_aberto": "#e74c3c", "card_andamento": "#f39c12", "card_fechado": "#27ae60",
                "tree_odd": "#f2f2f2", "tree_even": "#ffffff", "btn_bg": "#0f3842", "btn_fg": "#FFFFFF", "btn_active": "#2980b9"
            }

        self.principal.config(bg=cores["bg_principal"])
        self.top_frame.config(bg=cores["bg_top_menu"])
        self.menu_frame.config(bg=cores["bg_top_menu"])
        self.conteudo.config(bg=cores["bg_principal"])
        self.label_titulo_app.config(bg=cores["bg_top_menu"], fg="#FFFFFF")
        
        if self.original_user_img:
            r, g, b = tuple(int(cores["bg_top_menu"].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            bg_img = Image.new("RGBA", self.original_user_img.size, (r, g, b, 255))
            img_composta = Image.alpha_composite(bg_img, self.original_user_img).convert("RGB")
            
            self.user_icon = ImageTk.PhotoImage(img_composta)
            self.user_label.config(image=self.user_icon, bg=cores["bg_top_menu"])

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background=cores["btn_bg"], foreground=cores["btn_fg"], font=("Arial", 11), padding=6, borderwidth=0)
        style.map("TButton", background=[("active", cores["btn_active"])])
        
        style.configure("Treeview", background=cores["bg_widget"], fieldbackground=cores["bg_widget"], foreground=cores["fg_texto"], font=("Arial", 10), rowheight=24)
        style.map("Treeview", background=[("selected", cores["selecionado"])], foreground=[("selected", cores["fg_texto"])])
        self.tree.tag_configure("oddrow", background=cores["tree_odd"], foreground=cores["fg_texto"])
        self.tree.tag_configure("evenrow", background=cores["tree_even"], foreground=cores["fg_texto"])

        style.configure("TCombobox", fieldbackground=cores["bg_widget"], background=cores["btn_bg"], foreground=cores["fg_texto"], insertcolor=cores["fg_texto"], arrowcolor=cores["fg_texto"])
        style.map('TCombobox', fieldbackground=[('readonly', cores["bg_widget"])], foreground=[('readonly', cores["fg_texto"])])

        self.card_abertos.config(bg=cores["card_aberto"])
        self.card_andamento.config(bg=cores["card_andamento"])
        self.card_fechados.config(bg=cores["card_fechado"])
        
        def atualizar_widgets_tk(widget):
            for w in widget.winfo_children():
                widget_class = w.winfo_class()
                try:
                    if widget_class in ("Frame", "Labelframe"):
                        w.config(bg=cores["bg_principal"])
                        atualizar_widgets_tk(w)
                    elif widget_class == "Label":
                        is_title = "bold" in str(w.cget("font")).lower()
                        fg = cores["fg_titulo"] if is_title and modo == 'claro' else cores["fg_texto"]
                        if w not in [self.card_abertos, self.card_andamento, self.card_fechados]:
                           w.config(bg=cores["bg_principal"], fg=fg)
                    elif widget_class in ("Entry", "Text"):
                        w.config(
                            bg=cores["bg_widget"], 
                            fg=cores["fg_texto"], 
                            insertbackground=cores["fg_texto"], 
                            relief="solid", 
                            bd=1,
                            disabledbackground=cores["bg_widget"], 
                            disabledforeground=cores["fg_disabled"]
                        )
                except tk.TclError:
                    pass

        for frame in self.frames.values():
            frame.config(bg=cores["bg_principal"])
            atualizar_widgets_tk(frame)

        self.atualizar_lista()

        self.fg_color_atual = cores["fg_texto"] 
        
        def atualizar_widgets_tk(widget):
            for w in widget.winfo_children():
                widget_class = w.winfo_class()
                try:
                    if widget_class in ("Frame", "Labelframe"):
                        w.config(bg=cores["bg_principal"])
                        atualizar_widgets_tk(w)
                    elif widget_class == "Label":
                        is_title = "bold" in str(w.cget("font")).lower()
                        fg = cores["fg_titulo"] if is_title and modo == 'claro' else cores["fg_texto"]
                        if w not in [self.card_abertos, self.card_andamento, self.card_fechados]:
                           w.config(bg=cores["bg_principal"], fg=fg)
                    elif widget_class in ("Entry", "Text"):
                        w.config(bg=cores["bg_widget"], fg=cores["fg_texto"], insertbackground=cores["fg_texto"], relief="solid", bd=1)
                except tk.TclError:
                    pass

        for frame in self.frames.values():
            frame.config(bg=cores["bg_principal"])
            atualizar_widgets_tk(frame)

        self.atualizar_lista()

        self.fg_color_atual = cores["fg_texto"]

    def confirmar_sair(self):
        if messagebox.askyesno("Confirmar Saída", "Tem certeza que deseja sair?"):
            self.principal.destroy()

if __name__ == "__main__":
    principal = tk.Tk()
    app = ITsolutions(principal)
    principal.mainloop()
