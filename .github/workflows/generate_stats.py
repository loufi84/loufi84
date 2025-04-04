# Force update test
import os
import requests
import matplotlib.pyplot as plt
import re

# Récupération du token GitHub
GH_TOKEN = os.getenv("GH_TOKEN")
if not GH_TOKEN:
    print("Erreur : GH_TOKEN not defined.")
    exit(1)

# API GitHub pour récupérer les repos
url = "https://api.github.com/user/repos?type=owner&per_page=100"

# Headers pour l'authentification
headers = {
    "Authorization": f"token {GH_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"GitHub API's error : {response.status_code} - {response.text}")
    exit(1)

repos = response.json()

# Dictionnaire des langages
languages = {}

# Parcours des repos pour récupérer les langages
for repo in repos:
    repo_name = repo['name']
    lang_url = f"https://api.github.com/repos/loufi84/{repo_name}/languages"
    
    lang_response = requests.get(lang_url, headers=headers)
    if lang_response.status_code == 200:
        repo_languages = lang_response.json()
        for lang, lines in repo_languages.items():
            languages[lang] = languages.get(lang, 0) + lines

# Trier les langages par utilisation
lang_stats = sorted(languages.items(), key=lambda x: x[1], reverse=True)

# Vérifier qu'il y a des données
if not lang_stats:
    print("No language detected.")
    exit(1)

# Générer un graphique
langs, values = zip(*lang_stats)
plt.figure(figsize=(8, 6))
plt.pie(values, labels=langs, autopct="%1.1f%%", colors=plt.cm.Paired.colors)
plt.title("Most used languages")

# Sauvegarde du graphique
plt.savefig("languages.png")

# Mise à jour du README.md
with open("README.md", "r") as file:
    readme = file.read()

# Suppression de la section
readme = re.sub(r"### Languages used.*?<!-- LANGUAGES -->", "<!-- LANGUAGES -->", readme, flags=re.DOTALL)

# Ajoute les stats de langage et l'image
lang_summary = "\n".join([f"- **{lang}**: {lines} lines" for lang, lines in lang_stats])
new_content = f"### Languages used\n\n![Languages used](languages.png)\n\n{lang_summary}\n<!-- LANGUAGES -->"

# Insère le contenu
readme = readme.replace("<!-- LANGUAGES -->", new_content)

# Sauvegarde du README mis à jour
with open("README.md", "w") as file:
    file.write(readme)

print("README.md update complete.")
