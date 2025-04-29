import requests 
import json
import base64
import warnings
import webbrowser
import subprocess
import os

print("Bienvenue sur SpyGuard")

### Récuperer le token afin de faire des requetes : 
# URL de l'API du token : 
url = "https://cybercape:cybercape@localhost:8443/api/get-token"

# Effectuer la requête GET en désactivant la vérification SSL car certificat non officiel
response = requests.get(url, verify=False)

# Vérifier le statut de la requête
if response.status_code == 200:
    try:
        # Analyser la réponse JSON
        data = response.json()  # Convertit la réponse en dictionnaire Python
        
        # Récupérer le token 
        token = data.get("token")
        if token:
            print("Token récupéré:", token)
        else:
            print("Le token n'a pas été trouvé dans la réponse.")
    except json.JSONDecodeError:
        print("Erreur : la réponse n'est pas un JSON valide.")
else:
    print(f"Erreur HTTP : {response.status_code}, {response.text}")


# URL à ouvrir
url = "https://cybercape:cybercape@localhost:8443"

if os.name == "posix" :
    #Pour linux/mac
    firefox_path = "/usr/bin/firefox"
else :
# Pour windows
    firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

# Lancer Firefox en mode navigation privée avec l'URL afin d'éviter le cache
subprocess.run([firefox_path, "--private-window", url])
