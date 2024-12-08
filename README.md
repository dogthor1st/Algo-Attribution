# Attribution Optimale des Sujets

Ce projet utilise l'algorithme hongrois pour répartir des sujets entre différents groupes en fonction de leurs préférences. 

## Fonctionnalités
- Lecture des préférences depuis un fichier CSV.
- Utilisation de l'algorithme hongrois pour trouver une attribution optimale.
- Calcul et affichage de la satisfaction totale.

## Utilisation
1. Préparez un fichier CSV contenant les préférences des groupes.
2. Lancez le script `main.py`.

## Exemple de fichier CSV
```csv
N° Groupe,[Sujet 1],[Sujet 2],[Sujet 3],[Sujet 4]
0,1,2,3,4
1,2,3,4,1
2,3,4,1,2
3,4,1,2,3
```
