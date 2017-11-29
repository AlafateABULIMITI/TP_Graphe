# coding: utf8
# ############################
# Lecture du fichier
# ############################

fichier_graphe = 'graphe_mcf.txt'

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
Gamma = []

for un_arc in touslesarcs:
    # Decoupage du contenu d'une ligne
    cet_arc = un_arc.split("\t")
    orig = int(cet_arc[0])
    dest = int(cet_arc[1])
    capmin = int(cet_arc[2])
    capmax = int(cet_arc[3])
    cost = int(cet_arc[4])
    Origine.append(orig)
    Destination.append(dest)
    Capa_min.append(capmin)
    Capa_max.append(capmax)
    Gamma.append(cost)
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

# Flot = [9, 0, 9, 9, 9]
# Theta = [10, 20, 10, 5, -25]
Flot = [0] * NbArcs
Theta = [0] * NbArcs


def ChercheArc(s, t):
    # print 'chercherArc', s, ' ', t
    i = 0
    while (1):
        if Origine[i] == s and Destination[i] == t:
            return i
        i += 1


def maj_courleur_mcf():
    global Flot
    for u in range(0, NbArcs):
        i = Origine[u]
        j = Destination[u]
        if Theta[u] < Gamma[u]:
            if Flot[u] > Capa_min[u]:
                Couleur[u] = 'V'
            if Flot[u] < Capa_min[u]:
                Couleur[u] = 'N'
            if Flot[u] == Capa_min[u]:
                Couleur[u] = 'I'
        if Theta[u] > Gamma[u]:
            if Flot[u] > Capa_max[u]:
                Couleur[u] = 'V'
            if Flot[u] < Capa_max[u]:
                Couleur[u] = 'N'
            if Flot[u] == Capa_max[u]:
                Couleur[u] = 'I'
        if Theta[u] == Gamma[u]:
            if Flot[u] > Capa_min[u] and Flot[u] < Capa_max[u]:
                Couleur[u] = 'R'
            if Flot[u] <= Capa_min[u]:
                Couleur[u] = 'N'
            if Flot[u] >= Capa_max[u]:
                Couleur[u] = 'V'
        Couleur_succ[i][succ[i].index(j)] = Couleur[u]
        Couleur_prec[j][prec[j].index(i)] = Couleur[u]


def ChercheCycle_NRV(u0):
    # print 'ChercherCycle'
    global Predecesseur, Successeur, LaChaine, Marque
    Marque = [0 for j in range(0, NbSommets)]
    Predecesseur = [-1 for j in range(0, NbSommets)]
    Successeur = [-1 for j in range(0, NbSommets)]
    dep = Destination[u0]
    arr = Origine[u0]
    sens_u0 = 1
    if Couleur[u0] == 'N':
        dep = Destination[u0]
        arr = Origine[u0]
        sens_u0 = 1
    elif Couleur[u0] == 'V':
        dep = Origine[u0]
        arr = Destination[u0]
        sens_u0 = -1
    # print "dep: ", dep
    # print "arr: ", arr
    Liste = []
    Deja_emplie = [0] * NbSommets
    trouve = False

    # u = cherche(dep,j)
    # if (u!=u0)
    for s in succ[dep]:
        u = ChercheArc(dep, s)
        if u != u0 and (Couleur_succ[dep][succ[dep].index(s)] == 'N'
                        or Couleur_succ[dep][succ[dep].index(s)] == 'R'):
            # print 'u in cherche ', u
            Liste = [s] + Liste
            Deja_emplie[s] = 1
            Predecesseur[s] = dep
    for p in prec[dep]:
        u = ChercheArc(p, dep)
        if u != u0 and (Couleur_prec[dep][prec[dep].index(p)] == 'V'
                        or Couleur_prec[dep][prec[dep].index(p)] == 'R'):
            # print 'u in cherche ', u
            Liste = [p] + Liste
            Deja_emplie[p] = 1
            Successeur[p] = dep


#    print 'List init: ', Liste
#    print Couleur
    while Liste != [] and not trouve:
        # print 'chaeuqe Liste: ', Liste
        i = Liste[0]
        # print i, " succ[i]: ", succ[i], Couleur_succ[i]
        Marque[i] = 1
        del (Liste[0])
        for s in succ[i]:
            if Couleur_succ[i][succ[i].index(
                    s)] == 'N' or Couleur_succ[i][succ[i].index(s)] == 'R':
                # print 's = ', s
                # print 'Marque[s] = ', Marque[s], Deja_emplie[s]
                if s == arr:
                    trouve = True
                    Predecesseur[s] = i
                    break
                elif Marque[s] == 0 and Deja_emplie[s] == 0:
                    Liste = [s] + Liste
                    Predecesseur[s] = i
                    Deja_emplie[s] = 1
        for d in prec[i]:
            if Couleur_prec[i][prec[i].index(
                    d)] == 'V' or Couleur_prec[i][prec[i].index(d)] == 'R':
                if d == arr:
                    trouve = True
                    Successeur[d] = i
                    break
                elif Marque[d] == 0 and Deja_emplie[d] == 0:
                    Liste = [d] + Liste
                    Successeur[d] = i
                    Deja_emplie[d] = 1
    # print 'Successeur ', Successeur
    # print 'Predecesseur ', Predecesseur
    LaChaine = []

    if trouve:
        LaChaine.append([u0, sens_u0])
        # print 'arr ', arr
        # print 'dep ', dep
        i = arr
        while i != dep:
            # print 'line 154'
            if Successeur[i] != -1:
                u = ChercheArc(i, Successeur[i])
                LaChaine.append([u, -1])
                i = Successeur[i]
            elif Predecesseur[i] != -1:
                u = ChercheArc(Predecesseur[i], i)
                LaChaine.append([u, 1])
                i = Predecesseur[i]
        # print LaChaine
    return trouve


def ModifierFlot():
    # print 'modifier Flot'
    global Flot, LaChaine
    print 'In modifyFlow ', Flot
    print Couleur
    episilonf = 999999
    # print 'LaChaine ', LaChaine
    # print 'Flot ', Flot
    for i in LaChaine:
        u = i[0]
        sens = i[1]
        # print 'u = ', u
        # print 'Couleur[u] ', Couleur[u]
        # print 'Capa_max[u] ', Capa_max[u]
        # print 'Capa_min[u] ', Capa_min[u]
        if sens == 1:
            episilonf = min(episilonf, Capa_max[u] - Flot[u])
        else:
            episilonf = min(episilonf, Flot[u] - Capa_min[u])
    # print 'episilonf ', episilonf
    for i in LaChaine:
        u = i[0]
        sens = i[1]
        Flot[u] += episilonf * sens


def ChercheSetA(u0):
    global setA
    setA = []
    Liste = []
    dep = Destination[u0]
    # print 'dest u0 = ', dep
    arr = Origine[u0]
    Liste.append(dep)
    setA.append(dep)
    Deja_emplie = [0] * NbSommets
    Marque = [0 for j in range(0, NbSommets)]
    while (Liste != []):
        i = Liste[0]
        Marque[i] = 1
        del (Liste[0])
        for s in succ[i]:
            if s != arr and Marque[s] == 0 and Deja_emplie[s] == 0:
                if Couleur[u0] == 'N':
                    if Couleur_succ[i][succ[i].index(
                            s)] == 'N' or Couleur_succ[i][succ[i].index(
                                s)] == 'R':
                        Liste = [s] + Liste
                        setA.append(s)
                        Deja_emplie[s] = 1
                elif Couleur[u0] == 'V':
                    if Couleur_succ[i][succ[i].index(
                            s)] == 'V' or Couleur_succ[i][succ[i].index(
                                s)] == 'R':
                        Liste = [s] + Liste
                        setA.append(s)
                        Deja_emplie[s] = 1
        for d in prec[i]:
            if d != arr and Marque[d] == 0 and Deja_emplie[d] == 0:
                if Couleur[u0] == 'N':
                    if Couleur_prec[i][prec[i].index(
                            d)] == 'V' or Couleur_prec[i][prec[i].index(
                                d)] == 'R':
                        Liste = [d] + Liste
                        setA.append(d)
                        Deja_emplie[d] = 1
                elif Couleur[u0] == 'V':
                    if Couleur_prec[i][prec[i].index(
                            d)] == 'N' or Couleur_prec[i][prec[i].index(
                                d)] == 'R':
                        Liste = [d] + Liste
                        setA.append(d)
                        Deja_emplie[d] = 1


def ChercheOmega(setA):
    global omegaPlus, omegaMoins
    omegaPlus = []
    omegaMoins = []
    for i in range(0, NbArcs):
        if Origine[i] in setA and Destination[i] not in setA:
            omegaPlus.append(i)
        if Origine[i] not in setA and Destination[i] in setA:
            omegaMoins.append(i)


def ModifierTension(op, om):
    global Theta
    episilon = 99999
    temp = []
    sens = 1
    for i in (op + om):
        if i in op:
            if Flot[i] == Capa_max[i]:
                temp.append(99999)
            else:
                temp.append(Gamma[i] - Theta[i])
        elif i in om:
            if Flot[i] == Capa_min[i] and Theta[i] <= Gamma[i]:
                temp.append(99999)
            else:
                temp.append(Theta[i] - Gamma[i])
    episilon = min(temp)

    for i in (op + om):
        if i in op:
            Theta[i] += episilon
        if i in om:
            Theta[i] -= episilon


Marque = [0 for j in range(0, NbSommets)]
Predecesseur = [-1 for j in range(0, NbSommets)]
Successeur = [-1 for j in range(0, NbSommets)]
LaChaine = []
# Flot = [9, 0, 9, 9, 9]
setA = []
omegaPlus = []
omegaMoins = []

Compatible = [0] * NbArcs
Conforme = [0] * NbArcs

maj_courleur_mcf()
for i in range(0, NbArcs):
    if Theta[i] == Gamma[i] and (Flot[i] in range(Capa_min[i],
                                                  Capa_max[i] + 1)):
        Conforme[i] = 1
    elif Theta[i] > Gamma[i] and Flot[i] == Capa_max[i]:
        Conforme[i] = 1
    elif Theta[i] < Gamma[i] and Flot[i] == Capa_min[i]:
        Conforme[i] = 1
    else:
        Conforme[i] = 0
NbConforme = sum(Conforme)
while NbConforme != NbArcs:
    u0 = Conforme.index(0)
    print Flot
    if ChercheCycle_NRV(u0):
        ModifierFlot()
    else:
        ChercheSetA(u0)
        ChercheOmega(setA)
        if Couleur[u0] == 'V':
            temp = omegaPlus
            omegaPlus = omegaMoins
            omegaMoins = temp
        print 'setA:', setA
        print 'o+:', omegaPlus
        print 'flow before:', Flot
        ModifierTension(omegaPlus, omegaMoins)
    maj_courleur_mcf()
    for i in range(0, NbArcs):
        if Theta[i] == Gamma[i] and (Flot[i] in range(Capa_min[i],
                                                      Capa_max[i] + 1)):
            Conforme[i] = 1
        elif Theta[i] > Gamma[i] and Flot[i] == Capa_max[i]:
            Conforme[i] = 1
        elif Theta[i] < Gamma[i] and Flot[i] == Capa_min[i]:
            Conforme[i] = 1
        else:
            Conforme[i] = 0
    NbConforme = sum(Conforme)
print 'Flot: ', Flot
print 'Theta: ', Theta
# print Conforme
