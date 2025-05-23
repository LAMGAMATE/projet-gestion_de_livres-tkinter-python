from tkinter import *
from tkinter import messagebox, ttk
import csv
import os

liste_livres = []

def form2():
    def enregistrer_csv():
        with open("livres.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for livre in liste_livres:
                writer.writerow(livre)

    def ajouter():
        titre = input_titre.get()
        auteur = input_auteur.get()
        annee = input_annee.get()
        isbn = input_isbn.get()
        selected_cat = listbox_cat.curselection()
        categorie = listbox_cat.get(selected_cat) if selected_cat else "Non spécifiee"
        disponible = var_dispo.get()

        if titre and auteur and annee and isbn:
            if not annee.isdigit():
                messagebox.showerror("Erreur", "Année doit etre un nombre entier.")
                return
            for livre in liste_livres:
                if livre[3] == isbn:
                    messagebox.showerror("Erreur", "ISBN existe déja dans la liste")
                    return

            livre = [titre, auteur, annee, isbn, categorie, disponible]
            liste_livres.append(livre)
            afficher_tout()
            enregistrer_csv()
            effacer()
        else:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs")

    def afficher_tout():
        for i in table.get_children():
            table.delete(i)
        for livre in liste_livres:
            table.insert('', END, values=livre)

    def supprimer():
        selected = table.selection()
        if selected:
            for sel in selected:
                values = table.item(sel, 'values')
                for i, livre in enumerate(liste_livres):
                    if livre == list(values):
                        del liste_livres[i]
                        break
            afficher_tout()
            enregistrer_csv()

    def modifier():
        selected = table.selection()
        if selected:
            index = table.index(selected[0])
            titre = input_titre.get()
            auteur = input_auteur.get()
            annee = input_annee.get()
            isbn = input_isbn.get()
            selected_cat = listbox_cat.curselection()
            categorie = listbox_cat.get(selected_cat) if selected_cat else "Non spécifiee"
            disponible = var_dispo.get()

            if titre and auteur and annee and isbn:
                if not annee.isdigit():
                    messagebox.showerror("Erreur", "Année doit etre un nombre")
                    return
                liste_livres[index] = [titre, auteur, annee, isbn, categorie, disponible]
                afficher_tout()
                enregistrer_csv()
                effacer()
            else:
                messagebox.showwarning("Attention", "Veuillez remplir tous les champs")

    def rechercher():
        mot_cle = zone_recherche.get().lower()
        for i in table.get_children():
            table.delete(i)
        for livre in liste_livres:
            if mot_cle in str(livre).lower():
                table.insert('', END, values=livre)

    def effacer():
        input_titre.delete(0, END)
        input_auteur.delete(0, END)
        input_annee.delete(0, END)
        input_isbn.delete(0, END)
        zone_recherche.delete(0, END)
        listbox_cat.selection_clear(0, END)
        var_dispo.set("Oui")

    def remplir_form(event):
        selected = table.selection()
        if selected:
            values = table.item(selected[0], 'values')
            input_titre.delete(0, END)
            input_titre.insert(0, values[0])
            input_auteur.delete(0, END)
            input_auteur.insert(0, values[1])
            input_annee.delete(0, END)
            input_annee.insert(0, values[2])
            input_isbn.delete(0, END)
            input_isbn.insert(0, values[3])
            for i in range(listbox_cat.size()):
                if listbox_cat.get(i) == values[4]:
                    listbox_cat.selection_clear(0, END)
                    listbox_cat.selection_set(i)
            var_dispo.set(values[5])

    root2 = Tk()
    root2.title("Gestion des Livres")
    root2.geometry("950x700")
    root2.configure(bg="#ecf0f1")
    root2.resizable(False, False)

    Label(root2, text="Titre:").place(x=20, y=20)
    input_titre = Entry(root2, width=40)
    input_titre.place(x=150, y=20)

    Label(root2, text="Auteur:").place(x=20, y=60)
    input_auteur = Entry(root2, width=40)
    input_auteur.place(x=150, y=60)

    Label(root2, text="Année:").place(x=20, y=100)
    input_annee = Entry(root2, width=40)
    input_annee.place(x=150, y=100)

    Label(root2, text="ISBN:").place(x=20, y=140)
    input_isbn = Entry(root2, width=40)
    input_isbn.place(x=150, y=140)

    Label(root2, text="Catégorie:").place(x=20, y=180)
    listbox_cat = Listbox(root2, height=5, exportselection=False)
    for cat in ["Roman", "Science", "Histoire", "Art", "Informatique", "Autre"]:
        listbox_cat.insert(END, cat)
    listbox_cat.place(x=150, y=180)

    Label(root2, text="Disponible:").place(x=20, y=300)
    var_dispo = StringVar(value="Oui")
    Radiobutton(root2, text="Oui", variable=var_dispo, value="Oui").place(x=150, y=300)
    Radiobutton(root2, text="Non", variable=var_dispo, value="Non").place(x=220, y=300)

    Label(root2, text="Rechercher:").place(x=550, y=20)
    zone_recherche = Entry(root2, width=30)
    zone_recherche.place(x=640, y=20)
    Button(root2, text="Rechercher", command=rechercher).place(x=830, y=18)

    Button(root2, text="Ajouter", command=ajouter, bg="#27ae60", fg="white", width=15).place(x=150, y=350)
    Button(root2, text="Modifier", command=modifier, bg="#2980b9", fg="white", width=15).place(x=310, y=350)
    Button(root2, text="Supprimer", command=supprimer, bg="#c0392b", fg="white", width=15).place(x=470, y=350)
    Button(root2, text="Effacer", command=effacer, bg="#f1c40f", width=15).place(x=630, y=350)

    columns = ("Titre", "Auteur", "Année", "ISBN", "Catégorie", "Disponible")
    table = ttk.Treeview(root2, columns=columns, show='headings')
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=120)

    table.place(x=20, y=400, width=900, height=250)
    table.bind("<ButtonRelease-1>", remplir_form)

    if os.path.exists("livres.csv"):
        with open("livres.csv", "r", encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 6:
                    liste_livres.append(row)
        afficher_tout()

    root2.mainloop()

def login():
    username = txt1.get()
    password = txt2.get()
    if username == "admin" and password == "1234":
        messagebox.showinfo("Succes", f"Bienvenue {username}")
        root.destroy()
        form2()
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")
        txt1.delete(0, 'end')
        txt2.delete(0, 'end')

root = Tk()
root.title("Connexion")
root.geometry("400x300")
root.configure(bg="#ecf0f1")
root.resizable(False, False)

frame_login = Frame(root, bg="#ffffff", bd=2, relief=SOLID)
frame_login.place(relx=0.5, rely=0.5, anchor=CENTER)

Label(frame_login, text="Se connecter", font=("Arial", 18, "bold"), bg="white", fg="#2c3e50").grid(row=0, column=0, columnspan=2, pady=20)

Label(frame_login, text="Nom d'utilisateur:", bg="white", anchor="w").grid(row=1, column=0, sticky="w", padx=10)
txt1 = Entry(frame_login, width=30)
txt1.grid(row=1, column=1, pady=10, padx=10)

Label(frame_login, text="Mot de passe:", bg="white", anchor="w").grid(row=2, column=0, sticky="w", padx=10)
txt2 = Entry(frame_login, show="*", width=30)
txt2.grid(row=2, column=1, pady=10, padx=10)

btn1 = Button(frame_login, text="Connexion", bg="#27ae60", fg="white", width=20, command=login)
btn1.grid(row=3, column=0, columnspan=2, pady=20)

root.mainloop()
