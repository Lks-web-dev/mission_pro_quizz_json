import requests
import json
import unicodedata

# ====> REMARQUE : Les Url ci-dessous sont différentes que celles affichées dans la vidéo.
# C'est normal, continuez bien avec les url de ce fichier
open_quizz_db_data = (
    ("Animaux", "Les chats", "https://www.codeavecjonathan.com/res/mission/openquizzdb_50.json"),
    ("Arts", "Musée du Louvre", "https://www.codeavecjonathan.com/res/mission/openquizzdb_86.json"),
    ("Bande dessinnée", "Tintin", "https://www.kiwime.com/oqdb/files/2124627384/OpenQuizzDB_124/openquizzdb_124.json"),  # Lien non fonctionnel
    ("Cinéma", "Alien", "https://www.codeavecjonathan.com/res/mission/openquizzdb_241.json"),
    ("Cinéma", "Star wars", "https://www.codeavecjonathan.com/res/mission/openquizzdb_90.json"),
    ("Vie quotidienne", "Chocolat", "https://www.kiwime.com/oqdb/files/1019394664/OpenQuizzDB_019/openquizzdb_19.json"),  # Ajout + 1 quizz
)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def get_quizz_filename(categorie, titre, difficulte):
    # Tous les fichiers json sont désormais dans le dossier quizz_json
    return "quizz_json/" + strip_accents(categorie).lower().replace(" ", "") + "_" + strip_accents(titre).lower().replace(" ", "") + "_" + strip_accents(difficulte).lower().replace(" ", "") + ".json"


def generate_json_file(categorie, titre, url):
    out_questionnaire_data = {"categorie": categorie, "titre": titre, "questions": []}
    out_questions_data = []
    response = requests.get(url)
    try:
        data = json.loads(response.text)  # Parce que récupérer de request ".text"
    except:
        print("Exception pour la requete : " + url)
    else:
        try:
            difficulte = data["difficulté"]  # Information sur la difficulté
            all_quizz = data["quizz"]["fr"]
            for quizz_title, quizz_data in all_quizz.items():
                out_filename = get_quizz_filename(categorie, titre, quizz_title)
                print(out_filename)
                out_questionnaire_data["niveau"] = quizz_title  # je remplace difficulte par niveau car plus approprié
                for question in quizz_data:
                    question_dict = {}
                    question_dict["titre"] = question["question"]
                    question_dict["choix"] = []
                    for ch in question["propositions"]:
                        question_dict["choix"].append((ch, ch == question["réponse"]))
                    out_questions_data.append(question_dict)
                out_questionnaire_data["questions"] = out_questions_data
                out_questionnaire_data["difficulté"] = difficulte  # Ajouté au dictionnaire
                out_json = json.dumps(out_questionnaire_data)

                file = open(out_filename, "w")
                file.write(out_json)
                file.close()
                print("end")
        except:
            print("Exception data pour l'url : " + url + "-Questionnaire : " + titre)


if __name__ == "__main__":
    for quizz_data in open_quizz_db_data:
        generate_json_file(quizz_data[0], quizz_data[1], quizz_data[2])

