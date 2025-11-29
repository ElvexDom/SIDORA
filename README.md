# SIDORA AI – Base de Données Utilisateurs et Jeux Vidéo

## Objectif

Modéliser, normaliser et implémenter la base de données pour SIDORA AI, incluant la gestion des utilisateurs et des jeux vidéo. Intégrer les contraintes de protection des données personnelles (RGPD) dès la conception.

---

## Référentiels et Compétences

* Compétences transversales en modélisation de données et normalisation
* Certification RNCP Développeur.se en intelligence artificielle (2023)

---

## Ressources

* Bibliothèque **FAKER** pour générer des utilisateurs simulés
* Dataset **jeux vidéo** au format CSV pour tester l’import et la gestion des entités Jeux
* Données fictives d’utilisateurs pour tester le système de pseudonymisation et de consentement

---

## Contexte du Projet

* Développement d’un **logiciel de gestion des utilisateurs et des jeux vidéo** pour SIDORA AI.

* Migration des systèmes d’information vers une architecture robuste adaptée à la gestion des utilisateurs, des jeux et des données sensibles.

* Analyse des besoins métiers pour identifier les entités principales : **utilisateurs, jeux, éditeurs, plateformes**.

* Conception du Modèle Conceptuel (MCD) et Logique (MLD) de données avec application des règles de normalisation (3NF).

* Développement des requêtes SQL d’insertion, modification, suppression et extraction.

* **Intégration des contraintes RGPD pour les utilisateurs** :

  * **Mot de passe haché avec bcrypt** : garantit la sécurité, la non‑réversibilité et la conformité à l’Article 32 du RGPD (sécurité du traitement).
  * **Email haché avec SHA‑256** : permet la vérification et l’unicité sans conservation en clair, conformément au principe de minimisation des données et à l’Article 5 du RGPD (protection des données).
  * **Pseudonyme utilisateur stocké en clair** : nécessaire à l’affichage et aux interactions, sans permettre l’identification directe d’une personne réelle, en conformité avec l’Article 5 du RGPD (protection des données).

* Génération de données simulées avec **Faker** pour les tests, en respectant les principes de **privacy by design**.

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
