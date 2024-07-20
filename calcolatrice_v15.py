import tkinter as tk
from tkinter import ttk

def update_calculations(*args):
    try:
        # Ottieni i valori inseriti dall'utente
        cost = entry_cost.get()
        margin = entry_margin.get()
        price = entry_price.get()
        markup = entry_markup.get()
        minutes = entry_minutes.get()
        hours = entry_hours.get()
        hourly_cost = entry_hourly_cost.get()
        
        # Converti i valori in numeri, se non sono vuoti
        cost = float(cost) if cost else None
        margin = float(margin) if margin else None
        price = float(price) if price else None
        markup = float(markup) if markup else None
        minutes = float(minutes) if minutes else None
        hours = float(hours) if hours else None
        hourly_cost = float(hourly_cost) if hourly_cost else None
        
        # Calcola le ore in base ai minuti, se le ore non sono fornite
        if hours is None and minutes is not None:
            hours = minutes / 60
        # Calcola i minuti in base alle ore, se i minuti non sono forniti
        elif minutes is None and hours is not None:
            minutes = hours * 60
        
        # Calcola i valori mancanti
        if hourly_cost is not None:
            if cost is None:
                if price is not None:
                    if margin is not None:
                        cost = price * (1 - margin / 100)
            if price is None:
                if cost is not None:
                    if margin is not None:
                        price = cost / (1 - margin / 100)
        
        if cost is None:
            if price is not None:
                if margin is not None:
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

        # Calcola costo basato su costi orari e tempo
        if hourly_cost is not None:
            if minutes is not None:
                cost = hourly_cost * (minutes / 60)
            elif hours is not None:
                cost = hourly_cost * hours
            
            # Calcola il prezzo basato sul costo orario e margine
            if margin is not None:
                price = cost / (1 - margin / 100)
            elif markup is not None:
                price = cost * (1 + markup / 100)

        # Mostra i risultati
        if cost is not None:
            label_cost_result.config(text=f"COSTO: {cost:.2f}")
        else:
            label_cost_result.config(text="")
        
        if margin is not None:
            label_margin_result.config(text=f"MARGINE: {margin:.2f}%")
        else:
            label_margin_result.config(text="")
        
        if price is not None:
            label_price_result.config(text=f"PREZZO: {price:.2f}")
        else:
            label_price_result.config(text="")

        if hourly_cost is not None:
            label_hourly_cost_result.config(text=f"COSTO ORARIO: {hourly_cost:.2f}")
        else:
            label_hourly_cost_result.config(text="")
        
        if hours is not None:
            label_hours_result.config(text=f"ORE: {hours:.2f}")
        else:
            label_hours_result.config(text="")
        
        if minutes is not None:
            label_minutes_result.config(text=f"MINUTI: {minutes:.2f}")
        else:
            label_minutes_result.config(text="")
        
        if not any([cost, margin, price, hourly_cost, hours, minutes]):
            label_general_result.config(text="Inserisci valori sufficienti per effettuare il calcolo.")
        else:
            label_general_result.config(text="")
        
    except ValueError:
        label_general_result.config(text="Per favore, inserisci valori numerici validi.")

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
    entry_minutes.delete(0, tk.END)
    entry_hours.delete(0, tk.END)
    entry_hourly_cost.delete(0, tk.END)
    update_calculations()

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Fare in modo che l'aggiornamento della clipboard sia visibile

def exit_program():
    root.quit()

# Configura la finestra principale
root = tk.Tk()
root.title("Product Management - Service Price Calculator")

# Funzione per creare campo input con bottone di cancellazione interno
def create_input_with_clear_button(label_text, row):
    frame = tk.Frame(root, bg="white")
    frame.grid(row=row, column=0, columnspan=6, padx=10, pady=5, sticky=tk.W+tk.E)

    label = tk.Label(frame, text=label_text, bg="white")
    label.pack(side=tk.LEFT, padx=5)

    entry_frame = tk.Frame(frame)
    entry_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
    
    entry = ttk.Entry(entry_frame, width=20)
    entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
    entry.bind("<KeyRelease>", update_calculations)

    button_clear = tk.Button(entry_frame, text="C", command=lambda: clear_entry(entry))
    button_clear.pack(side=tk.RIGHT)

    return entry

# Input utente con bottoni di cancellazione
entry_cost = create_input_with_clear_button("COSTO:", 0)
entry_margin = create_input_with_clear_button("MARGINE:", 1)
entry_price = create_input_with_clear_button("PREZZO:", 2)
entry_markup = create_input_with_clear_button("MARKUP (%):", 3)
entry_minutes = create_input_with_clear_button("MINUTI:", 4)
entry_hours = create_input_with_clear_button("ORE:", 5)
entry_hourly_cost = create_input_with_clear_button("COSTO ORARIO:", 6)

# Bottone per cancellare tutti i valori
tk.Button(root, text="CANCELLA TUTTO", command=clear_all_entries).grid(row=7, column=0, columnspan=6, pady=10, sticky=tk.W+tk.E)

# Cornice per i risultati con bordo grigio chiaro
results_frame = tk.Frame(root, bg="lightgray", bd=2, relief=tk.SOLID)
results_frame.grid(row=8, column=0, columnspan=6, padx=10, pady=10, sticky=tk.W+tk.E)

# Etichette dei risultati e bottoni per copiare i valori
def create_result_label_with_copy(text, row, column):
    frame = tk.Frame(results_frame, bg="lightgray")
    frame.grid(row=row, column=column, padx=5, pady=5, sticky=tk.W)

    label = tk.Label(frame, text=text, bg="lightgray", width=20, anchor=tk.W, justify=tk.LEFT, relief=tk.SOLID, bd=1)
    label.pack(side=tk.LEFT)

    button_copy = tk.Button(frame, text="CP", command=lambda: copy_to_clipboard(label.cget("text")), bg="lightgray")
    button_copy.pack(side=tk.RIGHT, padx=5)

    return label

# Risultati
label_cost_result = create_result_label_with_copy("", 0, 0)
label_margin_result = create_result_label_with_copy("", 0, 1)
label_price_result = create_result_label_with_copy("", 0, 2)

label_hourly_cost_result = create_result_label_with_copy("", 1, 0)
label_hours_result = create_result_label_with_copy("", 1, 1)
label_minutes_result = create_result_label_with_copy("", 1, 2)

label_general_result = tk.Label(results_frame, text="", bg="lightgray", anchor=tk.W, justify=tk.LEFT)
label_general_result.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)

# Cornice per i bottoni di margine
frame_margin_buttons = tk.Frame(root, bg="lightgray", bd=2, relief=tk.SOLID)
frame_margin_buttons.grid(row=9, column=0, columnspan=6, padx=10, pady=10, sticky=tk.W+tk.E)

tk.Label(frame_margin_buttons, text="MARGINE (%)", bg="lightgray").pack(side=tk.LEFT, padx=5)

btn_40 = tk.Button(frame_margin_buttons, text="40%", command=lambda: set_margin(40), width=5)
btn_40.pack(side=tk.LEFT, padx=5)

btn_38 = tk.Button(frame_margin_buttons, text="38%", command=lambda: set_margin(38), width=5)
btn_38.pack(side=tk.LEFT, padx=5)

btn_36 = tk.Button(frame_margin_buttons, text="36%", command=lambda: set_margin(36), width=5)
btn_36.pack(side=tk.LEFT, padx=5)

# Bottone per uscire dal programma
tk.Button(root, text="ESCI", command=exit_program).grid(row=10, column=0, columnspan=6, pady=10, sticky=tk.W+tk.E)

# Avvia la GUI
root.mainloop()
