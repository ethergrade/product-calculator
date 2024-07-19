import tkinter as tk

def update_calculations(*args):
    try:
        # Ottieni i valori inseriti dall'utente
        cost = entry_cost.get()
        margin = entry_margin.get()
        price = entry_price.get()
        markup = entry_markup.get()
        
        # Converti i valori in numeri, se non sono vuoti
        cost = float(cost) if cost else None
        margin = float(margin) if margin else None
        price = float(price) if price else None
        markup = float(markup) if markup else None
        
        # Inizializza i valori dei risultati
        result = ""
        
        # Calcola i valori mancanti
        if cost is None:
            if price is not None:
                if margin is not None:
                    # Calcolo corretto del costo
                    cost = price * (1 - margin / 100)
                elif markup is not None:
                    cost = price / (1 + markup / 100)
        if margin is None:
            if cost is not None and price is not None:
                margin = ((price - cost) / price) * 100
        if price is None:
            if cost is not None:
                if margin is not None:
                    price = cost / (1 - margin / 100)
                elif markup is not None:
                    price = cost * (1 + markup / 100)
        if markup is None:
            if cost is not None and price is not None:
                markup = ((price - cost) / cost) * 100

        # Mostra i risultati
        if cost is not None:
            result += f"COSTO: {cost:.2f}\n"
        if margin is not None:
            result += f"MARGINE: {margin:.2f}%\n"
        if price is not None:
            result += f"PREZZO: {price:.2f}\n"
        if markup is not None:
            result += f"MARKUP: {markup:.2f}%\n"
        
        if result == "":
            result = "Inserisci valori sufficienti per effettuare il calcolo."
        
        label_result.config(text=result)
        
    except ValueError:
        label_result.config(text="Per favore, inserisci valori numerici validi.")

def set_margin(value):
    entry_margin.delete(0, tk.END)
    entry_margin.insert(0, value)
    update_calculations()

def clear_entry(entry):
    entry.delete(0, tk.END)
    update_calculations()

def clear_all_entries():
    entry_cost.delete(0, tk.END)
    entry_margin.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_markup.delete(0, tk.END)
    update_calculations()

# Configura la finestra principale
root = tk.Tk()
root.title("Calcolo Costo, Margine, Prezzo e Markup")

# Etichette e campi di inserimento
tk.Label(root, text="COSTO:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
entry_cost = tk.Entry(root)
entry_cost.grid(row=0, column=1, padx=10, pady=5)
entry_cost.bind("<KeyRelease>", update_calculations)
tk.Button(root, text="C", command=lambda: clear_entry(entry_cost)).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="MARGINE (%):").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
entry_margin = tk.Entry(root)
entry_margin.grid(row=1, column=1, padx=10, pady=5)
entry_margin.bind("<KeyRelease>", update_calculations)
tk.Button(root, text="C", command=lambda: clear_entry(entry_margin)).grid(row=1, column=2, padx=5, pady=5)

# Bottoni per valori predefiniti del margine
tk.Button(root, text="40%", command=lambda: set_margin("40")).grid(row=1, column=3, padx=5, pady=5)
tk.Button(root, text="38%", command=lambda: set_margin("38")).grid(row=1, column=4, padx=5, pady=5)
tk.Button(root, text="36%", command=lambda: set_margin("36")).grid(row=1, column=5, padx=5, pady=5)

tk.Label(root, text="PREZZO:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
entry_price = tk.Entry(root)
entry_price.grid(row=2, column=1, padx=10, pady=5)
entry_price.bind("<KeyRelease>", update_calculations)
tk.Button(root, text="C", command=lambda: clear_entry(entry_price)).grid(row=2, column=2, padx=5, pady=5)

tk.Label(root, text="MARKUP (%):").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
entry_markup = tk.Entry(root)
entry_markup.grid(row=3, column=1, padx=10, pady=5)
entry_markup.bind("<KeyRelease>", update_calculations)
tk.Button(root, text="C", command=lambda: clear_entry(entry_markup)).grid(row=3, column=2, padx=5, pady=5)

# Bottone per cancellare tutti i valori
tk.Button(root, text="CANCELLA TUTTO", command=clear_all_entries).grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Etichetta per mostrare i risultati
label_result = tk.Label(root, text="Inserisci i valori sopra per vedere i risultati", justify=tk.LEFT)
label_result.grid(row=5, column=0, columnspan=6, padx=10, pady=10)

# Avvia la GUI
root.mainloop()