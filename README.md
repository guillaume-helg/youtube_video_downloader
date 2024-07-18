Programme de telechargement de video youtube au format video ou musical.


## Avant de lancé le programme pour la 1ere fois il faut :
- si vous téléchargez une playlist vérifiez qu'elle soit publique

# Spotify Playlist to YouTube Link Extractor

Ce projet Python permet de prendre un lien de playlist Spotify, d'extraire les titres et les artistes, puis de rechercher chaque titre et artiste sur YouTube pour obtenir le premier résultat. Les résultats sont enregistrés dans un fichier texte.

## Prérequis

1. **Python 3.6+**
2. **pip** (Python package installer)

## Installation

### Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/spotify-to-youtube.git
cd spotify-to-youtube
````

### Installer les dépendances
```bash
pip install -r requirements.txt
```

### Configuration
Créez un fichier .env dans le répertoire du projet et ajoutez vos identifiants Spotify et YouTube API :

```plaintext
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
YOUTUBE_API_KEY=your_youtube_api_key
```

Vous pouvez obtenir ces identifiants en suivant les étapes ci-dessous :

Spotify API :

Allez sur Spotify Developer Dashboard et connectez-vous avec votre compte Spotify.
Créez une nouvelle application et récupérez le Client ID et Client Secret.

YouTube Data API :

Allez sur Google Cloud Console.
Créez un nouveau projet ou sélectionnez un projet existant.
Activez l'API YouTube Data API v3 pour votre projet.
Créez des identifiants (API key) pour l'API YouTube Data API.
Utilisation


Exécutez le script en passant le lien de la playlist Spotify en paramètre :

```bash
python spotify_playlist_to_file.py "https://open.spotify.com/playlist/XXXXXXXXXX"
```


Le script extrait les titres et les artistes de la playlist Spotify spécifiée, recherche chaque titre et artiste sur YouTube, et enregistre les résultats dans un fichier tracks.txt.

Exemple de fichier tracks.txt
```plaintext
Track Name 1 - Artist Name 1 - https://www.youtube.com/watch?v=XXXXXXXXXXX
Track Name 2 - Artist Name 2 - https://www.youtube.com/watch?v=XXXXXXXXXXX
```


### Fichiers supplémentaires

**`requirements.txt`** :

```plaintext
spotipy
google-api-python-client
python-dotenv
pytube
```
