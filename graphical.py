import tkinter as tk

# creazione della finestra principale
root = tk.Tk()
# aggiunta del titolo alla finestra
root.wm_title("WP-LogCrack\u200E")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = int(screen_width * 0.5)
height = int(screen_height * 0.5)
# impostazione delle dimensioni della finestra
root.geometry(f"{width}x{height}")

# creazione del widget etichetta con testo formattato
logo_label = tk.Label(root, text="WP-LogCrack", font=("Arial", 30, "bold"), fg="#008000")
logo_label.pack(pady=20)

def submit():
    val1 = var1.get()
    val2 = var2.get()
    val3 = var3.get()
    accepted = var4.get()

    # esempio di stampa dei valori inseriti nella form
    print(f"Valore 1: {val1}")
    print(f"Valore 2: {val2}")
    print(f"Valore 3: {val3}")
    print(f"Accettazione: {accepted}")




var1 = tk.StringVar()
var2 = tk.StringVar()
var3 = tk.StringVar()
label1 = tk.Label(root, text="Username")
entry1 = tk.Entry(root, textvariable=var1)
label2 = tk.Label(root, text="Password")
entry2 = tk.Entry(root, textvariable=var2)
label3 = tk.Label(root, text="Link Server")
entry3 = tk.Entry(root, textvariable=var3)
# creazione della casella di controllo
var4 = tk.BooleanVar()
checkbutton = tk.Checkbutton(root, text="DNS spoofing", variable=var4)

# creazione del bottone di invio
submit_button = tk.Button(root, text="Start Attack", command=submit)

# disposizione dei widget nella finestra
label1.place(relx=0.5, rely=0.25, anchor="center")
entry1.place(relx=0.5, rely=0.30, anchor="center")

label2.place(relx=0.5, rely=0.4, anchor="center")
entry2.place(relx=0.5, rely=0.45, anchor="center")

label3.place(relx=0.5, rely=0.55, anchor="center")
entry3.place(relx=0.5, rely=0.6, anchor="center")

checkbutton.place(relx=0.5, rely=0.7, anchor="center")
submit_button.place(relx=0.5, rely=0.9, anchor="center")

# avvio del mainloop della finestra
root.mainloop()