import openai

from openai import OpenAI
client = OpenAI(
  api_key="sk-proj-PacqffrWEhpxvwjGbbAFT3BlbkFJnxy4YPMFIexooGA7h0zQ")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a tech recruiter, you have to evaluate an answer by true or false."},
    {"role": "user", "content": "question : capitale de la france ? réponse : bamako. ta réponse doit commencer par true or false"}
  ]
)

print(completion.choices[0].message)

