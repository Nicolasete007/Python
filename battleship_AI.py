from random import randint, choice

def generar_tauler_buit(mida=10):
    """
    Generar un tauler buit de la mida indicada.
    """
    return [[0 for _ in range(mida)] for _ in range(mida)]

def comprova_marc(tauler, inici, final):
    """
    Comprova l'estat de la zona on aniria el vaixell i
    el marc al voltant, i mira si tot es aigüa.
    """
    amunt = max(0, inici[0] - 1)
    esquerra = max(0, inici[1] - 1)
    avall = min(len(tauler), final[0] +  1)
    dreta = min(len(tauler[0]), final[1] +  1)
    return sum([sum(llista[esquerra:dreta])
                for llista in tauler[amunt:avall]]) == 0

def omplir_vaixell(tauler, vaixell, valor):
    """
    Omple les caselles d'un vaixell amb el valor indicat.
    """
    inici, final = vaixell
    for llista in tauler[inici[0]:final[0]]:
        llista[inici[1]:final[1]] = [valor for _ in range(inici[1], final[1])]

def generar_enfonsar_flota(mida=10,
                           vaixells = {"portaavions": (1, 5),
                                       "cuirassats": (2, 4),
                                       "destructors": (3, 3),
                                       "fragates": (2, 2),
                                       "submarins": (4, 1)
                                       },
                           intents=100):
    """
    Genera un tauler amb la mida indicada i amb la flotat definida al diccionari vaixells.
    La codificació de vaixells es:
    Clau: Tipus de vaixell
    Valor: Tupla amb (nombre de vaixells, mida dels vaixells)
    S'intentarà generar els diferents en els intents indicats. Si no es pot, el resultat
    sera None.
    """
    tauler = generar_tauler_buit(mida)
    flota = {}

    for vaixell in sorted(vaixells, key=lambda x: vaixells[x][1], reverse=True):
        flota[vaixell] = []
        dades_vaixell = vaixells[vaixell]
        for _ in range(dades_vaixell[0]):
            valid = False
            while not valid:
                dreta = 0
                esquerra = len(tauler[0])
                amunt = 0
                avall = len(tauler)
                # Definim cap a on mira el vaixell
                # 0 dreta
                # 1 avall
                direccio = randint(0, 1)
                longitud = dades_vaixell[1]
                if direccio == 0:
                    esquerra -= longitud
                else:
                    avall -= longitud

                inici = randint(amunt, avall - 1), randint(dreta, esquerra - 1)

                if direccio == 0:
                    final = inici[0] + 1, inici[1] + longitud
                else:
                    final = inici[0] + longitud, inici[1] + 1

                if comprova_marc(tauler, inici, final):
                    omplir_vaixell(tauler, (inici, final), longitud)
                    flota[vaixell].append((inici, final))
                    valid = True

                if intents > 0:
                    intents -= 1
                else:
                    return None
    return tauler, flota

while True:
    resultat = generar_enfonsar_flota()
    if resultat is not None:
        tauler, flota = resultat
        break

tauler_joc = generar_tauler_buit()

def preparar_dades_flota(flota):
    vius = 0
    nova_flota = flota.copy()
    for vaixell in flota:
        for idx, posicio in enumerate(flota[vaixell]):
            inici, final = posicio
            mida = max(final[0]-inici[0], final[1]-inici[1])
            nova_flota[vaixell][idx] = [posicio, mida]
            vius += 1
    return nova_flota, vius

def comprovar_estat_vaixell(flota, fila, columna):
    for vaixell in flota:
        for idx, (posicio, _) in enumerate(flota[vaixell]):
            inici, final = posicio
            if fila in range(inici[0], final[0]) and columna in range(inici[1], final[1]):
                flota[vaixell][idx][1] -= 1
                #print("vaixell", vaixell, idx, flota[vaixell][idx][1])
                if flota[vaixell][idx][1] == 0:
                    return 'E', posicio
                else:
                    return 'X', posicio

def jugar(mida=10,
          vaixells = {"portaavions": (1, 5),
                      "cuirassats": (2, 4),
                      "destructors": (3, 3),
                      "fragates": (2, 2),
                      "submarins": (4, 1)
                      }
         ):
    # Generar la memoria
    memoria = {}
    # Generar el tauler i les dades de la flota
    while True:
        resultat = generar_enfonsar_flota(mida, vaixells)
        if resultat is not None:
            tauler, flota_inicial = resultat
            break
    flota, vius = preparar_dades_flota(flota_inicial)
    tauler_joc = generar_tauler_buit(mida)
    finalitzat = False
    torns = 0
    #print("vius:", vius)
    while not finalitzat:
        (fila, columna), memoria = jugador_bo(tauler_joc, memoria)
        if tauler_joc[fila][columna] == 0:
            if tauler[fila][columna] == 0:
                tauler_joc[fila][columna] = 'A'
            else:
                estat, vaixell = comprovar_estat_vaixell(flota, fila, columna)
                if estat == 'X':
                    tauler_joc[fila][columna] = estat
                elif estat == 'E':
                    omplir_vaixell(tauler_joc, vaixell, estat)
                    vius -= 1
                    finalitzat = (vius == 0)
                    #print("vius:", vius)
        torns += 1
    print(torns)
    return torns, tauler_joc

###########################################################################
###########################################################################
###########################################################################

direccio = 0

def casella_aleatoria(tauler):

    """Escollirà una casella aleatoria, començant per les parells i despres les senars,
    per tal de fer una graella i facilitar el trobar els vaixells més grans."""
    
    # Torna la direccio a 0
    global direccio
    direccio = 0

    caselles_possibles = []

    for f in range(len(tauler)):
        for c in range(len(tauler[f])):

            # Si hi ha caselles parells les ficara a la llisa de caselles possibles
            if (f+c) % 2 == 0 and tauler[f][c] == 0:
                caselles_possibles.append((f, c))

    # Si no hi ha caselles parells la llista estara buida, i escollira una casella aleatòria de les restants
    if caselles_possibles == []:
        
        x = randint(0, 9)
        y = randint(0, 9)

        while tauler[x][y] != 0:
            
            x = randint(0, 9)
            y = randint(0, 9)

    # Si hi ha caselles parell n'escollirà una de la llista
    else:
        x, y = choice(caselles_possibles)
    
    return x, y

def caselles_del_voltant(tauler, f, c):

    """Aquesta funció torna l'estat de les caselles del voltant d'una casella donada.
    La casella cNord es la de dalt, cSud la de baix, cEst la de la dreta i cOest la de
    l'esquerra. Si la casella està a la frontera del tauler, es marca com a 'res' l'estat
    de la casella que quedi fora."""

    if f != 0:
        cNord = tauler[f-1][c]
    else:
        cNord = "res"

    if f != 9:
        cSud = tauler[f+1][c]
    else:
        cSud = "res"

    if c != 9:
        cEst = tauler[f][c+1]
    else:
        cEst = "res"

    if c != 0:
        cOest = tauler[f][c-1]
    else:
        cOest = "res"

    return cNord, cSud, cEst, cOest

def buscar_direccions_possibles(tauler, filaA, columnaA):

    """Un cop s'ha trobat un vaixell, si el seu estat no és enfonsat,
    aquesta funció buscarà la direcció on ha de ser la resta del vaixell,
    segons les caselles cNord, cSud, cEst i cOest."""

    global direccio

    direccions_possibles = []

    cNord, cSud, cEst, cOest = caselles_del_voltant(tauler, filaA, columnaA)

    # Aquí el programa comprova si la casella actual té més d'una aigua al voltant. Si no avançarà cap a l'altra banda. 
    if (cNord == "X" and cSud == 0) or ((cNord == "A" or cNord == "res") and cEst == "A" and cOest == "A"):
        direccio = "sud"
    elif (cSud == "X" and cNord == 0) or ((cSud == "A" or cSud == "res") and cEst == "A" and cOest == "A"):
        direccio = "nord"
    elif (cEst == "X" and cOest == 0) or ((cEst == "A" or cEst == "res") and cNord == "A" and cSud == "A"):
        direccio = "oest"
    elif (cOest == "X" and cEst == 0) or ((cOest == "A" or cOest == "res") and cNord == "A" and cSud == "A"):
        direccio = "est"

    # En cas que no hi hagi una sola possibilitat, es fa una elecció aleatòria de les caselles possibles.
    elif cNord != "X" and cSud != "X" and cEst != "X" and cOest != "X":
        if cNord == 0:
            direccions_possibles.append("nord")
        if cSud == 0:
            direccions_possibles.append("sud")
        if cEst == 0:
            direccions_possibles.append("est")
        if cOest == 0:
            direccions_possibles.append("oest")

        direccio = choice(direccions_possibles)

def seguir_matant_barquitus(tauler, filaA, columnaA):

    """Segons la direcció establerta, aquesta funció escollirà una casella."""

    if direccio == "nord":
        x, y = filaA-1, columnaA

    elif direccio == "sud":
        x, y = filaA+1, columnaA

    elif direccio == "est":
        x, y = filaA, columnaA+1

    elif direccio == "oest":
        x, y = filaA, columnaA-1

    # Per tal d'evitar errors, afegeixo un else que retorna una casella aleatòria, en cas que l'elecció de direcció falli
    else:
        x, y = casella_aleatoria(tauler)

    return x, y

def marcar_aigua_al_voltant(tauler, fila, columna, tot):

    """Com que els vaixells no es poden tocar entre ells, per tal de minimitzar
    les caselles posibles on trobar-los, aquesta funció marca com a aigua les
    caselles del voltant dels vaixells trobats i enfonsats"""

    ### Marcar les cantonades com a aigua ###
    if fila != 9 and columna != 9:
        tauler[fila+1][columna+1] = "A"

    if fila != 9 and columna != 0:
        tauler[fila+1][columna-1] = "A"

    if fila != 0 and columna != 0:
        tauler[fila-1][columna-1] = "A"

    if fila != 0 and columna != 9:
        tauler[fila-1][columna+1] = "A"
    ### Marcar les cantonades com a aigua ###

    ### Marcar la resta com a aigua ###
    if tot:

        if fila != 9 and tauler[fila+1][columna] == 0:
            tauler[fila+1][columna] = "A"

        if fila != 0 and tauler[fila-1][columna] == 0:
            tauler[fila-1][columna] = "A"

        if columna != 9 and tauler[fila][columna+1] == 0:
            tauler[fila][columna+1] = "A"

        if columna != 0 and tauler[fila][columna-1] == 0:
            tauler[fila][columna-1] = "A"
    ### Marcar la resta com a aigua ###

def escollir_casella(tauler):
    
    """Aquesta és la funció principal del programa, que decideix entre
    escollir una casella aleatòria o buscar al voltant de l'últim vaixell
    trobat. També escull quan es marca l'aigua al voltant dels vaixells
    i quan s'escull la direcció."""

    # Marca aigua al voltant abans de tot per tal de treure caselles possibles
    for f in range(len(tauler)):
        for c in range(len(tauler[f])):
            
            # Si no està enfonsat marcarà només els cantons
            if tauler[f][c] == "X":
                marcar_aigua_al_voltant(tauler, f, c, False)
            
            # Si està enfonsat marcarà les 8 caselles del voltant
            elif tauler[f][c] == "E":
                marcar_aigua_al_voltant(tauler, f, c, True)

    # Al principi la casella és aleatòria
    x, y = casella_aleatoria(tauler)

    for f in range(len(tauler)):
        for c in range(len(tauler[f])):

            if tauler[f][c] == "X":

                cNord, cSud, cEst, cOest = caselles_del_voltant(tauler, f, c)
                # En cas que la casella sigui completament rodejada segueix a la següent
                if cNord != 0 and cSud != 0 and cEst != 0 and cOest != 0:
                    continue
                elif (cSud == "X" and cNord != 0) or (cEst == "X" and cOest != 0):
                    continue

                else:
                    # Aquí busca caselles al voltant i surt del loop per retornar la casella corresponent
                    buscar_direccions_possibles(tauler, f, c)
                    x, y = seguir_matant_barquitus(tauler, f, c)
                    break

    return x, y

def jugador_bo(tauler, dades={}):

    if "posicions" not in dades:
        dades["posicions"] = [(fila, columna) for fila, llista in enumerate(tauler)
                              for columna, _ in enumerate(llista)]
    if "darrera posicio" in dades:
        fila, columna = dades["darrera posicio"]
        print(fila, columna)
        print("Resultat:", tauler[fila][columna])
        for i in tauler:
            for j in i:
                print(j, end=" ")
            print("")
        print("\n\n")
    else:
        #Primera tirada (pq no hi ha darrera posició)
        fila = 0
        columna = 0

    fila, columna = escollir_casella(tauler)
    dades["darrera posicio"] = fila, columna   

    return (fila, columna), dades

###########################################################################
###########################################################################
###########################################################################

jugar()

mitjana = 0
vegades = 20
for i in range(vegades):
    torns, _ = jugar()
    mitjana += torns
print("Mitjana:", mitjana/vegades)
