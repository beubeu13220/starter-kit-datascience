
import pandas as pd 
path= "/home/brehelin/Documents/Kit Data Science/starter-kit-datascience/alexandre-brehelin/Lesson 6/"
data = pd.read_csv(path + "aliments.csv",sep="\t")

data_keep_prt_name = data[~data["product_name"].isnull()]

list_name_variable = [ 
"product_name",
"generic_name",
"categories_fr",
"nutrition_grade_fr",
"main_category_fr",
"labels_fr",
"sugars_100g",
"fat_100g",
"saturated-fat_100g",
"sodium_100g"
]

#Glucose et sucrose taux faible et peu renseigné
#Frutose peu renseigné mais taux élevé mais équivalement à celui du sucre

#Quand fat est renseigné le saturated l'est aussi mais pas inversement 

data_clean_variable = data_keep_prt_name.loc[:,list_name_variable]

#On corrige deux valeurs anormal de valeur de sucre 

data_clean_variable.loc[data_clean_variable["sugars_100g"]<0,"sugars_100g"]=0
data_clean_variable.loc[data_clean_variable["sugars_100g"]>100,"sugars_100g"]=100

idx_fat_drop = data_clean_variable[data_clean_variable["fat_100g"]>100].index
data_clean_variable = data_clean_variable.drop(idx_fat_drop)

idx_sodium_drop = data_clean_variable[data_clean_variable["sodium_100g"]>100].index
data_clean_variable = data_clean_variable.drop(idx_sodium_drop)

#on crée les indicateurs salé,...

data_clean_variable["too_sugar"] = 0
data_clean_variable["too_fat"] = 0
data_clean_variable["too_sodium"] = 0

avg_sugar = data_clean_variable["sugars_100g"].mean()
avg_fat = data_clean_variable["fat_100g"].mean()
avg_sodium = data_clean_variable["sodium_100g"].mean()

data_clean_variable["too_sugar"][data_clean_variable["sugars_100g"]>avg_sugar]=1
data_clean_variable["too_fat"][data_clean_variable["fat_100g"]>avg_fat]=1
data_clean_variable["too_sodium"][data_clean_variable["sodium_100g"]>avg_sodium]=1


df = data_clean_variable
data_study = df[ (df.too_sugar==1) |  (df.too_fat==1) | (df.too_sodium==1)]

#Permet de constater que les aliments sont classer par grade et que les plus mauvais sont les aliments e
pd.crosstab(data_study["too_sugar"],data_study["nutrition_grade_fr"])

#Obtenir les top produits sucrée
def top_product(label):
	top = (data_study["generic_name"].where(data_study[label]==1).value_counts()>6)
	top =  top.index[top.values]
	return pd.DataFrame(top.values,columns=[label])

top_sugar = top_product("too_sugar")
top_sodium = top_product("too_sodium")
top_fat = top_product("too_fat")


data_prdt_target = pd.concat([top_sugar,top_sodium,top_fat],axis=1)
data_prdt_target.to_csv(path + "top_produit_cible.csv")

def occurency_top(label):
	numerator = data_study.groupby(label)[label].count()[1] 
	b_numerator = len(data_study[label]) 
	return (numerator / b_numerator) * 100

#Les produits fat et sucré sont plus impapacté que les produits salé par la mesure 
nb_sugar =  occurency_top("too_sugar") 
nb_sodium =  occurency_top("too_sodium") 
nb_fat =  occurency_top("too_fat") 

#On crée 3 tables pour export chaque top produit 

data_conso_home = pd.ExcelFile(path+"irsocbdf11_TM105.xls").parse("irsocbdf11_TM105")

y = data_conso_home.ix[range(61)]

vec = [ i for i in y.index if len(y.loc[i,y.columns[0]].split("-")[0])==6] 
vec_2 =[ i for i in y.index if len(y.loc[i,y.columns[0]].split("-")[0])==3] 
 
vec_2.extend(vec) 
y = y.loc[vec_2,:]

for i in range(1,len(y)):

	y.iloc[i,1:] = y.iloc[i,1:]/y.iloc[0,1:] *100

df = y.reset_index() 

df.loc[1:,"TYPE DE MÉNAGE"][(df.loc[1:,"Personnes seules"]>df.loc[1:,"Ensemble"]).values]       

"""


sodium_100g*2,5

 Multiplier la quantité de graisse par 9. Par exemple, si l'étiquette indique que l'aliment 
 contient 6 g de matières grasses, vous multipliez par 6 9. Cela vous donnera 54, 
 ce qui signifie que la nourriture a 54 calories proviennent de matières grasses
 """