import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
import os

ARQUIVO_PEDIDOS = "pedidos.json"

def carregar_pedidos():
    if os.path.exists(ARQUIVO_PEDIDOS):
        with open(ARQUIVO_PEDIDOS, "r") as f:
            return json.load(f)
    return []

def salvar_pedidos(pedidos):
    with open(ARQUIVO_PEDIDOS, "w") as f:
        json.dump(pedidos, f, indent=4)

def consultar_cep(cep):
    try:
        url = f"https://viacep.com.br/ws/{cep}/json/"
        resposta = requests.get(url)
        dados = resposta.json()
        
        if "erro" in dados:
            return None
        
        endereco = f"{dados['logradouro']} - {dados['bairro']} - {dados['localidade']}/{dados['uf']}"
        return endereco

    except Exception as e:
        print(f"Erro ao consultar o CEP: {e}")
        return None

janela = tk.Tk()
janela.title("Reparo de Iluminação Pública")
janela.geometry("420x450")
janela.resizable(True, False)

pedidos = carregar_pedidos()
endereco_encontrado = tk.StringVar()

def buscar_endereco():
    cep = cep_entry.get()
    endereco = consultar_cep(cep)
    if endereco:
        endereco_encontrado.set(endereco)
        endereco_label.config(text=f"Endereço: {endereco}")
        endereco_label.update_idletasks()
        altura_extra = endereco_label.winfo_reqheight()
        janela.geometry(f"420x{450 + altura_extra}")
    else:
        endereco_encontrado.set("")
        endereco_label.config(text="Endereço não encontrado.")
        messagebox.showwarning("Erro", "CEP inválido ou não encontrado.")

def gerar_pedido():
    cep = cep_entry.get()
    endereco = endereco_encontrado.get()
    numero = numero_entry.get()
    problema = problema_var.get()

    if not (cep and endereco and numero and problema):
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos corretamente.")
        return

    protocolo = len(pedidos) + 1
    pedido = {
        "protocolo": protocolo,
        "cep": cep,
        "endereco": endereco,
        "numero": numero,
        "problema": problema
    }
    pedidos.append(pedido)
    salvar_pedidos(pedidos)
    messagebox.showinfo("Pedido enviado", f"Protocolo gerado: {protocolo}")
    limpar_campos()

def limpar_campos():
    cep_entry.delete(0, tk.END)
    numero_entry.delete(0, tk.END)
    problema_var.set("")
    endereco_label.config(text="")
    endereco_encontrado.set("")
    janela.geometry("420x450")

def abrir_meus_pedidos():
    def buscar_protocolo():
        try:
            num = int(entrada_protocolo.get())
            resultado = next((p for p in pedidos if p["protocolo"] == num), None)
            texto_resultado.delete("1.0", tk.END)
            if resultado:
                texto_resultado.insert(tk.END, f"Protocolo: {resultado['protocolo']}\n")
                texto_resultado.insert(tk.END, f"CEP: {resultado['cep']}\n")
                texto_resultado.insert(tk.END, f"Endereço: {resultado['endereco']}, Nº {resultado['numero']}\n")
                texto_resultado.insert(tk.END, f"Problema: {resultado['problema']}")
            else:
                texto_resultado.insert(tk.END, "Protocolo não encontrado.")
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido.")

    janela_pedidos = tk.Toplevel()
    janela_pedidos.title("Consultar Pedido por Protocolo")
    janela_pedidos.geometry("400x250")
    janela_pedidos.resizable(False, False)

    tk.Label(janela_pedidos, text="Digite o número do protocolo:").pack(pady=5)
    entrada_protocolo = tk.Entry(janela_pedidos)
    entrada_protocolo.pack()

    tk.Button(janela_pedidos, text="Buscar", command=buscar_protocolo).pack(pady=5)

    texto_resultado = tk.Text(janela_pedidos, height=10)
    texto_resultado.pack(fill=tk.BOTH, expand=True)

# --- Interface principal ---
tk.Label(janela, text="Digite o CEP da rua:").pack(pady=5)
cep_entry = tk.Entry(janela)
cep_entry.pack()

tk.Button(janela, text="Buscar Endereço", command=buscar_endereco).pack(pady=5)
endereco_label = tk.Label(janela, text="", wraplength=380, justify="left")
endereco_label.pack()

tk.Label(janela, text="Número da casa:").pack(pady=5)
numero_entry = tk.Entry(janela)
numero_entry.pack()

tk.Label(janela, text="Tipo de problema:").pack(pady=5)
problema_var = tk.StringVar()
problemas = ["Lâmpada queimada", "Acesa o tempo todo", "Acende e apaga"]
for p in problemas:
    ttk.Radiobutton(janela, text=p, variable=problema_var, value=p).pack(anchor="w")

tk.Button(janela, text="Gerar Pedido", command=gerar_pedido).pack(pady=10)
tk.Button(janela, text="Meus Pedidos", command=abrir_meus_pedidos).pack()

janela.mainloop()
