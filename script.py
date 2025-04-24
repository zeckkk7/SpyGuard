import requests 
import json
import base64
import warnings
import webbrowser
import subprocess
import os


# Désactivation des messages d'avertissements par rapport au certificat ssl
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter("ignore", InsecureRequestWarning)


print("Bienvenue sur SpyGuard")


### Récuperer le token afin de faire des requetes : 
# URL de l'API du token : 
url = "https://spytest:arki84@localhost:8443/api/get-token"

# Effectuer la requête GET en désactivant la vérification SSL car certificat non officiel
response = requests.get(url, verify=False)

# Vérifier le statut de la requête
if response.status_code == 200:
    try:
        # Analyser la réponse JSON
        data = response.json()  # Convertit la réponse en dictionnaire Python
        
        # Récupérer le token (supposons qu'il est dans une clé 'token')
        token = data.get("token")
        if token:
            print("Token récupéré:", token)
        else:
            print("Le token n'a pas été trouvé dans la réponse.")
    except json.JSONDecodeError:
        print("Erreur : la réponse n'est pas un JSON valide.")
else:
    print(f"Erreur HTTP : {response.status_code}, {response.text}")


#une fois qu'on est connecté il faut aller a la page reseau afin de définir les interfaces

#url_reseau = "https://spytest:arki84@localhost:8443/api/config/list"
#response_reseau = requests.get(url, verify=False)


# URL à ouvrir
url = "https://spytest:arki84@localhost:8443"

if os.name == "posix" :
    firefox_path = "/usr/bin/firefox"
else :
# Chemin vers Firefox (modifiez selon votre système)
    firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

# Lancer Firefox en mode navigation privée avec l'URL
subprocess.run([firefox_path, "--private-window", url])

print(os.name)
#url_web = "https://spytest:arki84@localhost:8443"
#webbrowser.open(url_web)