import json
from openai import OpenAI
import logging

from django.shortcuts import render

# Create your views here.
import random
from django.http import JsonResponse, HttpResponseNotFound
from django.views import View
from django.views.decorators.http import require_POST

from .models import Question, Experience, Job

API_KEY_GPT = ""
MODEL = "gpt-3.5-turbo"

logger = logging.getLogger(__name__)

class GetRandomQuestion(View):
    def post(self, request):
        """
        method which defines the route to get a random answer
        """
        try:
            data = json.loads(request.body.decode('utf-8'))
            if 'job' in data and 'experience' in data and 'technologies' in data:
                # Tous les champs requis sont présents
                job = data['job']
                experience = data['experience']
                technologies = data['technologies']
            else:
                # Certains champs requis sont manquants
                return JsonResponse({'error': 'Missing required fields'}, status=400)

        except json.decoder.JSONDecodeError:
            # Erreur lors du décodage JSON
            return JsonResponse({'error': 'Invalid JSON data in request body'}, status=400)

        job_search = Job.objects.filter(nom=job).first()
        if not job_search:
            return HttpResponseNotFound(f"Job {job} don't exist in database")

        experience_search = Experience.objects.filter(nom=experience).first()
        if not experience_search:
            return HttpResponseNotFound(f"Experience {experience} don't exist in database")

        filtered_questions = Question.objects.filter(
            job__nom=job,
            experiences__nom=experience,
            technologie__nom__in=technologies
        )

        if len(filtered_questions) == 0:
            return HttpResponseNotFound("No question corresponding")

        random_question = random.choice(filtered_questions)

        response_data = {
            'question_id': random_question.id,
            'question_text': random_question.question_text
        }

        print(response_data)

        return JsonResponse(response_data)

    def get(self, request):
        # Rejet des requêtes GET avec une réponse HTTP 405 (Method Not Allowed)
        return JsonResponse({'error': 'GET method not allowed'}, status=405)





class CheckAnswer(View):
    def evaluate_answer(self, question: Question, reponse: str):
        client = OpenAI(
            api_key=API_KEY_GPT)

        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system",
                 "content": "You are a tech recruiter, you have to evaluate an answer by true or false."},
                {"role": "user",
                 "content": "question : capitale de la france ? réponse : bamako. ta réponse doit commencer par true or false"}
            ]
        )

        print(f"réponse de gpt : {completion.choices[0]}")

        # Récupération de la réponse générée par le modèle
        ai_response = completion.choices[0].message.strip().lower()

        # Vérification de la réponse
        if "true" in ai_response:
            return True
        elif "false" in ai_response:
            return False
        else:
            raise ValueError("La réponse générée n'est ni 'true' ni 'false'. Veuillez réessayer.")

    def percent_correct_answer(self, question: Question, experience: str) -> float:
        return 0

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            if 'question_id' in data and 'answer' in data and 'experience' in data:
                question_id = data.get('question_id')
                answer = data.get('answer')
                experience = data.get('experience')
            else:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in request body'}, status=400)

        # Récupérez la question depuis la base de données
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found'}, status=404)

        pct_correct = self.percent_correct_answer(question, experience)
        is_correct = self.evaluate_answer(question.question_text, answer)

        # il faut actualiser la BDD

        # Renvoyez une réponse JSON avec le résultat de la vérification
        return JsonResponse({'is_correct': is_correct, 'percent_correct': pct_correct})

    def get(self, request):
        # Rejet des requêtes GET avec une réponse HTTP 405 (Method Not Allowed)
        return JsonResponse({'error': 'GET method not allowed'}, status=405)

