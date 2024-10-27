import pandas as pd 
import numpy as np 
import plotly.graph_objects as go 
import plotly.express as px
import streamlit as st
from datetime import datetime
import seaborn as sns

from plotly.subplots import make_subplots

st.title("Tableau de Bord des Performances de Rameurs : Analyses et Visualisations")

st.markdown("<u>Introduction</u>", unsafe_allow_html=True)


# Texte d'introduction

st.markdown("""
Bienvenue sur notre tableau de bord dédié aux performances de 32 rameurs sur une distance totale de 2000 mètres. Ce tableau offre une vue détaillée des résultats individuels et des paramètres clés de la course, en vous permettant d'explorer chaque étape du parcours.

Les données sont analysées selon divers indicateurs, tels que la vitesse moyenne, le nombre total de coups de rame, le rythme cardiaque, et les segments intermédiaires de 500 mètres. Grâce à des graphiques et des calculs précis, vous pourrez observer les efforts de chaque rameur et comprendre comment les différentes stratégies et cadences influencent leur progression sur la distance complète.
""")

st.write("<u>Resultats globales des performances extraites des 8 serie de fichiers json constituant les resultats de 4 rameurs</u>",unsafe_allow_html=True)
st.markdown("Longueur_Moy2000 : Longueur moyenne sur 2000 m ")
st.markdown("vitesse_Moy2000 : Longueur moyenne sur 2000 m ")
st.markdown("vitesse_Moy_0 :  vitesse moyenne sur le premier split indicé 0 de 500m")
st.markdown("nombre_coup_rame_0 :  nombre de coup de rame sur le premier split 0 de 500m")
st.markdown("Longueur_Moy2000 :  Longueur moyenne sur le premier split de 500m ")
st.markdown("split_stroke_count0 : la cadence sur le split 0 500 m ")


# Chargement des données
result = pd.read_csv("C:/Users/pc/Documents/Dasbord/result.csv")
result=result.round(2)
result

st.sidebar.title("Mon équipe")
st.sidebar.markdown(" GNAMBA Frederic")
st.sidebar.markdown(" FALL Ousmane")
st.sidebar.markdown("TORO Illiace ")
st.sidebar.markdown("YOUMBI AKOUA derrick")



    


# Selection de choix du graphs

st.sidebar.title("Visualisation des distributions de performances")
selection = st.sidebar.selectbox("Sélectionnez le type de graphique",
                                    options=["Histogramme", "Boîte à Moustache"],
                                    key="1")

# definition d'un dictionnaire comprenant en valeurs de listes des variables par splits qui sera utilsé pour l'affichage des graphs

var_dict = {
    "Cadence par split de 500m": ["split_stroke_rate0", "split_stroke_rate1",
                                 "split_stroke_rate2", "split_stroke_rate3"],
    "Longueur moyenne par split": ["Longueur_Moy_0", "Longueur_Moy_1",
                                  "Longueur_Moy_2", "Longueur_Moy_3"],
    "Temps moyen sur chaque split": ["split_time00", "split_time11", "split_time22",
                           "split_time33"]
}

def plot_distribution(feature, selection):
  

    if selection == "Histogramme":
        fig = make_subplots(rows=1, cols=len(features), subplot_titles=features)

        for i, feature in enumerate(features):
            fig.add_trace(
                go.Histogram(
                    x=result[feature],
                    marker_color='blue',
                    name=feature,
                    nbinsx=30  
                ),
                row=1, col=i+1
            )

        fig.update_layout(title_text="Distribution des performances", showlegend=False)

    elif selection == "Boîte à Moustache":
        fig = make_subplots(rows=1, cols=len(features), subplot_titles=features)

        for i, feature in enumerate(features):
            fig.add_trace(
                go.Box(
                    y=result[feature],
                    name=feature,
                    fillcolor='lightblue'  
                ),
                row=1, col=i+1
            )

        fig.update_layout(title_text="Boîtes à Moustache des performances")

    else:
        st.error("Type de graphique non reconnu. Veuillez choisir 'Histogramme' ou 'Boîte à Moustache'.")
        return None  # Indicate error

    return fig






select_var_group = st.sidebar.radio(
    "Sélectionnez un groupe de fonctionnalités",
    list(var_dict.keys())

)

if select_var_group:
    select_colonne = var_dict[select_var_group]
    fig = plot_distribution(select_colonne,selection)
    if fig:
        st.plotly_chart(fig)
            


cadences = []
longueurs = []
vitesse = []

# Collecter les données pour les quatre splits dans une seule colonne poour prendre en charge toutes les series
for i in range(4): 
    cadences.extend(result[f'split_stroke_rate{i}'])
    longueurs.extend(result[f'Longueur_Moy_{i}'])
    vitesse.extend(result[f'vitesse_moyenne_{i}'])

# Créer un DataFrame avec les données concaténées
Res = pd.DataFrame({
    "longueur_moy": longueurs,
    "cadences": cadences,
    "vitesse": vitesse
})

st.write("**Données globales de la longueur moyenne , cadence et la vitesse moyenne pour chaque split:** ",unsafe_allow_html=True)
st.markdown("***Nous avons ici une consolidation de tous les splits par rameurs pour chaque variables (cadence, longueur moyenne et vitesse moyenne). Cette apporche pour mesurer la correlation entre les trois variables peut conduire a une perte d'informations sur le suivi par rameur en masquant les differences individuelles. Une etude par rameur sera faite au dessous")
st.dataframe(Res)

st.write("**Données de la correlation entre longueur moyenne , cadence et la vitesse moyenne pour chaque split:** ",unsafe_allow_html=True)

#corr=Res.drop(columns="vitesse_moyenne_2000").corr()
corr= Res.corr()
st.dataframe(corr)

st.markdown(""" Au regards des correlations, nous pouvons constater qu'il y a une correlation positive(0.683) entre la longueur et la vitesse
Cela dit, une augmentation de la lougueur moyenne augmente est associée a une vitesse plus elevée. Aussi, nous observons une correlation negative -0.653 entre la longueur moyenne et la cadence par coup. cela dit, au fur et a mesure que la cadence 
augmente, la longueur a tendance a diminuer. Tandis qu'il y a une faible correlation positive (0.093) entre la vitesse et la cadence
Cela signifie qu'il n ya presque pas de relation entre la vitesse et la cadence. La vitesse ne semble donc pas dépendre directement de la cadence, mais pourrait être davantage 
influencée par la longueur de chaque coup. Lorsqu'on fait varier la cadence et la vitesse, les deux mesures auront un effet contraire sur la longueur moyenne, qui au tendance a limiter l'evolution de la longueur.""")



st.write("**Graphs du nuage de points entre les Données de la longueur moyenne , cadence pour chaque split :**",unsafe_allow_html=True)
st.markdown("Notons que chaque point de données est une mesure correspondante sur un intervalle de 500m. 32 rameurs pour 4 splits d'ou un nuage de points de 128 points.")


# Visionnage de la relation entre la cadence et la longueur moyenne avec la couleur en fonction de la vitesse

fig = px.scatter(
    Res, x="cadences", y="longueur_moy",
    color="cadences",
    color_continuous_scale="Viridis", 
    title="Nuage de points des Cadences et Longueur Moyenne par Vitesse"
)

# Affichage du graphique 

st.plotly_chart(fig)

# Identifier la ligne de vitesse maximale
vitess_index = Res["vitesse"].idxmax()
ligne_Vitesse_Max = Res.iloc[vitess_index]

# Affichage de la ligne avec la vitesse maximale

st.write("<u>**Données de la vitesse maximale :**</u>",unsafe_allow_html=True)
st.dataframe(ligne_Vitesse_Max.to_frame().T)

# Visionnage de la relation entre vitesse moyenne , la longueur moyenne et la cadence

#cadences= st.slider("Sélectionnez la cadence", min_value=20, max_value=60, value=30, step=1)
#vitesse= st.slider("Sélectionnez la vitesse", min_value=4.0, max_value=25.0, value=5.5, step=0.1)

fig_3d = px.scatter_3d(
    Res, x="cadences", y="longueur_moy", z="vitesse",
    color="vitesse",
    color_continuous_scale="Viridis",
    title="Nuage de points 3D des Cadences, Longueur Moyenne et Vitesse"
)
st.plotly_chart(fig_3d)




st.write("**Données par rameur de la longueur moyenne , cadence et la vitesse moyenne pour chaque split:** ",unsafe_allow_html=True)
st.markdown("Nous effectuons dans cette partie une etude par rameur. Nous allons observer la correlation par split de 500 de chaque variable")

result0=result[["Participant","time","vitesse_moyenne_2000","vitesse_moyenne_0","vitesse_moyenne_1","vitesse_moyenne_2","vitesse_moyenne_3","split_stroke_rate0","split_stroke_rate1","split_stroke_rate2",
                "split_stroke_rate3","Longueur_Moy_0","Longueur_Moy_1","Longueur_Moy_2","Longueur_Moy_3","split_time00","split_time11","split_time22","split_time33"]].round(2)

st.dataframe(result0)

st.write("**Correlation entre les variables par split**")

corr=result0.select_dtypes("number").drop(columns="vitesse_moyenne_2000").corr()
corr




fig= px.imshow(corr,text_auto=True, title=("Matrice de Correlation par split"))
st.plotly_chart(fig)

st.write("**Interpretation**")
st.markdown("Nous constatons une tres forte correlation negative entre la vitesse moyenne et le temps moyen sur chaque splits. Cela est évident, car un temps plus long pour parcourir la distance indique une vitesse plus lente.")
st.markdown("De meme, il y a une tres forte correlation negative entre la longueur moyenne et la cadence sur chaque split. Cela conforte notre affirmation sur l'etude de la correlation avec les données consolidées.Cette analyse détaillée par split permet d'affiner la compréhension des relations entre ces variables, en montrant comment chaque split contribue à la performance globale des rameurs")

st.write("**Considerons ici les 5 rameurs les plus performants et les 5 derniers avec les plus faibles temps moyen sur 2000m pour essayeer de mieux comprendres les analyses.**")


result1=result[["Participant","time","vitesse_moyenne_2000","split_stroke_rate0","split_stroke_rate1","split_stroke_rate2",
                "split_stroke_rate3","Longueur_Moy_0","Longueur_Moy_1","Longueur_Moy_2","Longueur_Moy_3","vitesse_moyenne_0","vitesse_moyenne_1","vitesse_moyenne_2","vitesse_moyenne_3"]][result["time"]<450].sort_values(by="time",ascending = True)
result1

result2=result[["Participant","time","vitesse_moyenne_2000","split_stroke_rate0","split_stroke_rate1","split_stroke_rate2",
                "split_stroke_rate3","Longueur_Moy_0","Longueur_Moy_1","Longueur_Moy_2","Longueur_Moy_3","vitesse_moyenne_0","vitesse_moyenne_1","vitesse_moyenne_2","vitesse_moyenne_3"]][result["time"]>560].sort_values(by="time",ascending = True)
result2


st.markdown("Le rameur le plus performant, Maxime, a montré une progression notable de sa vitesse au cours de la course, mettant une forte intensité dans les deux derniers segments de 500 m. Dans ces portions, il a atteint respectivement des temps de 97,6 et 92,1 secondes, ce qui correspond à des vitesses élevées de 18,44 et 19,54 km/h. Au fur et à mesure que sa cadence augmentait (atteignant 29 et 34 coups par minute dans ces deux segments), sa longueur par coup de rame a diminué, passant à 10,59 m et 9,58 m. Cela suit une logique cohérente : plus la cadence est élevée, plus la longueur de chaque coup de rame tend à diminuer, ce qui, à son tour, augmente la vitesse globale de progression.")
st.markdown("Parmi les participants, Maxime se distingue en appliquant une technique modérée en début de course, avec une cadence et une vitesse mesurées. Il a compensé cela par une longueur de rame plus importante, et a progressivement accéléré son rythme au fil des segments. Maxime est le seul à avoir maintenu une progression croissante jusqu’à la fin de la série, optimisant ainsi la gestion de son énergie et de sa puissance.")
st.markdown("Maintenir une vitesse stable tout au long de la course pour préserver la régularité,Augmenter progressivement la vitesse et la cadence tout en conservant la puissance pour optimiser la longueur de rame.")
st.markdown("À l’inverse, les rameurs ayant obtenu des temps plus élevés affichent des vitesses basses, probablement en raison d'une puissance fournie insuffisante. Cela est particulièrement évident chez les derniers, comme Amaury et Tom, dont les faibles performances peuvent être attribuées à une cadence élevée mais à une longueur de rame faible, limitant ainsi l’efficacité de leur propulsion.")
