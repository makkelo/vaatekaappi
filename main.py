# Asetukset:

vaatetiedosto = 'talvivaatteet.csv'
kosketustiedosto = 'vaatekosketukset.csv'
tulostiedosto = 'vaateyhdistelmat_20231104.csv'
maxi = 3 # kuinka monta väriä yhdistelmässä saa enintään olla
mini = 2 # kuinka monta väriä yhdistelmässä on vähintään oltava

# Koodi: funktiot:

def transpose(taulukko):
    kaanteinentaulukko = []
    vanhaleveys = len(taulukko)
    vanhakorkeus = len(taulukko[0])
    for kertaa in range(vanhakorkeus):
        kaanteinentaulukko.append([])
    uusix = 0
    uusiy = 0
    vanhax = 0
    vanhay = 0
    for kertaa in range(vanhakorkeus * vanhaleveys):
        kaanteinentaulukko[uusix].append(taulukko[vanhax][vanhay].strip())
        uusix += 1
        if uusix == vanhakorkeus:
            uusix = 0
            uusiy += 1
        vanhay += 1
        if vanhay == vanhakorkeus:
            vanhay = 0
            vanhax += 1
    return kaanteinentaulukko

def lisaarivit(taulukko: list, vaatetyyppienvarit: list) -> list:
    sarakkeita = len(taulukko)
    uusitaulukko = []
    uusisarake = []
    for sarake in range(sarakkeita):
        uusitaulukko.append([])
        for rivi in range(len(taulukko[0])):
            for kertaa in range(len(vaatetyyppienvarit[sarakkeita])):
                uusitaulukko[sarake].append(taulukko[sarake][rivi].strip())
            for kertaa in range(len(vaatetyyppienvarit[sarakkeita])):
                uusisarake.append(vaatetyyppienvarit[sarakkeita][kertaa].strip())
    uusitaulukko.append(uusisarake)
    return uusitaulukko

def suodatakaanteinentaulukko(taulukko, max, min) -> list:
    for rivi in taulukko:
        rivi.append([]) # lisätään tila värimäärälle
    #print(taulukko)
    # laske rivien värimäärä
    for rivi in taulukko:
        kaytetytvarit = []
        for vari in rivi:
            #print(vari)
            if not vari in kaytetytvarit and not vari == []:
                #print('lisätty', vari)
                kaytetytvarit.append(vari.strip())
            else:
                continue
        rivi[len(rivi)-1] = len(kaytetytvarit)
        #print(rivi)
    # pudota liialliset ja liian vähäiset rivit
    suodatettutaulukko = []
    #print('->', taulukko, '<-')
    for rivi in taulukko:
        if rivi[len(rivi)-1] <= max and rivi[len(rivi)-1] >= min:
            #print('rivissä värejä', rivi[len(rivi)-1])
            suodatettutaulukko.append(rivi[0:(len(rivi)-1)])
            #suodatettutaulukko.append(rivi[0:(len(rivi))])
    for i in range(len(suodatettutaulukko)): # vikat luupit poistavat ylimääräiset välilyönnit
        for j in range(len(suodatettutaulukko[i])):
            suodatettutaulukko[i][j] = suodatettutaulukko[i][j].strip()
    return suodatettutaulukko

def kosketuslist(vaate) -> list:
    for i in range(len(kosketukset)):
        if vaate == kosketukset[i][0]:
            return kosketukset[i][1]
    return 0


def kerrovarit2(vaate, i, rivi) -> list:
    varit = []
    for vaate in kosketuslist(vaatetyypit[i]):
        #print(vaate, maxmin[i][vaatetyypit.index(vaate.strip())], '.')
        #print(vaatetyypit.index(vaate.strip()))
        varit.append(rivi[vaatetyypit.index(vaate.strip())])
    return varit



# Koodi: pääohjelma:

vaatteet = []
with open(vaatetiedosto) as kaappifile:
    for rivi in kaappifile:
        vaatteet.append(rivi.strip().replace('"', '').split(';'))
print('vaatteet:', vaatteet[1:])

vaatetyypit = []
for i in range(1, len(vaatteet)):
    if vaatteet[i][0] not in vaatetyypit:
        vaatetyypit.append(vaatteet[i][0].strip())
print('vaatetyypit:', vaatetyypit)

varit = []
for i in range(1, len(vaatteet)):
    if vaatteet[i][1] not in varit:
        varit.append(vaatteet[i][1].strip())
print('värit:', varit)

vaatetyyppienvarit = []
for i in range(len(vaatetyypit)):
    vaatetyyppienvarit.append([])
    for j in range(1, len(vaatteet)):
        #print(vaatetyypit[i], vaatteet[j][0])
        if vaatetyypit[i] == vaatteet[j][0]:
            vaatetyyppienvarit[i].append(vaatteet[j][1].strip())
print('vaatetyyppien värit:', vaatetyyppienvarit)

vareja = []
for sarake in vaatetyyppienvarit:
    for vari in sarake:
        if not vari in vareja:
            vareja.append(vari)
print(f'erilaisia värejä yhteensä: {len(vareja)}')

yhdistelmienmaara = 1
for i in range(len(vaatetyyppienvarit)):
    yhdistelmienmaara *= len(vaatetyyppienvarit[i])
print('vaateyhdistelmiä:', yhdistelmienmaara)

# Erittele seuraavaksi kaikki mahdolliset väriyhdistelmät

uusitaulukko = []
uusitaulukko.append(vaatetyyppienvarit[0][:])

for i in range(len(vaatetyyppienvarit)-1):
    uusitaulukko = lisaarivit(uusitaulukko, vaatetyyppienvarit)


# Suodatetaan teoreettisia vaihtoehtoja.

# 1. Liikaa tai liian vähän värejä sisältävät suodatetaan.

suodatettava = transpose(uusitaulukko)

maxmin = suodatakaanteinentaulukko(suodatettava, maxi, mini)

print('maxmin sisältää ', len(maxmin), 'väriyhdistelmää, jos sallittuja värejä yhdessä yhdistelmässä on', f'{mini}-{maxi}')

# 2. Suodatetaan pois väriyhdistelmät, joissa vierekkäiset vaatteet ovat samaa väriä.

kokokosketukset = []
with open(kosketustiedosto) as kosketusfile:
    for rivi in kosketusfile:
        kokokosketukset.append(rivi.strip().replace('"', '').split(';'))
for sarake in kokokosketukset:
    temp = sarake[1].strip().split(',')
    sarake.pop(1)
    sarake.append(temp)
kosketukset = kokokosketukset[1:]

kosketuksettomat = []
# käy läpi vaateyhdistelmät rivi riviltä
for rivi in maxmin:
    varitormays = False
    for i in range(len(vaatetyypit)):
        if rivi[i] in kerrovarit2(vaatetyypit[i], i, rivi):
            varitormays = True
    if not varitormays:
        kosketuksettomat.append(rivi)


print('kosketuksettomat sisältää', len(kosketuksettomat), 'väriyhdistelmää')

'''
print()
print(vaatetyypit)
for rivi in kosketuksettomat:
    print(rivi)
'''

# jos haluat sallia, että housut ja takki ovat samaa väriä, muokkaa kosketustaulukosta, että takki ei koske housuja ja housut eivät koske takkia.

rivi = ''
with open('vaateyhdistelmät_20231024.csv', 'w') as valmisfile:
    for cell in vaatetyypit:
        rivi += cell + ';'
    rivi = rivi[0:-1]
    valmisfile.write(f'{rivi}\n')
    rivi = ''
    for line in kosketuksettomat:
        for cell in line:
            rivi += cell + ';'
        rivi = rivi[0:-1]
        valmisfile.write(f'{rivi}\n')
        rivi = ''

import pandas as pd

df = pd.DataFrame(kosketuksettomat, columns = vaatetyypit)

print(df)

df.to_csv(tulostiedosto, index=False, sep=';')