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
            if not S.grille[indice].fixe and S.grille[indice].val != None: #elimine des numeros a des places aleatoires qui ne sont pas celles remplies par l'appel creer()
                S.grille[indice].val = None
                nombres += 1
        S.fixer()
        return S
    else:
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


##frontend

class Fenetre:
    
    
    def __init__(self, win):
        """initialise les attributs de la fenetre de Sudoku en appelle self.page_depart()"""
        self.win = win #fenetre (ou window)
        self.win.geometry("1920x1080") #format de la fenetre
        self.win.minsize(960, 720) #format minimum de la fenetre
        self.win.iconphoto(True, tk.PhotoImage(file="logo.png")) #icone de la fenetre
        self.win.title("Sudoku par Arthur") #titre de la fenetre
        self.page_depart() 
        
    def effacer(self):
        """efface tous les elements de la fenetre, obligatoire a chaque nouvelle page"""
        for i in self.win.winfo_children():
            i.destroy() #detruit tous les elements de la page
            
    def quitter(self):
        """tue la fenetre"""
        self.win.destroy() #tue la fenetre
        
    def page_depart(self, texte = False):
        """premiere page, propose le choix entre quitter, creer une grille (self.page_creer1()) ou resoudre une grille (self.page_resoudre())"""
        self.effacer() #obligatoire
        
        btn_quitter = tk.Button(self.win, text="Quitter", command=self.quitter, font=('Arial', 25)).pack(side=tk.TOP) #tue la fenetre
        
        if texte: #si l'utilisateur a resolu un Sudoku
            texte_felicitations = tk.Label(self.win, text="Bravo !", font=('Arial', 40)).pack(side=tk.TOP, pady=30)
        
        frame = tk.Frame(self.win) #Frame pour la mise en page
        btn_creer = tk.Button(frame, text="Creer une grille", command=self.page_creer1, font=('Arial', 40)).pack(pady=80) #creer un Sudoku
        btn_resoudre = tk.Button(frame, text="Resoudre une grille", command=self.page_resoudre, font=('Arial', 40)).pack(pady=80) #resoudre un Sudoku
        frame.pack(expand=tk.YES)
        
    def page_creer1(self):
        """propose de creer une grille de Sudoku avec un nombre de chiffres preremplis a selectionner"""
        self.effacer() #obligatoire
        
        btn_retour = tk.Button(self.win, text="Retour", command=self.page_depart, font=('Arial', 25)).pack() #fait revenir une page en arriere
        
        frame = tk.Frame(self.win) #Frame pour la mise en page
        txt_selection = tk.Label(frame, text="Combien de chiffres voulez-vous dans la grille ?", font=('Arial', 25)) #texte
        txt_selection.pack(pady=40)
        choix_selection = tk.Entry(frame, width=2, font=('Arial', 25)) #entree utilisateur
        choix_selection.pack(pady=40)
        self.choix = choix_selection #pour creation_grille()
        btn_valider = tk.Button(frame, text = "Valider", font=('Arial', 25), command=self.creation_grille) #bouton Valider
        btn_valider.pack()
        frame.pack(expand=tk.YES) #mise en page
        
    def creation_grille(self):
        """Verifie si la creation d'une grille avec le nombre de chiffres entres est possible"""
        try:
            int(self.choix.get())
        except:
            return #si l'entree n'est pas un chiffre
        if int(self.choix.get()) >= 0 and int(self.choix.get()) <= 81: #si le chiffre est bon
            self.page_creer2(int(self.choix.get()))
        else:
            txt_mauvaise_selection = tk.Label(self.win, text="Merci de faire une entree valide (un nombre entre 0 et 81 inclus)", font=('Arial', 25), fg="red").pack() #texte fausse entree
    
        
    def page_creer2(self, elmts):
        """affiche la grille de Sudoku preremplie"""
        self.effacer() #obligatoire
        
        btn_retour = tk.Button(self.win, text="Retour", command=self.page_creer1, font=('Arial', 25)).pack() #bouton retour
        
        self.Sudo = creer(elmts).grille #cree grille avec elmts chiffres
        
        self.cases = {} #contients les cases 
        
        self.frame = tk.Frame(self.win) #Frame pour la mise en page
        
        for i in range(9):
            for j in range(9):
                if self.Sudo[i*9 + j].val == None: #case vide
                    vcmd = (self.win.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
                    self.cases[str(i) + str(j)] = tk.Entry(self.frame, width=2, font=('Arial', 40), validate="key", validatecommand=vcmd)
                    self.cases[str(i) + str(j)].grid(row=i, column=j) #cree une entree utilisateur selon les regles de validate()
                else:
                    tk.Label(self.frame, width=2, font=('Arial', 40), text=str(self.Sudo[i*9 + j].val)).grid(row=i, column=j) #remplit la case avec le chiffre prerempli
                    
        btn_verifier = tk.Button(self.frame, text="Verifier",font=('Arial', 40), command=self.verifier_grille).grid(row=10, column=3, columnspan=3, pady=20) #bouton Verifier
        
        self.frame.pack(expand=tk.YES) #mise en page
        
                


    def validate(self, action, index, valeur, ancienne_valeur, texte, type_entree, type_declencheur, nom_widget):
        """bloque la saisie d'autre chose qu'un chiffre entre 1 et 9 inclus ou d'un vide sur une des cases de Sudoku"""
        if action == "1": #il y a un changement dans l'entree
            if texte in '0123456789' and len(valeur) < 2: #entree permise
                return True
            elif texte == "": #entree permise
                return True
            else: #entree interdite
                return False
        else:
            return True #pas de changement dans l'entree
        
    
    def verifier_grille(self):
        """verifie si la grille remplie par l'utilisateur est correcte et terminee"""
        L = [] #grille sous forme de liste de listes
        for i in range(len(self.Sudo)):
            if i % 9 == 0:
                L.append([])
            L[i // 9].append(self.Sudo[i].val) #rempli L avec les valeurs preremplies
            
        for k, v in self.cases.items(): #parcours des entrees
            if v.get() != "" : #si l'entree n'est pas vide
                L[int(k[0])][int(k[1])] = int(v.get())
            else:
                texte_reessayer = tk.Label(self.frame, text="Il y a une erreur dans la grille !", font=('Arial', 30), fg="red").grid(row=9, column=0, columnspan=9) #texte grille mauvaise
                self.frame.pack(expand=tk.YES) #mise en page
                return
        
        Sudo_tmp = Sudoku(L) #cree un Sudoku() avec la grille L
        if Sudo_tmp.rempli() and Sudo_tmp.bonne_grille():
            self.page_depart(True) #bonne reponse
        else:
            texte_reessayer = tk.Label(self.frame, text="Il y a une erreur dans la grille !", font=('Arial', 30), fg="red").grid(row=9, column=0, columnspan=9) #texte grille mauvaise
            self.frame.pack(expand=tk.YES) #mise en page
            
    def page_resoudre(self):
        """page de resolution automatique"""
        self.effacer() #obligatoire
        
        btn_retour = tk.Button(self.win, text="Retour", command=self.page_depart, font=('Arial', 25)).pack() #bouton retour
        
        self.cases = {} #contients les cases 
        
        self.frame = tk.Frame(self.win) #Frame pour la mise en page
        
        for i in range(9):
            for j in range(9):
                vcmd = (self.win.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
                self.cases[str(i) + str(j)] = tk.Entry(self.frame, width=2, font=('Arial', 40), validate="key", validatecommand=vcmd)
                self.cases[str(i) + str(j)].grid(row=i, column=j) #cree une entree utilisateur selon les regles de validate()
                
        btn_resoudre = tk.Button(self.frame, text="Resoudre la grille",font=('Arial', 40), command=self.resoudre_grille).grid(row=10, column=0, columnspan=9, pady=20) #bouton Verifier
        
        self.frame.pack(expand=tk.YES) #mise en page
        
    def resoudre_grille(self):
        """resout la grille remplie partiellement par l'utilisateur"""
        L = [] #grille sous forme de liste de liste
        for i in range(9):
            L.append([])
            for j in range(9):
                for k, v in self.cases.items():
                    if int(k[0]) == i and int(k[1]) == j: #case a remplir
                        if v.get() != "": #si la case a ete saisie
                            L[i].append(int(v.get())) #remplir avec la valeur saisie
                        else:
                            L[i].append(None) #remplir avec un None
        
        Sudo_tmp = Sudoku(L) #cree un Sudoku() avec la grille L
        
        try:
            Sudo_tmp.resoudre()
        except: #la grille n'est pas resoluble
            txt_grille_insoluble = tk.Label(self.frame, text="Grille insoluble", font=('Arial', 30), fg="red").grid(row=9, column=0, columnspan=9) #texte grille insoluble
            return
        
        self.page_resolu(Sudo_tmp.grille)
        
        
    def page_resolu(self, grille:list):
        """page avec la grille resolue, les chiffres non saisis par l'utilisateur sont en rouge"""
        self.effacer() #obligatoire
        
        btn_continuer = tk.Button(self.win, text="Continuer", command=self.page_depart, font=('Arial', 25)).pack() #bouton continuer
        
        self.frame = tk.Frame(self.win) #Frame pour la mise en page
        
        for i in range(9):
            for j in range(9):
                if grille[i*9 + j].fixe == True: #l'utilisateur a renseigne la case
                    tk.Label(self.frame, width=2, font=('Arial', 40), text=str(grille[i*9 + j].val)).grid(row=i, column=j) #cree une case avec le chiffre de l'utilisateur
                else:
                    tk.Label(self.frame, width=2, font=('Arial', 40), text=str(grille[i*9 + j].val), fg="red").grid(row=i, column=j) #cree une case avec le chiffre inscrit par l'appel resoudre_grille()
                
        self.frame.pack(expand=tk.YES) #mise en page




        
##creation de la fenetre

root = tk.Tk() #fenetre
f = Fenetre(root) #constructions
root.mainloop() #creer la fenetre

