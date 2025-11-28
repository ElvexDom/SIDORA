# SIDORA AI – Base de Données Ventes de Jeux Vidéo

## Objectif

Modéliser, normaliser et implémenter la base de données de ventes de jeux vidéo pour SIDORA AI.
Intégrer les contraintes de protection des données personnelles (RGPD) dès la conception.

---

## Référentiels et Compétences

* Compétences transversales en modélisation de données et normalisation
* Certification RNCP Développeur.se en intelligence artificielle (2023)

---

## Ressources

* Bibliothèque FAKER pour générer les données simulées
* Dataset brut : ventes de jeux vidéo (CSV/JSON)

---

## Contexte du Projet

* Migration des systèmes d’information vers une architecture robuste
* Analyse des besoins métiers pour identifier les entités principales : jeux, éditeurs, plateformes, utilisateurs, ventes
* Conception du Modèle Conceptuel (MCD) et Logique (MLD) de données
* Application des règles de normalisation (3NF)
* Développement des requêtes SQL d’insertion, modification, suppression et extraction
* Intégration des contraintes RGPD, notamment pour la table Utilisateurs

---

## Livrables

1. Modèle Logique de Données (MLD) avec définition des relations
2. Script Python pour création des tables et contraintes d’intégrité
3. Note de Conformité RGPD avec pseudonymisation, gestion du consentement et durée de rétention

---

## Critères de Performance

* MLD/MPD en 3NF
* Clés primaires, étrangères et contraintes SQL correctement définies
* Table Utilisateurs avec champ consentement (Boolean) et date limite de rétention
* Pseudonymisation/anonymisation des données sensibles

---
