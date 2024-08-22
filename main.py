import random
import os
import time
import sys
import msvcrt

# Constantes pour la taille de la grille
GRILLE_LARGEUR = 10
GRILLE_HAUTEUR = 20

# Définition des formes des pièces (rotation des pièces représentée par différentes matrices)
PIECES_TETRIS = {
    'I': [['0000',
           '1111',
           '0000',
           '0000']],
    'O': [['11',
           '11']],
    'T': [['010',
           '111',
           '000']],
    'S': [['011',
           '110',
           '000']],
    'Z': [['110',
           '011',
           '000']],
    'J': [['100',
           '111',
           '000']],
    'L': [['001',
           '111',
           '000']]
}

class Piece:
    def __init__(self, forme):
        self.forme = forme
        self.rotation = 0
        self.x = GRILLE_LARGEUR // 2 - len(self.forme[0]) // 2
        self.y = 0
    
    @property
    def structure(self):
        return self.forme[self.rotation % len(self.forme)]
    
    def rotation_suivante(self):
        return (self.rotation + 1) % len(self.forme)
    
    def rotate(self):
        self.rotation = self.rotation_suivante()

class Tetris:
    def __init__(self):
        self.grille = [[' ' for _ in range(GRILLE_LARGEUR)] for _ in range(GRILLE_HAUTEUR)]
        self.piece_courante = self.nouvelle_piece()
        self.score = 0
    
    def nouvelle_piece(self):
        forme = random.choice(list(PIECES_TETRIS.keys()))
        return Piece(PIECES_TETRIS[forme])

    def est_valide(self, piece, dx=0, dy=0, rotation=None):
        if rotation is None:
            rotation = piece.rotation
        structure = piece.forme[rotation % len(piece.forme)]
        for y, ligne in enumerate(structure):
            for x, cellule in enumerate(ligne):
                if cellule == '1':
                    if (y + piece.y + dy >= GRILLE_HAUTEUR or
                        x + piece.x + dx < 0 or
                        x + piece.x + dx >= GRILLE_LARGEUR or
                        self.grille[y + piece.y + dy][x + piece.x + dx] != ' '):
                        return False
        return True

    def fixer_piece(self, piece):
        structure = piece.structure
        for y, ligne in enumerate(structure):
            for x, cellule in enumerate(ligne):
                if cellule == '1':
                    self.grille[y + piece.y][x + piece.x] = 'X'
        self.supprimer_lignes()
        self.piece_courante = self.nouvelle_piece()
        if not self.est_valide(self.piece_courante):
            self.fin_du_jeu()

    def supprimer_lignes(self):
        nouvelles_lignes = []
        lignes_supprimees = 0
        for ligne in self.grille:
            if ' ' not in ligne:
                lignes_supprimees += 1
            else:
                nouvelles_lignes.append(ligne)
        for _ in range(lignes_supprimees):
            nouvelles_lignes.insert(0, [' ' for _ in range(GRILLE_LARGEUR)])
        self.grille = nouvelles_lignes
        self.score += lignes_supprimees * 100

    
    def fin_du_jeu(self):
        self.afficher_grille()
        print(f"Game Over! Votre score: {self.score}")
        rejouer = input("Voulez-vous rejouer? (o/n): ")
        if rejouer.lower() == 'o':
            self.__init__() 
            self.jouer()  
        else:
            sys.exit()

    def afficher_grille(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        grille_temporaire = [ligne[:] for ligne in self.grille]
        structure = self.piece_courante.structure
        for y, ligne in enumerate(structure):
            for x, cellule in enumerate(ligne):
                if cellule == '1':
                    grille_temporaire[y + self.piece_courante.y][x + self.piece_courante.x] = 'X'
        for ligne in grille_temporaire:
            print('|' + ''.join(ligne) + '|')
        print('+' + '-' * GRILLE_LARGEUR + '+')
        print(f'Score: {self.score}')
        
    def descendre_piece(self):
        if self.est_valide(self.piece_courante, dy=1):
            self.piece_courante.y += 1
        else:
            self.fixer_piece(self.piece_courante)

    def tourner_piece(self):
        rotation_suivante = self.piece_courante.rotation_suivante()
        if self.est_valide(self.piece_courante, rotation=rotation_suivante):
            self.piece_courante.rotate()

    def deplacer_gauche(self):
        if self.est_valide(self.piece_courante, dx=-1):
            self.piece_courante.x -= 1

    def deplacer_droite(self):
        if self.est_valide(self.piece_courante, dx=1):
            self.piece_courante.x += 1
            
    def jouer(self):
        self.afficher_grille()
        self.descendre_piece()

def gestion_clavier(tetris):
    if msvcrt.kbhit():
        touche = msvcrt.getch().decode('cp437').lower()
        if touche == 'a':
            tetris.deplacer_gauche()
        elif touche == 'd':
            tetris.deplacer_droite()
        elif touche == 's':
            tetris.descendre_piece()
        elif touche == 'x':
            tetris.tourner_piece()

def main():
    tetris = Tetris()
    while True:
        tetris.jouer()
        gestion_clavier(tetris)
        time.sleep(0.3)

if __name__ == '__main__':
    main()


