# Recherche de Fichiers et Dossiers Modernisée

## Table des matières

- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
    - [Pré-requis](#pré-requis)
    - [Cloner le dépôt](#cloner-le-dépôt)
    - [Installer les dépendances](#installer-les-dépendances)
- [Utilisation](#utilisation)
    - [Lancer l'application](#lancer-lapplication)
    - [Utilisation de l'interface](#utilisation-de-linterface)
- [Création de l'exécutable](#création-de-lexécutable)
- [Structure du projet](#structure-du-projet)
- [Contribuer](#contribuer)
- [License](#license)

## Description

L'application de Recherche Intelligente de Fichiers et Dossiers est une application de bureau que j'ai développé en Python, permettant de rechercher et de prévisualiser des fichiers et des dossiers sur votre ordinateur. Elle offre une interface utilisateur moderne et intuitive pour faciliter la gestion des fichiers.

## Fonctionnalités

- Recherche de fichiers et de dossiers
- Filtrage par type de fichier
- Prévisualisation des fichiers (images, textes, PDF, documents Word, fichiers de code, vidéos)
- Sélection et modification du répertoire de recherche
- Interface utilisateur personnalisable

## Installation

### Pré-requis

- Python 3.12.2 ou plus récent
- pip (outil de gestion de paquets pour Python)
- Git (pour cloner le dépôt, facultatif)

### Cloner le dépôt

Clonez le dépôt Git sur votre machine locale :

```bash
git clone <https://github.com/matheogonnet/smart-file-search.git>

cd recherche-fichiers-dossiers
```

### Installer les dépendances

Installez les dépendances requises en utilisant pip :

```bash
pip install -r requirements.txt
```

## Utilisation

### Lancer l'application

Pour lancer l'application, exécutez le fichier `main.py` :

```bash
python main.py
```

### Utilisation de l'interface

- **Barre de recherche** : Utilisez la barre de recherche pour trouver des fichiers ou des dossiers par nom.
- **Filtrage** : Sélectionnez un type de fichier dans le menu déroulant pour affiner votre recherche.
- **Réinitialisation** : Cliquez sur le bouton "Réinitialiser" pour effacer tous les filtres.
- **Sélection de répertoire** : Par défault le répertoire est 'Documents', mais cliquez sur le bouton "Sélectionner Répertoire" pour changer le répertoire de recherche.
- **Prévisualisation** : Cliquez une fois sur un fichier pour avoir un aperçu. Double-cliquez pour l'ouvrir.

## Création de l'exécutable

Pour créer un exécutable unique de l'application, utilisez PyInstaller avec la commande suivante :

```bash
pyinstaller --onefile --windowed --icon=images/icone.ico --add-data "images/image.png;." --add-data "searching_tool/__init__.py;searching_tool" --add-data "searching_tool/file_search_app.py;searching_tool" --add-data "searching_tool/helpers.py;searching_tool" --add-data "searching_tool/preview.py;searching_tool" main.py

```

L'exécutable sera généré dans le répertoire `dist`.

## Structure du projet

Voici la structure du projet :

```
project_root/
├── main.py
├── icone.ico
├── image.png
├── requirements.txt
├── searching_tool/
│   ├── __init__.py
│   ├── file_search_app.py
│   ├── helpers.py
│   └── preview.py

```

- `main.py` : Fichier principal qui initialise l'application.

- `images/` : Dossier contenant les images et le favicon.
    - `icone.ico` : Icône de l'application.
    - `image.png` : Image utilisée dans l'application.

- `requirements.txt` : Liste des dépendances du projet.

- `searching_tool/` : Dossier contenant les modules de l'application.
    - `__init__.py` : Indique que `searching_tool` est un module Python.
    - `file_search_app.py` : Contient la classe `FileSearchApp` et ses méthodes.
    - `helpers.py` : Fonctions utilitaires.
    - `preview.py` : Fonctions de prévisualisation des fichiers.

## Contribuer

Les contributions sont les bienvenues ! Si vous souhaitez contribuer, veuillez suivre ces étapes :

1. Forkez le dépôt.
2. Créez une branche pour votre fonctionnalité (`git checkout -b fonctionnalite/amélioration`).
3. Commitez vos changements (`git commit -m 'Ajout de fonctionnalité'`).
4. Poussez vos changements (`git push origin fonctionnalite/amélioration`).
5. Ouvrez une Pull Request.

## License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
