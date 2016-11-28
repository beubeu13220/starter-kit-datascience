
# Peut-on établir un lien entre la densité de médecins par spécialité  et par territoire et 
# la pratique du dépassement d'honoraires ? 
# Est-ce  dans les territoires où la densité est la plus forte que les médecins  pratiquent
#  le moins les dépassement d'honoraires ? 
# Est ce que la densité de certains médecins / praticiens est corrélé à la densité de
#  population pour certaines classes d'ages (bebe/pediatre, personnes agées / infirmiers etc...) ?

	
import pandas as pd

#Import des tables
path = "/home/brehelin/Documents/Exercice Hackathon Santé Miglietti/"
data = pd.read_csv(path+"R201501.CSV",sep=";",encoding="ISO-8859-1")

data_med = pd.read_csv(path+"donne_med.csv",sep=";",skiprows=5,encoding="Latin_")

data_density_reg = pd.ExcelFile(path+"estim_pop.xls").parse("Feuille1")

#Sur data on conserve certaine colonne et limite l'étude à 1000 lignes
columns = ["cpl_cod","dep_mon","region", "l_region","exe_spe","exe_spe1","pre_spe","pre_spe","rec_mon"]
data = data.loc[:,columns]

#On normalise les dépassements d'honoraires 
data["dep_mon"]=data["dep_mon"].str.replace(".","").str.replace(",",".")
data["dep_mon"]=data["dep_mon"].astype(float)

#Depassement par region
data.groupby("region")["dep_mon"].sum()

#Depassement par region et specialité
data.groupby(["region","exe_spe1"])["dep_mon"].sum()


#On normalise les nom des colonnes entre data et data_med
data_med.columns=["region","exe_spe1","age","nb"]
#On garde seulement les régions
data_med=data_med[data_med["region"]!="FRANCE ENTIERE"]
data_med=data_med[data_med["region"]!="FRANCE Métropolitaine"]

data_density_reg = data_density_reg[data_density_reg["region"]!="France métropolitaine"]
data_density_reg = data_density_reg[data_density_reg["region"]!="France métropolitaine et DOM"]
data_density_reg = data_density_reg[data_density_reg["region"]!="DOM"]


#On crée une norme pour les régions
#On regarde dans une liste les régions des deux tables
#Pour ensuite créer un dict normalisé des régions 
list_reg_data_med = list(set(data_med["region"].tolist()))
list_reg_data_med = [t.replace("\x92"," ").lower() for t in list_reg_data_med]

list_reg_data = list(set(data["l_region"].tolist()))
list_reg_data = [t[3:].lower() for t in list_reg_data]

data["l_region"] = data["l_region"].apply(lambda x : x[3:].lower())
data_med["region"] = data_med["region"].apply(lambda x : x.replace("\x92"," ").lower())
data_density_reg["region"] = data_density_reg["region"].apply(lambda x : x.replace("Î","i").replace("'"," ").lower())


dict_reg = { 'centre' : 'centre-val de loire',
'guadeloupe': 'guadeloupe',
'rhone alpes' : 'auvergne-rhône-alpes',
'auvergne':  'auvergne-rhône-alpes',
'ile-de-france': 'ile-de-france',
'bourgogne' :'bourgogne-franche-comté', 
'franche comte' : 'bourgogne-franche-comté',
'basse normandie' : 'normandie', 
'haute normandie' : 'normandie',
'mayotte':'mayotte',
"provence alpes cote d'azur" : 'provence-alpes-côte d azur',
 'languedoc roussillon' : 'languedoc-roussillon-midi-pyrénées', 
 'midi pyrenees' : 'languedoc-roussillon-midi-pyrénées',
 'reunion': 'la réunion' ,
 'pays de la loire': 'pays de la loire',
 'guyane': 'guyane',
 'alsace' : 'alsace-champagne-ardenne-lorraine', 
 'champagne ardenne' : 'alsace-champagne-ardenne-lorraine', 
 'lorraine' : 'alsace-champagne-ardenne-lorraine',
 'aquitaine' : 'aquitaine-limousin-poitou-charentes',
 'limousin' : 'aquitaine-limousin-poitou-charentes',
 'poitou charentes' : 'aquitaine-limousin-poitou-charentes',
 'corse':'corse',
 'bretagne':'bretagne',
 'martinique':'martinique',
 'picardie' : 'nord-pas-de-calais-picardie',
 'nord pas de calais':'nord-pas-de-calais-picardie'
 }

#apply dict de normélisation
data["l_region"]=data.l_region.replace(dict_reg)


#Nord pas de calais
#centre val de loir

data_density_reg.loc[data_density_reg["region"]=="nord - pas-de-calais-picardie","region"] = 'nord-pas-de-calais-picardie'
data_density_reg.loc[data_density_reg["region"]=="centre-val-de-loire","region"] = 'centre-val de loire'

#Normalisation des spécialités 

dict_spe = {
"Chirurgie plastique reconstructrice et esthétique":	99,
"Recherche médicale":	99,
"Néphrologie":	35,
"Cardiologie et maladies vasculaires":	3,
"Médecine physique et réadaptation":	31,
"Médecine interne":	9,
"Chirurgie urologique":	4,
"Santé publique et médecine sociale":	80,
"Radiothérapie":	6,
"Dermatologie et vénéréologie":	5,
"Endocrinologie et métabolisme":	42,
"Ensemble des spécialités d'exercice":	99,
"Psychiatrie":	17,
"Gynécologie-obstétrique":	7,
"Rhumatologie":	14,
"Médecine nucléaire":	99,
"Médecine du travail":	99,
"Anatomie et cytologie pathologiques":	37,
"Gériatrie":	99,
"Chirurgie maxillo-faciale et stomatologie":	18,
"Biologie médicale":	38,
"Chirurgie viscérale et digestive":	99,
"Génétique médicale":	99,
"Chirurgie générale":	4,
"Pédiatrie":	12,
"Chirurgie infantile":	4,
"Spécialistes":	99,
"Généralistes":	1,
"Ophtalmologie":	15,
"Chirurgie orthopédique et traumatologie":	27,
"Médecine générale":	1,
"Radiodiagnostic et imagerie médicale":	6,
"Chirurgie thoracique et cardio-vasculaire":	3,
"Gastro-entérologie et hépatologie":	8,
"ORL et chirurgie cervico-faciale":	11,
"Réanimation médicale":	2,
"Gynécologie médicale":	7,
"Oncologie option médicale":	99,
"Hématologie":	99,
"Pneumologie":	13,
"Neurochirurgie":32,
"Chirurgie vasculaire":	3,
"Neurologie":32,
"Anesthésie-réanimation":	2
}
#large vers fin
data_sp  = data.loc[:,["exe_spe","exe_spe1"]]
data_med["exe_spe1"]=data_med.exe_spe1.replace(dict_spe)


