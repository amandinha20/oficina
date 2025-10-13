import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Conexão e criação do banco de dados (DER implementado)
def criar_banco():
    conn = sqlite3.connect('oficina.db')
    cursor = conn.cursor()
    # Tabela Cliente
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            cpf VARCHAR(11) NOT NULL UNIQUE,
            telefone VARCHAR(15),
            endereco TEXT
        )
    ''')
    # Tabela Veiculo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS veiculo (
            id_veiculo INTEGER PRIMARY KEY AUTOINCREMENT,
            placa VARCHAR(8) NOT NULL UNIQUE,
            modelo VARCHAR(50) NOT NULL,
            ano INTEGER NOT NULL,
            cor VARCHAR(30),
            quilometragem INTEGER,
            id_cliente INTEGER NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente) ON DELETE CASCADE
        )
    ''')
    # Tabela Servico
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servico (
            id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(50) NOT NULL UNIQUE,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL CHECK (preco > 0)
        )
    ''')
    conn.commit()
    conn.close()

# Funções de validação
def cpf_valido(cpf):
    return len(cpf) == 11 and cpf.isdigit()

def placa_valida(placa):
    return len(placa) == 8 and placa[3] == '-' and placa[:3].isalpha() and placa[4:].isdigit()

def ano_valido(ano_str):
    try:
        ano = int(ano_str)
        return 1900 <= ano <= datetime.now().year
    except ValueError:
        return False

def preco_valido(preco_str):
    try:
        return float(preco_str) > 0
    except ValueError:
        return False

def telefone_valido(tel):
    cleaned = ''.join(filter(str.isdigit, tel))
    return len(cleaned) >= 10

def quilometragem_valida(qm_str):
    if qm_str == '':
        return True
    try:
        return int(qm_str) >= 0
    except ValueError:
        return False

# Classe base para CRUD
class CRUDWindow:
    def __init__(self, parent, titulo, campos, tabela, colunas_lista, validadores=None, campos_obrigatorios=None, pk_field='id'):
        self.parent = parent
        self.titulo = titulo
        self.campos = campos  # Dict: nome_campo -> label
        self.tabela = tabela
        self.colunas_lista = colunas_lista
        self.validadores = validadores or {}
        self.campos_obrigatorios = campos_obrigatorios or list(campos.keys())
        self.pk_field = pk_field
        self.janela = tk.Toplevel(parent)
        self.janela.title(titulo)
        self.janela.geometry("700x600")
        self.tree = None
        self.conn = sqlite3.connect('oficina.db')
        self.carregar_lista()
        self.criar_interface()

    def criar_interface(self):
        # Frame para lista
        frame_lista = tk.Frame(self.janela)
        frame_lista.pack(pady=10, fill=tk.BOTH, expand=True)
        tk.Label(frame_lista, text=f"Lista de {self.titulo}").pack()
        self.tree = ttk.Treeview(frame_lista, columns=self.colunas_lista, show='headings')
        for col in self.colunas_lista:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botões
        btn_frame = tk.Frame(self.janela)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Inserir", command=self.inserir).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Editar", command=self.editar).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Excluir", command=self.excluir).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Fechar", command=self.janela.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Entry para busca
        search_frame = tk.Frame(self.janela)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
        self.entry_busca = tk.Entry(search_frame, width=20)
        self.entry_busca.pack(side=tk.LEFT, padx=5)
        self.entry_busca.bind('<Return>', lambda e: self.buscar())
        tk.Button(search_frame, text="Buscar", command=self.buscar).pack(side=tk.LEFT, padx=5)

    def carregar_lista(self, where_clause=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        cursor = self.conn.cursor()
        query = f"SELECT * FROM {self.tabela} {where_clause}"
        rows = cursor.execute(query).fetchall()
        for row in rows:
            self.tree.insert('', 'end', values=row)
        cursor.close()

    def inserir(self):
        self.criar_formulario("Inserir")

    def editar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um registro para editar.")
            return
        item = self.tree.item(selected[0])
        values = item['values']
        self.criar_formulario("Editar", values)

    def excluir(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um registro para excluir.")
            return
        if messagebox.askyesno("Confirmação", f"Excluir este {self.titulo.lower()}?"):
            values = self.tree.item(selected[0])['values']
            id_reg = values[0]
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {self.tabela} WHERE {self.pk_field} = ?", (id_reg,))
            self.conn.commit()
            cursor.close()
            self.carregar_lista()
            messagebox.showinfo("Sucesso", f"{self.titulo} excluído com sucesso.")

    def buscar(self):
        termo = self.entry_busca.get().strip()
        if not termo:
            self.carregar_lista()
            return
        campo_busca = self.colunas_lista[1]  # Nome/Placa/Nome
        self.carregar_lista(f"WHERE {campo_busca} LIKE '%{termo}%'")

    def validar_dados(self, dados):
        erros = []
        for i, campo in enumerate(self.campos.keys()):
            valor = dados[i].strip()
            if campo in self.campos_obrigatorios and not valor:
                erros.append(f"{self.campos[campo]} é obrigatório.")
            if campo in self.validadores and valor and not self.validadores[campo](valor):
                erros.append(f"{self.campos[campo]} inválido.")
        if erros:
            messagebox.showerror("Validação", "\n".join(erros))
            return False
        return True

    def criar_formulario(self, acao, valores=None):
        form = tk.Toplevel(self.janela)
        form.title(f"{acao} {self.titulo}")
        form.geometry("400x500")
        entries = {}
        row = 0
        for campo, label in self.campos.items():
            tk.Label(form, text=label).grid(row=row, column=0, sticky='w', padx=10, pady=5)
            entry = tk.Entry(form, width=30)
            entry.grid(row=row, column=1, padx=10, pady=5)
            if valores and row < len(valores) - 1:
                entry.insert(0, valores[row + 1])
            entries[campo] = entry
            row += 1
        
        def salvar():
            dados = [entries[campo].get().strip() for campo in self.campos.keys()]
            if not self.validar_dados(dados):
                return
            cursor = self.conn.cursor()
            try:
                if acao == "Inserir":
                    placeholders = ', '.join(['?' for _ in dados])
                    campos_str = ', '.join(self.campos.keys())
                    query = f"INSERT INTO {self.tabela} ({campos_str}) VALUES ({placeholders})"
                    cursor.execute(query, dados)
                else:  # Editar
                    id_reg = valores[0]
                    set_clause = ', '.join([f"{c} = ?" for c in self.campos.keys()])
                    query = f"UPDATE {self.tabela} SET {set_clause} WHERE {self.pk_field} = ?"
                    dados.append(id_reg)
                    cursor.execute(query, dados)
                self.conn.commit()
                messagebox.showinfo("Sucesso", f"{acao} com sucesso.")
                form.destroy()
                self.carregar_lista()
            except sqlite3.IntegrityError as e:
                messagebox.showerror("Erro", f"Dados duplicados ou inválidos (ex: CPF/placa/nome único).")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")
            finally:
                cursor.close()

        tk.Button(form, text="Salvar", command=salvar).grid(row=row, column=0, columnspan=2, pady=20)

# CRUD Específico para Cliente
class ClienteCRUD(CRUDWindow):
    def __init__(self, parent):
        campos = {
            'nome': 'Nome Completo (obrigatório)',
            'cpf': 'CPF (11 dígitos, único)',
            'telefone': 'Telefone (ex: (11)99999-9999)',
            'endereco': 'Endereço (opcional)'
        }
        validadores = {
            'cpf': cpf_valido,
            'telefone': telefone_valido
        }
        campos_obrigatorios = ['nome', 'cpf']
        super().__init__(parent, "Clientes", campos, "cliente", 
                        ['ID_Cliente', 'Nome', 'CPF', 'Telefone', 'Endereço'], 
                        validadores, campos_obrigatorios, 'id_cliente')

# CRUD Específico para Veiculo (com dropdown de clientes)
class VeiculoCRUD(CRUDWindow):
    def __init__(self, parent):
        self.clientes = self.carregar_clientes()
        campos = {
            'placa': 'Placa (AAA-0000, único)',
            'modelo': 'Modelo (obrigatório)',
            'ano': 'Ano de Fabricação (1900-atual)',
            'cor': 'Cor (opcional)',
            'quilometragem': 'Quilometragem Atual (opcional)',
            'id_cliente': 'Proprietário (selecione cliente)'
        }
        validadores = {
            'placa': placa_valida,
            'ano': ano_valido,
            'quilometragem': quilometragem_valida
        }
        campos_obrigatorios = ['placa', 'modelo', 'ano', 'id_cliente']
        super().__init__(parent, "Veículos", campos, "veiculo", 
                        ['ID_Veiculo', 'Placa', 'Modelo', 'Ano', 'Cor', 'Quilometragem', 'ID_Cliente'], 
                        validadores, campos_obrigatorios, 'id_veiculo')
        # Override para usar dropdown em id_cliente
        self.criar_formulario = self.criar_formulario_override

    def carregar_clientes(self):
        conn = sqlite3.connect('oficina.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nome FROM cliente ORDER BY nome")
        clientes = cursor.fetchall()
        conn.close()
        return clientes

    def criar_formulario_override(self, acao, valores=None):
        form = tk.Toplevel(self.janela)
        form.title(f"{acao} Veículo")
        form.geometry("450x550")
        entries = {}
        row = 0
        # Campos até cor
        for campo, label in list(self.campos.items())[:4]:  # placa, modelo, ano, cor
            tk.Label(form, text=label).grid(row=row, column=0, sticky='w', padx=10, pady=5)
            entry = tk.Entry(form, width=30)
            entry.grid(row=row, column=1, padx=10, pady=5)
            if valores and row < 4:
                entry.insert(0, valores[row + 1])
            entries[campo] = entry
            row += 1
        
        # Quilometragem
        tk.Label(form, text=self.campos['quilometragem']).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        entry_km = tk.Entry(form, width=30)
        entry_km.grid(row=row, column=1, padx=10, pady=5)
        if valores:
            entry_km.insert(0, valores[5])
        entries['quilometragem'] = entry_km
        row += 1
        
        # Dropdown para cliente
        tk.Label(form, text=self.campos['id_cliente']).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        cliente_values = [f"{id_c}: {nome}" for id_c, nome in self.clientes]
        self.combo_cliente = ttk.Combobox(form, values=cliente_values, width=27, state="readonly")
        self.combo_cliente.grid(row=row, column=1, padx=10, pady=5)
        if valores and self.clientes:
            # Encontra o cliente correspondente
            id_c = valores[-1]
            nome_c = next((nome for idd, nome in self.clientes if idd == id_c), "")
            self.combo_cliente.set(f"{id_c}: {nome_c}")
        row += 1
        
        def salvar():
            dados = [entries[campo].get().strip() for campo in list(self.campos.keys())[:-1]]  # Sem id_cliente
            id_cliente = extrair_id_cliente()
            if id_cliente is None:
                return
            dados.append(id_cliente)
            if not self.validar_dados(dados):
                return
            cursor = self.conn.cursor()
            try:
                if acao == "Inserir":
                    placeholders = ', '.join(['?' for _ in dados])
                    campos_str = ', '.join(self.campos.keys())
                    query = f"INSERT INTO {self.tabela} ({campos_str}) VALUES ({placeholders})"
                    cursor.execute(query, dados)
                else:
                    id_reg = valores[0]
                    set_clause = ', '.join([f"{c} = ?" for c in self.campos.keys()])
                    query = f"UPDATE {self.tabela} SET {set_clause} WHERE {self.pk_field} = ?"
                    dados.append(id_reg)
                    cursor.execute(query, dados)
                self.conn.commit()
                messagebox.showinfo("Sucesso", f"{acao} com sucesso.")
                form.destroy()
                self.carregar_lista()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Placa já existe ou cliente inválido.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")
            finally:
                cursor.close()

        def extrair_id_cliente():
            sel = self.combo_cliente.get()
            if not sel:
                messagebox.showerror("Erro", "Selecione um cliente.")
                return None
            try:
                return int(sel.split(':')[0].strip())
            except Exception:
                messagebox.showerror("Erro", "Cliente inválido.")
                return None

        tk.Button(form, text="Salvar", command=salvar).grid(row=row, column=0, columnspan=2, pady=20)

if __name__ == "__main__":
    criar_banco()
    root = tk.Tk()
    root.title("Sistema de Oficina de Carros")
    root.geometry("400x300")

    def abrir_clientes():
        ClienteCRUD(root)

    def abrir_veiculos():
        VeiculoCRUD(root)

    btn_clientes = tk.Button(root, text="Gerenciar Clientes", command=abrir_clientes, width=25)
    btn_clientes.pack(pady=20)
    btn_veiculos = tk.Button(root, text="Gerenciar Veículos", command=abrir_veiculos, width=25)
    btn_veiculos.pack(pady=20)

    root.mainloop()

