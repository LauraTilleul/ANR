# ANR
Analyse données projets ANR 2006-2016

Les scripts python utilisés pour obtenir les fichiers de données (.json, .csv) contenus dans static/ sont dans le dossier scripts_python. 

Les données étant fixes il n'est pas nécessaire de réexecuter ces scripts. Les scripts ont à priori un nom parlant mais au cas où j'ai laissé en commentaire dans webapp.py les appels aux différents scripts pour voir de quelles données ils sont responsables.

Les fichiers de données ainsi obtenues sont utilisées pour différents graphes. Les codes HTML sont dans view/templates. Les scripts js éventuels sont dans static/script.

Les données "originales" i.e qui ne sont pas obtenues par un script doivent être dans original/static. Il s'agit du fichier csv de base ainsi que d'un fichier texte utilisé pour le travail avec TF/IDF. Les données étant trop lourdes elles sont en zip dans static/original.zip, à décompresser


Depuis le menu : 

-> Statistiques de base

sélectionner une option dans le menu déroulant pour afficher le graphe correspondant.
les données manquantes sont volontairement affichées, mais grisées.

-> Scatter Plot

un point représente un projet. 

-> Répartition des genres

cliquer sur une barre pour accéder au top des programmes i.e les programmes qui comptabilisent le plus de projets.
    
    -> Top Programmes (8 programmes max) (non terminé)
    possibilité de sélectionner une année
    passer sur une barre pour afficher le nom du programme et le nombre de projets associés.

-> Bubble Chart

représentation de 50 termes les + pertinents dans les résumés de projets, obtenus en utilisant TF/IDF

-> Matrice de Co-occurences 

représentation de 50 termes les + pertinents dans les résumés et leurs relations, obtenus en utilisant TF/IDF.
possibilité de trier par nom, fréquence, cluster

clusters : un point coloré <=> les 2 termes sont liés (apparaissent dans mêmes projets) et appartiennent au même cluster.

        un point non coloré (gris/noir) <=> relation entre les termes, mais n'appartiennent pas au même cluster
        
        Rien <=> pas de relation entre les termes
-   > plus un point est foncé plus la liaison est forte

-> Graphe des partenaires

algorithme de force pour la disposition des noeuds. Par souci de lisibilité sélection des 30 "meilleurs" partenaires i.e ceux qui participent à un max de projets. 

passer sur/ cliquer sur un noeud permet d'afficher ses voisins.

drag&drop permet de déplacer un noeud (algo de force influence le positionnement)

faire glisser le petit rond noir en bas à gauche vers la droite pour sélectionner les liaisons (arêtes) les plus fortes. 

cliquer sur l'arrière plan pour "reset" après avoir cliqué sur un noeud. 
