import sqlite3
import tkinter as tk
from tkinter import messagebox, Toplevel

# Conectando ao banco de dados e criando tabela, se não existir
def initialize_db():
    conn = sqlite3.connect("notas.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nota1 REAL NOT NULL,
        nota2 REAL NOT NULL,
        media REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Função para adicionar média ao banco de dados
def adicionar_media():
    def salvar_media():
        nome = entry_nome.get().strip()
        try:
            nota1 = float(entry_nota1.get().strip())
            nota2 = float(entry_nota2.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "As notas devem ser números.")
            return

        if not nome or entry_nota1.get() == "" or entry_nota2.get() == "":
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        media = (nota1 + nota2) / 2

        conn = sqlite3.connect("notas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alunos (nome, nota1, nota2, media) VALUES (?, ?, ?, ?)", (nome, nota1, nota2, media))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Média adicionada com sucesso!")
        janela_adicionar.destroy()

    # Criando janela para adicionar média
    janela_adicionar = Toplevel()
    janela_adicionar.title("Adicionar Média")
    janela_adicionar.geometry("300x200")

    tk.Label(janela_adicionar, text="Nome do Aluno:").pack(pady=5)
    entry_nome = tk.Entry(janela_adicionar)
    entry_nome.pack()

    tk.Label(janela_adicionar, text="Nota 1:").pack(pady=5)
    entry_nota1 = tk.Entry(janela_adicionar)
    entry_nota1.pack()

    tk.Label(janela_adicionar, text="Nota 2:").pack(pady=5)
    entry_nota2 = tk.Entry(janela_adicionar)
    entry_nota2.pack()

    tk.Button(janela_adicionar, text="Salvar", command=salvar_media).pack(pady=10)

# Função para exibir o histórico de médias
def ver_historico():
    janela_historico = Toplevel()
    janela_historico.title("Histórico de Notas")
    janela_historico.geometry("400x300")

    conn = sqlite3.connect("notas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, nota1, nota2, media FROM alunos")
    registros = cursor.fetchall()
    conn.close()

    if registros:
        for registro in registros:
            nome, nota1, nota2, media = registro
            tk.Label(janela_historico, text=f"Aluno: {nome} | Nota 1: {nota1} | Nota 2: {nota2} | Média: {media:.2f}").pack(pady=2)
    else:
        tk.Label(janela_historico, text="Nenhum registro encontrado.").pack(pady=10)

# Configuração da janela principal
initialize_db()
janela_principal = tk.Tk()
janela_principal.title("Média Escolar")
janela_principal.geometry("400x200")

titulo = tk.Label(janela_principal, text="Bem-vindo ao sistema de Média Escolar", font=("Arial", 12, "bold"))
titulo.pack(pady=10)
# Botão "Adicionar Média" com cor de fundo azul e texto em branco
botao_adicionar = tk.Button(janela_principal, text="Adicionar Média", command=adicionar_media, bg="blue", fg="white")
botao_adicionar.pack(pady=5)
# Botão "Ver Histórico" com cor de fundo vermelho e texto em branco
botao_historico = tk.Button(janela_principal, text="Ver Histórico", command=ver_historico, bg="red", fg="white")
botao_historico.pack(pady=5)

janela_principal.mainloop()