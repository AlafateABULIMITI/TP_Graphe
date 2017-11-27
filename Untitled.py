# coding: utf-8

# In[10]:

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
#print touslesarcs
INFINI = 99999

Origine = []
Destination = []

for un_arc in touslesarcs:
    # Decoupage du contenu d'une ligne
    cet_arc = un_arc.split("\t")
    orig = int(cet_arc[0])
    dest = int(cet_arc[1])
    Origine.append(orig)
    Destination.append(dest)

# ############################
# Remplissage des vecteurs
# ############################

NbSommets = max(max(Origine), max(Destination)) + 1

succ = [[] for i in range(NbSommets)]
prec = [[] for i in range(NbSommets)]

NbArcs = len(Origine)
for u in range(0, NbArcs):
    succ[Origine[u]].append(Destination[u])
    prec[Destination[u]].append(Origine[u])

print(Origine)
print(Destination)
print(succ)
print(prec)

# In[33]:


def ChercheChaine(dep, arr):
    global Marque
    global Predecesseur
    global Successeur
    print 'cherche chaine de ', dep, ' a ', arr
    Liste = []
    Liste.append(dep)
    Deja_emplie = [0] * NbSommets
    trouve = False
    while (Liste != []) and not trouve:
        i = Liste[0]
        Marque[i] = 1
        del (Liste[0])
        for s in succ[i]:
            if s == arr:
                trouve = True
                Predecesseur[s] = i
                break
            elif Marque[s] == 0 and Deja_emplie[s] == 0:
                Liste = [s] + Liste
                Predecesseur[s] = i
                Deja_emplie[s] = 1
        for d in prec[i]:
            if d == arr:
                trouve = True
                Successeur[d] = i
                break
            elif Marque[d] == 0 and Deja_emplie[d] == 0:
                Liste = [d] + Liste
                Successeur[d] = i
                Deja_emplie[d] = 1
    return trouve


#######


def ChercheChemin(dep, arr):
    global MarqueChemin
    Liste = []
    Liste.append(dep)
    Deja_emplie = [0] * NbSommets
    trouve = False
    while (Liste != []) and not trouve:
        i = Liste[0]
        MarqueChemin[i] = 1
        del (Liste[0])
        for s in succ[i]:
            if s == arr:
                trouve = True
                PredecesseurChemin[s] = i
                break
            elif MarqueChemin[s] == 0 and Deja_emplie[s] == 0:
                PredecesseurChemin[s] = i
                Liste = [s] + Liste
                Deja_emplie[s] = 1
    return trouve


######


def Connexite():
    connexite = True
    for sommetOrig in range(0, NbSommets):
        for sommetDest in range(0, NbSommets):
            if sommetOrig != sommetDest:
                if not ChercheChemin(sommetOrig, sommetDest):
                    connexite = False
    return connexite


while (1):
    orig = int(input("entrez le sommet origin "))
    if orig >= 0 and orig <= NbSommets - 1:
        break
while (1):
    dest = int(input("entrez le sommet destination "))
    if dest >= 0 and dest <= NbSommets - 1:
        break

Marque = [0 for j in range(0, NbSommets)]
Predecesseur = [-1 for j in range(0, NbSommets)]
Successeur = [-1 for j in range(0, NbSommets)]
PredecesseurChemin = [-1 for j in range(0, NbSommets)]
MarqueChemin = [0 for j in range(0, NbSommets)]

if ChercheChaine(orig, dest):
    print 'chaine trouve'
else:
    print 'non trouve'

# print ChercheChemin(orig,dest)
sommet = dest
print "la chaine est: "
while (1):
    if (Predecesseur[sommet] != -1):
        print '(', Predecesseur[sommet], sommet, ')'
        sommet = Predecesseur[sommet]
    elif (Successeur[sommet] != -1):
        print '(', sommet, Successeur[sommet], ')'
        sommet = Successeur[sommet]
    if sommet == orig:
        break

# cherche le chemin
if ChercheChemin(orig, dest):
    print 'chemin trouve'
else:
    print 'chemin non trouve'

sommet = dest
while (1):
    if (PredecesseurChemin[sommet] != -1):
        print '(', PredecesseurChemin[sommet], sommet, ')'
        sommet = PredecesseurChemin[sommet]
    if sommet == orig:
        break

if Connexite():
    print 'le graphe est connexe'
else:
    print 'le graphe est non connexe'
