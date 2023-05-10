# PROJET QUESTIONNAIRE V3 : POO
import sys, os
import fnmatch
import json


class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    # def FromData(data):
    #     # ....
    #     q = Question(data[2], data[0], data[1])
    #     return q

    def poser(self, iteration, nombre_de_question):
        print("QUESTION : " + str(iteration) + "/" + str(nombre_de_question))
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)


class Questionnaire:
    def __init__(self, questions):
        self.questions = questions

    def lancer(self):
        score = 0
        nombre_de_question = len(self.questions)
        iteration = 0
        for question in self.questions:
            iteration += 1
            if question.poser(iteration, nombre_de_question):
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


class CreationDeQuestionnaire:
    niveau_liste = ['debutant', 'confirme', 'expert']
    choix_niveau = ""  # correspond au niveau du jeu (debutant, expert, confirmé)
    titre = ""
    quizz = None
    categorie = ""
    difficulte = ""
    question = ""
    choix = []
    bonne_reponse = ""
    liste_de_question = []

    def __init__(self, nom_du_quizz):
        self.nom_du_quizz = nom_du_quizz
        self.niveau()

    def ouvrir_questionnaire_json(self):
        for file in os.listdir('quizz_json/'):
            if fnmatch.fnmatch(file, '*_' + self.titre[0] + '_' + self.choix_niveau + '.json'):
                file_json = open("quizz_json/" + file, 'r')
                data = file_json.read()
                self.quizz = json.loads(data)
                file_json.close()
                self.mise_en_forme()

    def niveau(self):
        self.titre = self.nom_du_quizz.split(".")
        print("Vous avez demandé le questionnaire : " + self.titre[0])
        print("Choisissez votre niveau de difficuté parmis ces choix :")
        print("1- Débutant")
        print("2- Confirmé")
        print("3- Expert")
        choix = Question.demander_reponse_numerique_utlisateur(1, 3)
        self.choix_niveau = self.niveau_liste[choix - 1]
        self.ouvrir_questionnaire_json()

    def mise_en_forme(self):
        self.categorie = self.quizz["categorie"]
        self.difficulte = self.quizz["difficulté"]
        for question in self.quizz["questions"]:
            self.question = question["titre"]
            liste_de_choix = question["choix"]
            for choix_unique in liste_de_choix:
                self.choix.append(choix_unique[0])
                if choix_unique[1]:
                    self.bonne_reponse = choix_unique[0]
            self.liste_de_question.append(Question(self.question, self.choix, self.bonne_reponse))
            self.choix = []
        self.presentation()

    def presentation(self):
        print("-" * 125)
        print("Vous avez choisi le niveau " + self.choix_niveau + ", il y a " + str(len(self.liste_de_question)) + " questions")
        print("Difficulté du quizz " + self.titre[0] + " est de : " + self.difficulte)
        print("-" * 125)


Questionnaire(CreationDeQuestionnaire(sys.argv[1]).liste_de_question).lancer()

# Questionnaire(
#     (
#     Question("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris"),
#     Question("Quelle est la capitale de l'Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome"),
#     Question("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"), "Bruxelles")
#     )
# ).lancer()


