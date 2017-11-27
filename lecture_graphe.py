# coding: utf8
# ############################
# Lecture du fichier
# ############################

fichier_graphe = 'graphe_qcq.txt'

# Format du fichier :
# Pour chaque arc :
# sommet_origine - tab - sommet_destination
# (derniere ligne sans le ENTER)

LeGraphe = open(fichier_graphe, "r")
touslesarcs = LeGraphe.readlines()

INFINI = 99999

Origine = []
Destination = []
Capa_min = []
Capa_max = []
for un_arc in touslesarcs:
    # Decoupage du contenu d'une ligne
    cet_arc = un_arc.split("\t")
    orig = int(cet_arc[0])
    dest = int(cet_arc[1])
    capmin = int(cet_arc[2])
    capmax = int(cet_arc[3])
    Origine.append(orig)
    Destination.append(dest)
    Capa_min.append(capmin)
    Capa_max.append(capmax)

# ############################
# Remplissage des vecteurs
# ############################

NbSommets = max(max(Origine), max(Destination)) + 1

NbArcs = len(Origine)

Couleur = ['-' for j in range(0, NbArcs)]
Couleur_succ = [[] for i in range(NbSommets)]
Couleur_prec = [[] for i in range(NbSommets)]
succ = [[] for i in range(NbSommets)]
prec = [[] for i in range(NbSommets)]

for u in range(0, NbArcs):
    succ[Origine[u]].append(Destination[u])
    prec[Destination[u]].append(Origine[u])
    Couleur_succ[Origine[u]].append('N')
    Couleur_prec[Destination[u]].append('N')

print(Origine)
print(Destination)
print(succ)
print(prec)
