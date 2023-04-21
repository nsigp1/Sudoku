##importations


from random import randint
import tkinter as tk


##backend


class Noeud:

    def __init__(self, valeur=None, ligne=None, colonne=None, carre=None, fixe=False):
        """initialise une case de sudoku"""
        self.val = valeur  # valeur de la case
        self.ligne = ligne  # numero de ligne
        self.colonne = colonne  # numero de colonne
        self.carre = carre  # numero de carre ou boite
        self.fixe = fixe  # True si le numero est une contrainte, False sinon


class Sudoku:

    def __init__(self, grille=[]):
        """initialise une grille de sudoku 9x9"""
        self.grille = []  # cree grille vide sous forme de liste
        for i in range(9):
            if i < 3:
                carre = 0
            elif i < 6:
                carre = 3
            else:
                carre = 6
            for j in range(9):
                if j % 3 == 0:
                    carre += 1
                if grille == []:
                    self.grille.append(Noeud(None, i, j, carre))
                else:
                    if grille[i][j] == None:  # si la case n'est pas preremplie
                        self.grille.append(Noeud(grille[i][j], i, j, carre, False))  # remplir avec None
                    else:
                        self.grille.append(Noeud(grille[i][j], i, j, carre, True))  # remplir avec le numero prerempli

    def rempli(self) -> bool:
        """renvoie True si la grille est remplie, False sinon"""
        for i in self.grille:
            if i.val == None:
                return False
        return True

    def regles(self, noeud: Noeud) -> bool:
        """renvoie True si le Noeud en parametre est conforme avec les regles de la grille de sudoku, False sinon"""
        if noeud.val == None:  # une case vide est toujours conforme aux regles
            return True
        for i in self.grille:
            if i.ligne == noeud.ligne and i.val == noeud.val and i.colonne != noeud.colonne:  # deux memes chiffres sur meme ligne
                return False
            elif i.colonne == noeud.colonne and i.val == noeud.val and i.ligne != noeud.ligne:  # deux memes chiffres sur meme colonne
                return False
            elif i.carre == noeud.carre and i.val == noeud.val and (
                    i.ligne != noeud.ligne or i.colonne != noeud.colonne):  # deux memes chiffres sur meme carre/boite
                return False
        return True

    def bonne_grille(self) -> bool:
        """renvoie True si la grille n'enfreint pas les regles du jeu, False sinon"""
        for i in self.grille:
            if not self.regles(i):
                return False
        return True

    def dessiner(self):
        """dessine en console une representation du sudoku"""
        k = 0
        retour = "|"
        for i in self.grille:
            if k != i.ligne:
                print(retour)
                k += 1
                if i.val == None:
                    retour = "| |"
                else:
                    retour = "|" + str(i.val) + "|"
            else:
                if i.val == None:
                    retour += " |"
                else:
                    retour += str(i.val) + "|"
        print(retour)

    def resoudre(self):
        """resout un sudoku"""
        compteur = 0  # compte les iterrations
        indice = 0  # position de la cellule
        prec = False  # True si la derniere iterration avait un indice superieur, False sinon
        while not (self.rempli() and self.bonne_grille()):
            compteur += 1
            if indice > 80 or indice < 0 or compteur > 9 ** 4:  # complexitee estimee
                raise Exception("grille insoluble")
            if self.grille[indice].fixe == True:  # nombre a ne pas toucher
                if prec:
                    indice -= 1  # case precedente
                else:
                    indice += 1  # case suivante
            else:
                if self.grille[indice].val == None:
                    self.grille[indice].val = 1  # on initialise la valeur de la case a 1
                else:
                    self.grille[indice].val += 1  # on ajoute 1 a la valeur de la case deja remplie
                while not self.regles(self.grille[indice]):
                    self.grille[indice].val += 1  # on augmente de 1 la valeur de la case
                if self.grille[indice].val > 9:  # impossible selon les regles
                    self.grille[indice].val = None  # on reinitialise la valeur de la case a None (elle devient vide)
                    indice -= 1  # case precedente
                    prec = True  # on informe que l'on vient d'une case apres celle que l'on etudiera
                else:
                    indice += 1  # case suivante
                    prec = False  # on informe que l'on vient d'une case avant celle que l'on etudiera
                    
    def resoluble(self) -> bool:
        """retourne True si le sudoku est resoluble, False sinon"""
        try:
            self.resoudre()
        except:
            return False
        return True
    
    def fixer(self):
        """fixe les elements renseignes"""
        for i in self.grille:
            if i.val != None:
                i.fixe = True


def creer(nombres: int) -> Sudoku:
    """cree une grille de Sudoku resoluble preremplie avec nombres chiffres"""
    if nombres > 50: #evite de causer des problemes de lenteur, quitte a sacrifier de l'aleatoire (on peut remplacer 50 par une autre valeur, plus grande pour plus d'aleatoire, moins pour plus de rapidite)
        S = creer(50)
        S.resoudre()
        while nombres < 81:
            indice = randint(0, 80)
            if not S.grille[indice].fixe: #elimine des numeros a des places aleatoires qui ne sont pas celles remplies par l'appel creer()
                S.grille[indice].val = None
                nombres += 1
        S.fixer()
        return S
    G = []  # representation d'une grille sous forme de liste de listes (que des None)
    for i in range(9):
        G.append([])
        for _ in range(9):
            G[i].append(None)
    Sudo = Sudoku(G)
    while nombres > 0: #compteur de nombres restants a inserer
        ligne = randint(0, 8)
        colonne = randint(0, 8)
        if ligne < 3:
            if colonne < 3:
                carre = 1
            elif colonne < 6:
                carre = 2
            else:
                carre = 3
        elif ligne < 6:
            if colonne < 3:
                carre = 4
            elif colonne < 6:
                carre = 5
            else:
                carre = 6
        else:
            if colonne < 3:
                carre = 7
            elif colonne < 6:
                carre = 8
            else:
                carre = 9
        case = Noeud(randint(1, 9), ligne, colonne, carre, True) #cree une case a un emplacement aleatoire avec un numero aleatoire
        if Sudo.regles(case):
            for i in range(len(Sudo.grille)):
                if Sudo.grille[i].ligne == ligne and Sudo.grille[i].colonne == colonne and not Sudo.grille[i].fixe:
                    Sudo.grille[i] = case #place la case dans la grille si cette case n'est pas deja occupee
                    if Sudo.resoluble():
                        nombres -= 1 #un nombre a ete place dans la grille
                    else: #reinitialise la case modifiee
                        Sudo.grille[i].val = None
                        Sudo.grille[i].fixe = False
        for i in Sudo.grille:
            if i.fixe == False:
                i.val = None #elimine les elements nons fixes qui sont apparus a l'appel de la fonction resoluble()
    return Sudo


##tests backend

# S = Sudoku([
#     [None, 5, None, None, 3, None, 4, None, None],
#     [4, None, None, None, None, None, None, None, None],
#     [None, None, None, None, 7, 1, 8, None, None],
#     [3, None, 6, 2, 9, None, None, 5, None],
#     [1, None, None, None, 6, None, None, None, 3],
#     [None, 7, None, None, 1, 4, 6, None, 9],
#     [None, None, 9, 6, 2, None, None, None, None],
#     [None, None, None, None, None, None, None, None, 7],
#     [None, None, 2, None, 4, None, None, 9, None],
# ])
# 
# k = []
# for i in range(9):
#     k.append([])
#     for _ in range(9):
#         k[i].append(None)
# 
# S2 = Sudoku(k)
# 
# S3 = creer(70)


##frontend (pas encore bien documente)


class Affichage:
    def __init__(self, fenetre):
        """cree un affichage de jeu de Sudoku"""
        self.fenetre = fenetre
        
        self.fenetre.geometry("800x800")
        self.fenetre.title("Sudoku")
        self.fenetre.iconphoto(True, tk.PhotoImage(file="logo.png"))
        
        self.boutons_defauts()
    
    def boutons_defauts(self):
        """ajoute les boutons par defauts sur la premiere page"""
        self.btn_jouer = tk.Button(self.fenetre, text="Jouer", font=("Helvetica", 14), command=self.selection_activite)
        self.btn_jouer.pack(pady=20)
        
        self.btn_quitter_menu = tk.Button(self.fenetre, text="Quitter", font=("Helvetica", 14), command=self.fenetre.destroy)
        self.btn_quitter_menu.pack(side=tk.BOTTOM, pady=20)

    def selection_activite(self):
        """affiche la page pour selectionner entre resoudre et creer un sudoku"""
        self.btn_jouer.pack_forget()
        self.btn_quitter_menu.pack_forget()
        
        exception = False
        try:
            self.btn_resolution_grille.pack_forget()
            self.btn_retour.pack_forget()
        except:
            exception = True
            
        if not exception:
            self.btn_resolution_grille.pack_forget()
            self.btn_retour.pack_forget()
            
        self.btn_creer = tk.Button(self.fenetre, text="Créer une grille", font=("Helvetica", 14), command=self.afficher_grille)
        self.btn_creer.pack(pady=20)
        
        self.btn_resoudre = tk.Button(self.fenetre, text="Résoudre une grille", font=("Helvetica", 14), command=self.menu_resoudre)
        self.btn_resoudre.pack(pady=20)
        
        self.btn_quitter = tk.Button(self.fenetre, text="Quitter", font=("Helvetica", 14), command=self.fenetre.destroy)
        self.btn_quitter.pack(side=tk.BOTTOM, pady=20)

    def menu_resoudre(self):
        """affiche la page de resolution automatique de sudoku"""
        self.btn_creer.pack_forget()
        self.btn_resoudre.pack_forget()
        self.btn_quitter.pack_forget()
        
        self.btn_resolution_grille = tk.Button(self.fenetre, text="Résoudre", font=("Helvetica", 14))
        self.btn_resolution_grille.pack(pady=20)
        
        self.btn_retour = tk.Button(self.fenetre, text="Retour", font=("Helvetica", 14), command=self.selection_activite)
        self.btn_retour.pack(pady=20)
        
    def afficher_grille(self):
        """affiche une grille preremplie"""
        pass #pas encore fait


root = tk.Tk()
app = Affichage(root)
root.mainloop()