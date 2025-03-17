import os
import requests

# Récupération du token
GH_TOKEN = os.getenv("GH_TOKEN")

# API GitHub de récupération des langages
url = "https://api.github.com/users/loufi84/repos?type=all&per_page=100"

# Requête de récupération des données
headers = {
  "Authorization": f"token{GH_TOKEN}"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
  repos = response.json()

  # Extrait les langages
  languages = {}
  for repo in repos:
    repo_name = repo['name']
    repo_languages_url = f"https://api.github.com/repos/loufi84/{repo_name}/languages"
    languages_response = requests.get(repo_languages_url, headers=header)

    if languages_response.status_code == 200:
      repo_languages = languages_response.json()
      for lang, lines in repo_languages.items():
        languages[lang] = languages.get(lang, 0) + lines

    # Génère un graphique des langages utilisés
    lang_stats = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    lang_summary = "\n".join([f"{lang}: {lines}" for lang, lines in lang_stats])

    # Mise à jour du README
    with open("README.md", "w") as file:
      readme = file.read()

    # Ajoute les stats de langage
    readme = readme.replace("<!-- LANGUAGES -->", f"### Langages utilisés\n{lang_summary}\n<!-- LANGUAGES -->")

    # Sauvegarde du fichier modifié
    with open("README.md", "w") as file:
      file.write(readme)

else:
  print("Erreur lors de la récupération des données depuis GitHub")
