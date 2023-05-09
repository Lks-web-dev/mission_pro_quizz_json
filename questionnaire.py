# PROJET QUESTIONNAIRE V3 : POO
import sys, os
import fnmatch


class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def FromData(data):
        # ....
        q = Question(data[2], data[0], data[1])
        return q

    def poser(self):
        print("QUESTION")
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
        for question in self.questions:
            if question.poser():
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


class CreationDeQuestionnaire:
    debutant = {}
    expert = {}
    confirme = {}
    niveau_liste = ['debutant', 'expert', 'confirme']
    choix = ""
    titre = ""

    def __init__(self, nom_du_quizz):
        self.nom_du_quizz = nom_du_quizz
        self.presentation()

    def ouvrir_questionnaire_json(self):
        for file in os.listdir('quizz_json/'):
            if fnmatch.fnmatch(file, '*_' + self.titre[0] + '_' + self.choix + '.json'):
                print(file)

    def presentation(self):
        self.titre = self.nom_du_quizz.split(".")
        print("Vous avez demandé le questionnaire : " + self.titre[0])
        print("Choisissez votre niveau de difficuté parmis ces choix :")
        print("1- Débutant")
        print("2- Expert")
        print("3- Confirmé")
        choix = Question.demander_reponse_numerique_utlisateur(1, 3)
        self.choix = self.niveau_liste[choix-1]
        self.ouvrir_questionnaire_json()


CreationDeQuestionnaire(sys.argv[1])
# Questionnaire(
#     (
#     Question("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris"),
#     Question("Quelle est la capitale de l'Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome"),
#     Question("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"), "Bruxelles")
#     )
# ).lancer()


