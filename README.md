# SIDORA AI – Base de Données Utilisateurs et Jeux Vidéo

## 🎯 Objectif

Concevoir, normaliser et implémenter une base de données pour **SIDORA AI**, incluant la gestion des **utilisateurs** et des **jeux vidéo**, avec intégration des contraintes de **protection des données personnelles (RGPD)** dès la conception.

---

## 🧰 Référentiels et Compétences

* Compétences en **modélisation de données** et **normalisation**.
* Certification **RNCP Développeur.se en intelligence artificielle (2023)**.

---

## 📚 Ressources

* Bibliothèque **Faker** pour générer des utilisateurs simulés.
* Dataset **jeux vidéo** au format CSV pour tester l’import et la gestion des entités.
* Données fictives d’utilisateurs pour tester la **pseudonymisation** et la gestion du **consentement**.

---

## 🏗️ Contexte du Projet

* Développement d’un **logiciel de gestion des utilisateurs et des jeux vidéo** pour SIDORA AI.
* Migration des systèmes d’information vers une architecture robuste adaptée à la gestion des **données sensibles**.
* Analyse des besoins métiers pour identifier les entités principales : **utilisateurs, jeux, éditeurs, plateformes**.
* Conception du **Modèle Conceptuel de Données (MCD)** et **Modèle Logique de Données (MLD)** en appliquant les règles de **3NF**.
* Développement des requêtes SQL pour **insertion, modification, suppression et extraction** des données.

### 🔒 Conformité RGPD

* **Mot de passe haché avec bcrypt** : garantit la sécurité, la non‑réversibilité et la conformité à l’Article 32 du RGPD (sécurité du traitement).
* **Email haché avec SHA‑256** : permet la vérification et l’unicité sans conservation en clair, conformément au principe de minimisation des données et à l’Article 5 du RGPD (protection des données).
* **Pseudonyme utilisateur stocké en clair** : nécessaire à l’affichage et aux interactions, sans permettre l’identification directe d’une personne réelle, en conformité avec l’Article 5 du RGPD (protection des données).
* **Conservation des données limitée à 5 ans maximum** : les données ne sont stockées **que si le consentement est donné** (consent = True), sinon aucun enregistrement n’est créé.
* **Génération de données simulées avec Faker** pour tester le système, respectant les principes de **privacy by design**.

---

## 📦 Livrables

1. **Modèle Conceptuel de Données (MCD)** détaillant les entités et leurs relations.
2. **Modèle Logique de Données (MLD)** avec définition des relations et contraintes d’intégrité.
3. **Script Python** pour la création des tables et la mise en place des contraintes d’intégrité.
4. **Note de Conformité RGPD** détaillant la pseudonymisation, la gestion du consentement et la durée de rétention.

---

## ⚡ Critères de Performance

* MLD/MPD normalisé en **3NF**.
* **Clés primaires, étrangères et contraintes SQL** correctement définies.
* Table **Utilisateurs** avec champ **consentement** (Boolean) et **date limite de rétention**.
* **Pseudonymisation/anonymisation** des données sensibles appliquée correctement.

---

## 🛠️ Prérequis

* **Python 3.11+**
* **pip** installé
* **Environnement virtuel** pour isoler les dépendances

---

## ⚙️ Installation

1. **Crée un environnement virtuel :**

```bash
python -m venv .venv
```

2. **Active l'environnement :**

*Sur Windows :*

```bash
.venv\Scripts\activate
```

*Sur macOS/Linux :*

```bash
source .venv/bin/activate
```

3. **Installe les dépendances :**

```bash
pip install -r requirements.txt
```

---

## ▶️ Lancer l'application

Depuis la racine du projet, lance le module principal :

```bash
python -m application
```

* ⚠️ Assure-toi d’avoir activé l’environnement virtuel avant d’exécuter le programme.

---

## 🧪 Tests

* Les tests sont réalisés avec **pytest**.
* Pour exécuter tous les tests depuis la racine :

```bash
pytest tests
```

* Pour exécuter un fichier spécifique :

```bash
pytest tests/test_nom_du_fichier.py
```

* Pour voir les détails de chaque test :

```bash
pytest -v
```

---

## 🔄 Intégration Continue (GitHub Actions)

Exemple d’étapes CI :

```yaml
- name: Run all unit tests
  run: pytest tests
```

---

## 📜 Licence

Ce projet est sous licence **MIT**.
