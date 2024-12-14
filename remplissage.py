import sqlite3, random

# ouverture/initialisation de la base de donnee 
conn = sqlite3.connect('mydb.db') #on cree une connexion
conn.row_factory = sqlite3.Row
c = conn.cursor() #creer une connexion ( ce qui  nous permettra de communiquer avec la base de donnee a travers les requettes sql)

id = random.randint(1,2)
N = 10
if id ==1:
    L=[round(random.uniform(20,38),2) for x in range(N)] 
elif id==2:
    L=[random.randint(0,1) for x in range(N)]

req1 ="INSERT INTO Mesure (valeur , id_capteur) VALUES (?,?)" # cette requette c'est pour les mesures
for valeur in L:
    c.execute(req1, (valeur, id))
conn.commit() # permet d'envoyer la requette 

liste_facture=[
    "Eau",
    "Electricité",
    "Loyer",
    "Déchets",
    "Internet",
    "Assurance"
]

req2 ="INSERT INTO Facture(Type_facture,montant, Valeur_consommee,id_logement) VALUES(?,?,?,?)"
for x in range(N):
    c.execute(req2,(random.choice(liste_facture),round(random.uniform(20,38),1), round(random.uniform(20,38),1),2)) # c'est les facture pour le logement 2

# fermeture
conn.commit() # permet d'envoyer la requette 
conn.close() # on ferme la connexion