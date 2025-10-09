# Vinted Alert

Script qui surveille Vinted et poste les nouveaux articles automatiquement sur Discord.

## Fonctionnalités

- Surveille les recherches Vinted en temps réel
- Poste automatiquement les nouveaux articles sur Discord
- Embeds avec toutes les infos (prix, taille, marque, localisation, avis vendeur)
- Commandes Discord pour configurer
- Gère plusieurs recherches en même temps
- Gestion des rate limits

## 🚀 Installation

### Prérequis

- Python 3.7 ou supérieur
- Un bot Discord avec les permissions appropriées
- Accès à un serveur Discord

### Étapes d'installation

1. **Cloner le repository**
   ```bash
   git clone https://github.com/2spy/Vinted-Discord-Bot.git
   cd Vinted-Discord-Bot
   ```

2. **Installer les dépendances**
   ```bash
   pip install requests beautifulsoup4 discord.py
   ```

3. **Configurer le bot Discord**
   - Créez une application sur le [Discord Developer Portal](https://discord.com/developers/applications)
   - Créez un bot et copiez le token
   - Invitez le bot sur votre serveur avec les permissions `Send Messages` et `Manage Webhooks`

4. **Configuration initiale**
   ```bash
   # Éditez le fichier config.json
   {
     "token": "VOTRE_TOKEN_BOT_DISCORD",
     "prefix": "$",
     "status": "Monitoring Vinted",
     "suburl": {},
     "embed-color-text": "YAML",
     "embed-color": 16777215,
     "embed-config": {
       "prix": "oui",
       "vendeur": "oui", 
       "avis": "oui",
       "localisation": "oui",
       "marque": "oui",
       "taille": "oui"
     }
   }
   ```

## 🎯 Utilisation

### Démarrage du bot

```bash
python loadsub.py
```

### Commandes Discord

| Commande | Description | Usage |
|----------|-------------|-------|
| `$sub <url>` | Ajouter une surveillance Vinted | `$sub https://vinted.fr/catalog?search_text=nike` |
| `$remove_sub` | Supprimer la surveillance du salon | `$remove_sub` |
| `$change_url <nouveau_url>` | Modifier l'URL surveillée | `$change_url https://vinted.fr/catalog?search_text=adidas` |
| `$change_color_text <couleur>` | Changer la couleur du texte | `$change_color_text YAML` ou `$change_color_text fix` |
| `$change_color_embed <couleur>` | Changer la couleur de l'embed | `$change_color_embed 16777215` |
| `$help` | Afficher l'aide | `$help` |

### Exemple d'utilisation

1. **Ajouter une surveillance**
   ```
   $sub https://vinted.fr/catalog?search_text=nike+air+max&order=newest_first
   ```

2. **Le bot créera automatiquement un webhook et commencera à surveiller**
   - Nouveaux articles postés automatiquement
   - Embeds avec toutes les informations disponibles
   - Images des articles incluses

## ⚙️ Configuration avancée

### Paramètres de l'embed

Vous pouvez personnaliser quelles informations afficher dans les embeds :

```json
{
  "embed-config": {
    "prix": "oui",           // Afficher le prix
    "vendeur": "oui",        // Afficher le nom du vendeur  
    "avis": "oui",          // Afficher les avis (positif/négatif)
    "localisation": "oui",   // Afficher pays/ville
    "marque": "oui",        // Afficher la marque
    "taille": "oui"         // Afficher la taille
  }
}
```

### Couleurs disponibles

- **Texte** : `YAML`, `fix`
- **Embed** : Code couleur hexadécimal (ex: `16777215` pour blanc)

## 📋 Structure du projet

```
Vinted-Discord-Bot/
├── config.json          # Configuration du bot
├── vinted.py            # Script principal de surveillance
├── loadsub.py           # Bot Discord avec commandes
├── README.md            # Documentation
└── LICENSE              # Licence MIT
```

## 🔧 Développement

### Architecture

- **`vinted.py`** : Module de scraping Vinted avec BeautifulSoup
- **`loadsub.py`** : Bot Discord utilisant discord.py
- **`config.json`** : Configuration centralisée

### Fonctionnalités techniques

- **Scraping intelligent** : Parse les données JSON des pages Vinted
- **Gestion des erreurs** : Retry automatique en cas de rate limit
- **Threading** : Surveillance parallèle de plusieurs recherches
- **Webhooks** : Notifications Discord optimisées

## ⚠️ Limitations et considérations

- **Rate limiting** : Le bot respecte les limites de Vinted (max 10 salons)
- **Éducatif uniquement** : Ce projet est destiné à des fins d'apprentissage
- **Respect des ToS** : Assurez-vous de respecter les conditions d'utilisation de Vinted

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/main`)
3. Committez vos changements (`git commit -m 'Add'`)
4. Push vers la branche (`git push origin feature/main`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.


## ⭐ Support

Si ce projet vous a aidé, n'hésitez pas à lui donner une étoile ! ⭐

---

> **Note éducative** : Ce bot est créé à des fins éducatives pour apprendre le web scraping et l'intégration Discord. Utilisez-le de manière responsable et respectez les conditions d'utilisation des services tiers.