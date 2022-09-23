![Alt text](https://github.com/DamienZeh/Gudlft_p11_ocr/blob/cleaning_and_finalization/logo/logo.png)<br>

# Güdlft

Cette application permet à des clubs sportifs de pouvoir réserver des places pour des compétitions.<br> Les secrétaires de clubs, une fois connectées, peuvent:<br>
- Voir les points de leur club;
- Voir les compétitions proposées(et celles qui ont eu déjà lieu);
- Y réserver des places(dans une limite de 12 places par compétition, par club);
- Un club peut réserver des places grâce à ses points.
- Il faudra 3 points pour réserver 1 place.

On peut aussi afficher les clubs et leurs points, sans besoin d'être connecté.<br>

Ceci est une version améliorée(déboguée et avec de nouvelles implémentations) du projet d'origine, <br>
qui se trouve [**ici**](https://github.com/OpenClassrooms-Student-Center/Python_Testing).<br>
Cette version à une branche, par bug corrigé, et amélioration ajoutée.<br>
Elle a aussi plusieurs types de tests.<br><br>





## Téléchargement et installation 

Cette application utilise **Python 3.10.5** ([plus d'informations ici](https://www.python.org/downloads/release/python-3105/)).<br>
Et **git** (si vous ne l'avez pas encore : [téléchargement/installation ici](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git))<br>
- Avec votre terminal, allez dans le dossier ou vous souhaitez placer le projet.<br/> 
Exemple : ``cd C:\Users\damie\Documents\Python_Project``
- Copiez le projet : ``git clone https://github.com/DamienZeh/Gudlft_p11_ocr.git``
- Puis, allez dans ce projet : ``cd Gudlft_p11_ocr\``<br/> 

Installation Windows:
- puis créez l’environnement virtuel avec  ``python -m venv env``<br/>
	_(‘env’ est le nom que j’ai sur mon environnement virtuel, il est aussi noté dans le gitignore.)_
- Puis activez le : ``.\env\Scripts\activate`` (pour windows)<br/>
	_(Vous avez maintenant un ‘(env)’ d’affiché, l'environnement est activé)_<br>
cette commande devra être lancée à chaque redémarrage du terminal.<br>

Installation Linux :
- puis créez l’environnement virtuel avec ``python3 -m venv env`` <br/>
	_(‘env’ est le nom que j’ai sur mon environnement virtuel, il est aussi noté dans le gitignore.)_
- Puis activez le : ``source env/bin/activate`` <br/>
	_(Vous avez maintenant un ‘(env)’ d’affiché, l'environnement est activé)_<br>
cette commande devra être lancée à chaque redémarrage du terminal.

Puis, l’installation  des packages présents dans le requirements.txt:<br> ``pip install -r requirements.txt``
<br/><br>


## Lancer l'application
Pour lancer l'application, tapez les commandes:<br/>
- Sur Windows:
	- ``$env:FLASK_APP = "server.py" ``<br/>
- Sur Linux:
	- ``export FLASK_APP=server.py ``<br/>

Puis :  ``flask run ``<br/>
Il suffira ensuite d'aller sur le site : **http://127.0.0.1:5000/**.<br/>
Pour se connecter, il faut faire parti des clubs inscrits. Voici les ids des clubs en exemple :<br/>
- john@simplylift.co
- admin@irontemple.com
- kate@shelifts.co.uk

Puis il suffit de choisir la compétition ou l'on veut s'inscrire, et choisir le nombre de places,<br/>
grâce aux points dont le club dispose. **Attention, pour rappel, 3 points = 1 place !**<br/>
Puis, l'utilisateur peut se déconnecter, s'il le souhaite.
<br/><br/>


## Lancer les tests
Pour lancer les tests (unitaires, intégrations, et fonctionnels), on se sert du pack **pytest** : <br>
- ``pytest -v``<br><br>


## Couverture du code
Pour voir le pourcentage de couverture de ces tests, on se sert de **coverage**.<br>
Il y a un fichier **.coveragerc**, qui exclut les fichiers autres que **server.py**,<br>
car on a besoin d'afficher la couverture des tests seulement sur ce fichier. Vous tapez: <br>
- ``pytest --cov`` <br>

Si on souhaite accéder au rapport (pour par exemple voir les Missings, en plus), on fait :<br> 
- ``coverage report -m`` <br><br>


## Tests de performances
Pour lancer les tests de performances, on se sert du pack **locust**.<br/>
Il faut que l'application soit lancée(comme on a vu un peu plus haut), puis ouvrez un autre terminal.<br/>
- Sur Windows:<br/>
``locust -f tests\performance_tests\locustfile.py --web-host localhost``.<br/>
- Sur Linux:<br/>
``locust -f tests/performance_tests/locustfile.py --web-host localhost``.<br/>

Il faudra ensuite aller sur **http://localhost:8089**, et lancer les tests.<br/>
Ou si vous souhaitez juste voir les résultats déjà réalisés, ils sont disponibles dans le projet(dossier reports).<br/><br/>

## Vérification du code
- Pour faire un contrôle du code avec **flake8** (avec max lenght à 79, sauf pour le settings.py), tapez :<br/>
``flake8 --max-line-length 79 --exclude=env`` ;<br/><br/>

## Auteur

* **Damien Hernandez** _alias_ [DamienZeh](https://damienhernandez.fr/)








