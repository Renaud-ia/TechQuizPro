from unittest.mock import patch

from django.test import TestCase
from django.db import transaction

# Create your tests here.
import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Job, Experience, Question, Technologie


class GetRandomQuestionTestCase(TestCase):
    def setUp(self):
        self.job = Job.objects.create(nom='job_name')
        self.experience1 = Experience.objects.create(nom='experience_name1')
        self.experience2 = Experience.objects.create(nom='experience_name2')

        self.technology = Technologie.objects.create(nom='technology')

        self.question = Question.objects.create(
            question_text='Test question',
            job=self.job,
            technologie=self.technology
        )

        self.question.experiences.set([self.experience1, self.experience2])

    def test_get_random_question_success(self):
        client = Client()
        data = {
            'job': 'job_name',
            'experience': 'experience_name1',
            'technologies': ['technology']
        }
        response = client.post('/question/generate/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('question_id', response.json())
        self.assertIn('question_text', response.json())

    def test_get_random_question_missing_fields(self):
        client = Client()
        response = client.post('/question/generate/', json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_get_random_question_invalid_json(self):
        client = Client()
        response = client.post('/question/generate/', '{invalid_json}', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_get_random_question_no_question_corresponding(self):
        client = Client()
        data = {
            'job': 'non_existing_job',
            'experience': 'non_existing_experience',
            'technologies': 'non_existing_technology'
        }
        response = client.post('/question/generate/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)


class CheckAnswerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = "question/evaluate/"
        with transaction.atomic():
            self.technologie = Technologie.objects.create(nom="css")
            self.job = Job.objects.create(nom='Développeur')
            self.question = Question.objects.create(
                question_text='Capitale de la France ?',
                job=self.job,
                technologie=self.technologie
            )

    @patch('questionshandler.views.CheckAnswer.evaluate_answer')
    @patch('questionshandler.views.CheckAnswer.percent_correct_answer')
    def test_post_with_valid_data(self, mock_percent_correct_answer, mock_evaluate_answer):
        mock_percent_correct_answer.return_value = 100.0
        mock_evaluate_answer.return_value = True

        data = {
            'question_id': self.question.id,
            'answer': 'Paris',
            'experience': '5 years'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        print(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'is_correct': True, 'percent_correct': 100.0})

    def test_post_with_missing_fields(self):
        data = {
            'question_id': self.question.id,
            'answer': 'Paris'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_post_with_invalid_json(self):
        data = "Invalid JSON"
        response = self.client.post(self.url, data, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_post_with_non_existent_question(self):
        data = {
            'question_id': 999,
            'answer': 'Paris',
            'experience': '5 years'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 404)

    def test_get_method_not_allowed(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)