#!/bin/bash

# Installer Volta
echo "Installation de Volta..."
curl https://get.volta.sh | bash

# Ouvrir un nouveau terminal et exécuter les commandes
echo "Lancement d'un nouveau terminal et exécution des commandes..."

# Création d'un script pour le terminal
cat <<EOF > /tmp/start_spyguard.sh
#!/bin/bash
cd /usr/share/spyguard/app/backend
volta pin node@16
volta pin npm@6
npm i
npm run build
EOF

# Rendre le script exécutable
chmod +x /tmp/start_spyguard.sh

# Ouvrir un nouveau terminal et exécuter le script
gnome-terminal -- /tmp/start_spyguard.sh
