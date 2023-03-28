# Partie 2 -a

## Question

Imagine maintenant que l'on a 100 000 000 de créneaux et qu'on a 1000 nouveaux
créneaux qui arrivent par seconde.

Quelles limites identifies-tu dans ton script précédent et que proposerais-tu
d’implémenter, en sachant que l'on souhaite le résultat précédent dans un
délai raisonnable ?

## Les Limites

Dans le script précédent, le principal goulot d'étranglement est la requête SQL qui scanne les tables à chaque appel du
script.
Avec 100 000 000 de créneaux et 1000 nouveaux créneaux par seconde, cela représente une charge très importante pour la
base de données.

Les limites du script sont:

1. **Temps d'exécution:** Le temps d'exécution du script pourrait être très long car il doit parcourir un grand nombre
   de données pour trouver les créneaux qui répondent aux critères donnés.
   L'ajout de 1000 nouveaux créneaux par seconde aggraverait encore la situation.

2. **Coût:** Le traitement de ce grand nombre de données dans BigQuery pourrait être très coûteux en termes de frais de
   requête.

3. **Limite de requêtes BigQuery:** Il existe des limites de requêtes (Rate Limit) pour l'utilisation de BigQuery qui pourraient être
   dépassées si on exécute ce script fréquemment.

4. **Chargement des données départementales à la volée:** peut également poser des problèmes de performance si le
   fichier de frontières de département est très volumineux ou s'il y a de
   nombreuses requêtes simultanées qui nécessitent ces données.

## Les propositions

### Proposition d'optimisation des tables

Avant de penser à l'architeture, ma première idée serait de stocker les données de frontières de département dans
BigQuery afin que les requêtes puissent y accéder directement plutôt que de les charger à chaque exécution de la
requête.

Pour améliorer les performances de la requête, on pourrait utiliser la puissance des jointures géographiques dans
BigQuery.
La table department_boudaries, au lieu de contenir les données numériques de frontières (latitude
nord/sud...), pourrait associer à chaque département, une donnée de type GEOGRPHY qui représenterait un
polygon décrivant les frontières des départements.

| department | polygon                     |
|------------|-----------------------------|
| 95         | POLYGON(north_latitude,...) |
| ...        | ....                        |

Les données de latitude et longitude de la table meeting_points pourraient être aussi remplacées par une donnée de type
GEOGRAPHY qui représente le point de rendez-vous.

| meeting_point_id | geo_point                    |
|------------------|------------------------------|
| 1                | GEOPOINT(latitude,longitude) |
| ...              | ....                         |

Ainsi on pourrait, joindre de manière efficace ces deux tables en utilisant la puissance de manipulation des
géographiques de BigQuery.

Les tables bookings et lessons pourraient être partitionnées par les dates afin d'améliorer les requêtes.

### Proposition d'optimisation de l'architecture

Pour améliorer les performances, on peut envisager d'utiliser une architecture de type "streaming" pour traiter les
nouveaux créneaux en temps réel plutôt que de les ajouter à la base de données et de les traiter ultérieurement.

Par exemple, on pourrait utiliser Cloud Pub/Sub pour collecter les données de nouveaux créneaux à mesure qu'ils sont
créés, puis utiliser Cloud Dataflow pour traiter ces données en continu.
Cloud DataFlow nous permettrait d'éviter de sur-solliciter l'écriture dans les tables BigQuery, en procédant à une
écriture par batch (groupes de crénaux).

Cloud DataFlow nous permettrait également de mettre à jour, en temps réel, une table qui contiendrait le nombre de
leçons agrégé par date, par département et par partnership.

Une nouvelle requête pourrait être codée pour intérogger cette base aggrégée. Cela permettrait d'obtenir rapidement les
résultats des agrégations, sans avoir à recalculer les agrégations sur les tables complètes.

On pourrait optimiser cette requête en partitionnant la table aggrégée par date et en la clusturisant par
partnership_type.

Le schéma ci-dessous récapitule l'architecture:

![Architecture](./images/archi_requests.png)

                           


