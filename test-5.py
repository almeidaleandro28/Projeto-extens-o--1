import tkinter as tk
from tkinter import messagebox
import sqlite3

class BusinessSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Business System")

        self.conn = sqlite3.connect('business.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

        self.setup_ui()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                id INTEGER PRIMARY KEY,
                                type TEXT,
                                description TEXT,
                                amount REAL,
                                invoice_number TEXT)''')
        self.conn.commit()

    def setup_ui(self):
        tk.Label(self.root, text="Descrição").grid(row=0, column=0)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Valor").grid(row=1, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Tipo (receita/despesa)").grid(row=2, column=0)
        self.type_entry = tk.Entry(self.root)
        self.type_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Número da Nota Fiscal").grid(row=3, column=0)
        self.invoice_entry = tk.Entry(self.root)
        self.invoice_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Adicionar", command=self.add_transaction).grid(row=4, column=0, columnspan=2)

        tk.Button(self.root, text="Mostrar Lançamentos", command=self.show_transactions).grid(row=5, column=0, columnspan=2)

        tk.Button(self.root, text="Mostrar Fluxo de Caixa", command=self.show_cash_flow).grid(row=6, column=0, columnspan=2)

        tk.Label(self.root, text="Número da Nota Fiscal para Filtrar").grid(row=7, column=0)
        self.filter_entry = tk.Entry(self.root)
        self.filter_entry.grid(row=7, column=1)

        tk.Button(self.root, text="Filtrar", command=self.filter_transactions).grid(row=8, column=0, columnspan=2)

        tk.Button(self.root, text="Fluxo de Caixa por Nota", command=self.show_cash_flow_by_invoice).grid(row=9, column=0, columnspan=2)

    def add_transaction(self):
        desc = self.desc_entry.get()
        amt = float(self.amount_entry.get())
        ttype = self.type_entry.get()
        invoice = self.invoice_entry.get()

        if desc and amt and ttype and invoice:
            self.cursor.execute("INSERT INTO transactions (type, description, amount, invoice_number) VALUES (?, ?, ?, ?)",
                                (ttype, desc, amt, invoice))
            self.conn.commit()
            self.clear_entries()
            messagebox.showinfo("Info", "Transação adicionada com sucesso")
        else:
            messagebox.showwarning("Erro de Entrada", "Preencha todos os campos")

    def clear_entries(self):
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.invoice_entry.delete(0, tk.END)
        self.filter_entry.delete(0, tk.END)

    def show_transactions(self):
        self.cursor.execute("SELECT * FROM transactions")
        transactions = self.cursor.fetchall()

        display_text = "ID | Tipo | Descrição | Valor | Nota Fiscal\n"
        display_text += "-"*50 + "\n"
        for trans in transactions:
            display_text += f"{trans[0]} | {trans[1]} | {trans[2]} | {trans[3]} | {trans[4]}\n"

        messagebox.showinfo("Todos os Lançamentos", display_text)

    def show_cash_flow(self):
        self.cursor.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
        data = self.cursor.fetchall()

        revenue = sum(row[1] for row in data if row[0] == 'receita')
        expenses = sum(row[1] for row in data if row[0] == 'despesa')
        cash_flow = revenue - expenses

        cash_flow_text = f"Total de Receitas: R${revenue}\nTotal de Despesas: R${expenses}\nFluxo de Caixa: R${cash_flow}"
        messagebox.showinfo("Fluxo de Caixa", cash_flow_text)

    def filter_transactions(self):
        invoice = self.filter_entry.get()
        if invoice:
            self.cursor.execute("SELECT * FROM transactions WHERE invoice_number=?", (invoice,))
            transactions = self.cursor.fetchall()

            if transactions:
                display_text = "ID | Tipo | Descrição | Valor | Nota Fiscal\n"
                display_text += "-"*50 + "\n"
                for trans in transactions:
                    display_text += f"{trans[0]} | {trans[1]} | {trans[2]} | {trans[3]} | {trans[4]}\n"

                messagebox.showinfo("Filtrar Lançamentos", display_text)
            else:
                messagebox.showinfo("Filtrar Lançamentos", "Nenhum lançamento encontrado com esse número de nota fiscal")
        else:
            messagebox.showwarning("Erro de Entrada", "Por favor, insira o número da nota fiscal para filtrar")

    def show_cash_flow_by_invoice(self):
        invoice = self.filter_entry.get()
        if invoice:
            self.cursor.execute("SELECT type, SUM(amount) FROM transactions WHERE invoice_number=? GROUP BY type", (invoice,))
            data = self.cursor.fetchall()

            revenue = sum(row[1] for row in data if row[0] == 'receita')
            expenses = sum(row[1] for row in data if row[0] == 'despesa')
            cash_flow = revenue - expenses

            cash_flow_text = f"Nota Fiscal: {invoice}\nTotal de Receitas: R${revenue}\nTotal de Despesas: R${expenses}\nFluxo de Caixa: R${cash_flow}"
            messagebox.showinfo("Fluxo de Caixa por Nota Fiscal", cash_flow_text)
        else:
            messagebox.showwarning("Erro de Entrada", "Por favor, insira o número da nota fiscal para calcular o fluxo de caixa")

    def __del__(self):
        self.conn.close()

# Criando a janela principal
root = tk.Tk()
app = BusinessSystem(root)
root.mainloop()
