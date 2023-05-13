import json
import unittest
from unittest.mock import patch
import questionnaire
import questionnaire_import
import os


class TestsQuestion(unittest.TestCase):
    print("test_du_questionnaire")

    def test_question_bonne_mauvaise_reponse(self):
        choix = ("choix1", "choix2", "choix3", "choix4")
        q = questionnaire.Question("Titre_question", choix, "choix3")
        # q.poser(1, 1)
        with patch("builtins.input", return_value="1"):
            self.assertFalse(q.poser(1, 1))
        with patch("builtins.input", return_value="3"):
            self.assertTrue(q.poser(1, 1))


class TestsQuestionnaire(unittest.TestCase):
    def test_questionnaire_lancer_alien_debutant(self):
        filename = os.path.join('test_data', 'viequotidienne_chocolat_debutant.json')
        filename_split_ = filename.split("_")

        with patch("builtins.input", return_value="1"):
            q = questionnaire.CreationDeQuestionnaire(filename_split_[-2] + ".json")
            self.assertIsNotNone(q)
            self.assertEqual(len(q.liste_de_question), 10, "⚠️ Le questionnaire débutant doit contenir 10 questions !")
            self.assertEqual(q.titre_questionnaire, "Chocolat", "⚠️ Le titre ne correspond pas !")
            self.assertEqual(q.choix_niveau, "debutant", "⚠️ le niveau doit être débutant !")
            self.assertEqual(q.categorie, "Vie quotidienne", "⚠️ La catégorie ne correspond pas !")
            with patch("builtins.input", return_value="1"):
                q2 = questionnaire.Questionnaire(q.liste_de_question)
                self.assertEqual(q2.lancer(), 2, "⚠️ Le score est différent de 2 !")


class TestsImportQuestionnaire(unittest.TestCase):
    def test_import_format_json(self):
        questionnaire_import.generate_json_file("Vie quotidienne", "Chocolat", "https://www.kiwime.com/oqdb/files/1019394664/OpenQuizzDB_019/openquizzdb_19.json")
        filenames = ("quizz_json/viequotidienne_chocolat_confirme.json", "quizz_json/viequotidienne_chocolat_debutant.json", "quizz_json/viequotidienne_chocolat_expert.json")

        for filename in filenames:
            self.assertTrue(os.path.isfile(filename))
            file = open(filename, 'r')
            json_data = file.read()
            file.close()
            # on a récupéré notre json_data que l'on va désérialiser
            try:
                data = json.loads(json_data)
            except:
                self.fail("Problème de désérialisation pour le fichier " + filename)

            self.assertIsNotNone(data.get("titre"))  # on utilise pas data["titre"] car on risque d'avoir une exception, avec get on aura un one
            self.assertIsNotNone(data.get("questions"))
            self.assertIsNotNone(data.get("difficulté"))
            self.assertIsNotNone(data.get("categorie"))

            for question in data.get("questions"):
                self.assertIsNotNone(question.get("titre"))
                self.assertIsNotNone(question.get("choix"))
                for choix in question.get("choix"):
                    self.assertGreater(len(choix[0]), 0)
                    self.assertTrue(isinstance(choix[1], bool))
                bonne_reponses = [i[0] for i in question.get("choix") if i[1]]
                self.assertEqual(len(bonne_reponses), 1)




unittest.main()
