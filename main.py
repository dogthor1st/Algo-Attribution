from scipy.optimize import linear_sum_assignment
import numpy as np
import pandas as pd

def generate_preference_matrix(preferences, n_subjects):
    """
    Génère une matrice de préférences basée uniquement sur les rangs.
    """
    n_people = len(preferences)
    preference_matrix = [[0] * n_subjects for _ in range(n_people)]

    for i, person_prefs in enumerate(preferences):
        for rank, subject in enumerate(person_prefs, 1):
            if 0 <= subject < n_subjects:
                preference_matrix[i][subject] = n_subjects - rank + 1  # Rangs simples

    return preference_matrix

def assign_preferences(preference_matrix):
    """
    Assigne les options aux personnes pour maximiser la satisfaction totale.
    """
    cost_matrix = -np.array(preference_matrix)  # L'algorithme minimise le coût
    row_indices, col_indices = linear_sum_assignment(cost_matrix)
    return list(zip(row_indices, col_indices))

# Charger le fichier CSV
file_path = "./preferences.csv"
data = pd.read_csv(file_path, header=None)

# Extraire les noms des sujets (première ligne)
subject_names = data.iloc[0, 1:].tolist()

# Extraire les préférences (ignorer la première ligne et la première colonne)
preferences = data.iloc[1:, 1:].reset_index(drop=True)
preferences = preferences.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
preferences_ordered = preferences.values.tolist()

# Vérification du nombre de groupes et de sujets
n_subjects = len(subject_names)
n_groups = len(preferences_ordered)

if n_groups != n_subjects:
    print(f"Erreur : Le nombre de groupes ({n_groups}) est différent du nombre de sujets ({n_subjects}).")
    exit()

# Générer la matrice de préférences
preference_matrix = generate_preference_matrix(preferences_ordered, n_subjects)

# Calculer l'affectation optimale
assignments = assign_preferences(preference_matrix)

# Afficher les résultats
print("\nMatrice de préférences :")
for row in preference_matrix:
    print(row)

print("\nAffectations optimales :")
print(f"{'Groupe':<10}{'Sujet':<50}")
print("-" * 60)
for group, subject in assignments:
    subject_name = subject_names[subject]
    print(f"{group:<10}{subject_name:<50}")

# Validation des affectations et calcul des classements réels
total_satisfaction = 0
satisfaction_details = []

print("\nValidation des affectations :")
for group, subject in assignments:
    try:
        # Recherche directe du classement dans le CSV
        actual_ranking = preferences_ordered[group][subject]
        total_satisfaction += actual_ranking
        satisfaction_details.append((group, subject, actual_ranking))
        print(f"Groupe {group} : Sujet attribué [{subject_names[subject]}], Classement réel : {actual_ranking}")
    except IndexError:
        print(f"Groupe {group} : Sujet attribué [{subject_names[subject]}], Classement non trouvé dans les préférences.")

# Afficher les détails
print("\nDétails de satisfaction :")
print(f"{'Groupe':<10}{'Sujet':<50}{'Classement':<10}")
print("-" * 70)
for group, subject, priority in satisfaction_details:
    subject_name = subject_names[subject]
    print(f"{group:<10}{subject_name:<50}{priority:<10}")

# Calcul du score parfait et du score maximum
num_groups = len(preferences_ordered)
perfect_score = num_groups  # Si chaque groupe obtient son 1er choix
max_score = sum(len(preferences_ordered[0]) for _ in range(num_groups))  # Si chaque groupe obtient son dernier choix
average_score = total_satisfaction / num_groups

# Déterminer l'interprétation qualitative
if total_satisfaction <= perfect_score * 2:
    interpretation = "Excellente répartition (la plupart des groupes ont obtenu leurs 1ers choix)"
elif total_satisfaction <= perfect_score * 4:
    interpretation = "Bonne répartition (les groupes ont obtenu des choix proches de leurs préférences)"
elif total_satisfaction <= max_score * 0.75:
    interpretation = "Répartition moyenne (certains groupes ont des choix éloignés)"
else:
    interpretation = "Répartition suboptimale (beaucoup de groupes ont des choix éloignés)"

# Affichage final
print(f"\nSatisfaction totale : {total_satisfaction}")
print(f"- Score parfait (tous les 1ers choix) : {perfect_score}")
print(f"- Maximum possible (tous les derniers choix) : {max_score}")
print(f"- Moyenne par groupe : {average_score:.2f}")
print(f"- Interprétation : {interpretation}")

