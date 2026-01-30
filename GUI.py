import tkinter as tk
from tkinter import ttk

# --- TON TRAVAIL : L'INTERFACE GRAPHIQUE (GUI) ---
class InterfaceFourmiliere:
    def __init__(self, fenetre_principale):
        self.fenetre = fenetre_principale
        self.fenetre.title("Projet Colonie de Fourmis")
        self.fenetre.configure(bg="#0A3764") 

        # 1. CRÉATION DU PANNEAU DE GAUCHE (MENU)
        self.menu = tk.Frame(self.fenetre, bg="#03111F", padx=15, pady=15)
        self.menu.pack(side="left", fill="y")

        tk.Label(self.menu, text="PARAMÈTRES", fg="white", bg="#D90707", 
                 font=("Helvetica", 12)).pack(pady=10)

        # Les curseurs pour les camarades (Métier)
        self.vitesse = self.creer_curseur("Vitesse des fourmis", 1, 10)
        self.evaporation = self.creer_curseur("Évaporation des traces", 80, 99)
        self.faim = self.creer_curseur("Endurance (Faim)", 100, 500)

        # Le bouton pour le camarade (Simulateur)
        self.bouton_play = tk.Button(self.menu, text="LANCER LA SIMULATION", 
                                     bg="#830CF3", fg="white", font=("Arial", 10, "bold"),
                                     relief="flat", command=self.clic_bouton)
        self.bouton_play.pack(pady=30, fill="x")

        # 2. CRÉATION DE LA ZONE DE DESSIN (À DROITE)
        self.zone_dessin = tk.Canvas(self.fenetre, width=600, height=500, 
                                     bg="white", bd=0, highlightthickness=0)
        self.zone_dessin.pack(side="right", padx=20, pady=20)

        # Dessiner le Nid et la Nourriture au départ
        self.preparer_carte()

    def creer_curseur(self, nom, min_val, max_val):
        """Aide à créer un curseur proprement"""
        tk.Label(self.menu, text=nom, fg="#BDC3C7", bg="#34495E").pack(anchor="w")
        curseur = ttk.Scale(self.menu, from_=min_val, to=max_val, orient="horizontal")
        curseur.pack(fill="x", pady=(0, 15))
        return curseur

    def preparer_carte(self):
        """Dessine les éléments fixes sur la carte"""
        # Le Nid (en haut à gauche)
        self.zone_dessin.create_oval(50, 50, 100, 100, fill="#000000", outline="")
        self.zone_dessin.create_text(75, 40, text="NID", font=("Arial", 8, "bold"))

        # La Nourriture (en bas à droite)
        self.zone_dessin.create_rectangle(500, 400, 550, 450, fill="#57F10F", outline="")
        self.zone_dessin.create_text(525, 390, text="RESSOURCE", font=("Arial", 8, "bold"))

    def clic_bouton(self):
        """Action quand on clique sur le bouton"""
        print("Signal envoyé au Simulateur : Lancement")

    def rafraichir_affichage(self, liste_fourmis):
        """
        C'est ici que le Simulateur va envoyer les données.
        On efface tout ce qui bouge et on redessine.
        """
        self.zone_dessin.delete("mobile") # Supprime uniquement les fourmis
        
        for fourmi in liste_fourmis:
            couleur = "green" if fourmi.a_nourriture else "black"
            self.zone_dessin.create_oval(fourmi.x-2, fourmi.y-2, fourmi.x+2, fourmi.y+2, 
                                         fill=couleur, tags="mobile")

# --- LANCEMENT DE L'APPLICATION ---
if __name__ == "__main__":
    app = tk.Tk()
    mon_ihm = InterfaceFourmiliere(app)
    app.mainloop()