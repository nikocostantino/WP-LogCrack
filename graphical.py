import tkinter as tk
from tkinter import messagebox

from utility import is_valid_ip_address, is_valid_wp_login_url


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.wm_title("WP-LogCrack\u200E")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = int(screen_width * 0.3)
        height = int(screen_height * 0.5)
        self.geometry(f"{width}x{height}")

        # creazione dei frame
        self.frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self)

        logo_label = tk.Label(self.frame1, text="WP-LogCrack", font=("Arial", 30, "bold"), fg="#008000")
        logo_label.pack(pady=20)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.server = tk.StringVar()
        self.label1 = tk.Label(self.frame1, text="Username")
        self.entry1 = tk.Entry(self.frame1, textvariable=self.username)
        self.label2 = tk.Label(self.frame1, text="Password")
        self.entry2 = tk.Entry(self.frame1, textvariable=self.password)
        self.label3 = tk.Label(self.frame1, text="Link Server")
        self.entry3 = tk.Entry(self.frame1, textvariable=self.server)
        self.label4 = tk.Label(self.frame1, text="Victim Ip")
        # creazione della casella di controllo
        self.dns_spoof = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(self.frame1, text="DNS spoofing", variable=self.dns_spoof, command=self.toggle_dns_spoof)

        # creazione del campo di testo che verrà mostrato solo se la casella di controllo è selezionata
        self.ip = tk.StringVar()
        self.entry4 = tk.Entry(self.frame1, textvariable=self.ip)

        # disposizione dei widget nella finestra
        self.entry4.pack_forget()

        # creazione del bottone di invio
        self.submit_button = tk.Button(self.frame1, text="Start Attack", command=self.submit)

        # disposizione dei widget nella finestra
        self.label1.pack(pady=10)#place(relx=0.5, rely=0.20, anchor="center")
        self.entry1.pack(pady=2)#.place(relx=0.5, rely=0.25, anchor="center")

        self.label2.pack(pady=10)#.place(relx=0.5, rely=0.35, anchor="center")
        self.entry2.pack(pady=2)#.place(relx=0.5, rely=0.40, anchor="center")

        self.label3.pack(pady=10)#.place(relx=0.5, rely=0.50, anchor="center")
        self.entry3.pack(pady=2)#.place(relx=0.5, rely=0.55, anchor="center")

        self.checkbutton.pack(pady=10)#.place(relx=0.5, rely=0.65, anchor="center")

        self.label4.pack(pady=10)#.place(relx=0.5, rely=0.75, anchor="center")
        self.entry4.pack(pady=2)#.place(relx=0.5, rely=0.80, anchor="center")
        self.entry4.config(state="disabled")

        self.submit_button.pack(pady=15)#.place(relx=0.5, rely=0.9, anchor="center")











        # creazione dei widget del frame2
        label2 = tk.Label(self.frame2, text="Pagina 2")
        button2 = tk.Button(self.frame2, text="Vai alla pagina 1", command=self.show_frame1)

        # posizionamento dei widget nel frame2
        label2.pack(pady=1)
        button2.pack(pady=1)

        # impostazione del frame1 come frame corrente
        self.current_frame = self.frame1
        self.current_frame.pack()

    def show_frame1(self):
        # mostra il frame1 e nasconde il frame2
        self.frame2.pack_forget()
        self.frame1.pack()
        self.current_frame = self.frame1

    def show_frame2(self):
        # mostra il frame2 e nasconde il frame1
        self.frame1.pack_forget()
        self.frame2.pack()
        self.current_frame = self.frame2

    def submit(self):
        errors = False

        if not is_valid_wp_login_url(self.server.get()):
            messagebox.showinfo("Error", "Server not valid!")
            errors = True
        if not is_valid_ip_address(self.ip.get()):
            messagebox.showinfo("Error", "IP address not valid!")
            errors = True
        self.show_frame2()

    def toggle_dns_spoof(self):
        if self.dns_spoof.get():
            self.entry4.config(state="normal")

        else:
            self.entry4.config(state="disabled")


# creazione dell'applicazione
app = MyApp()

# avvio del mainloop
app.mainloop()
