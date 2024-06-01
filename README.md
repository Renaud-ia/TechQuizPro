# TechQuizPro
Tech Quiz Pro: Master technical interviews effortlessly with this ongoing project. Built with Python and React, it offers tailored practice sessions, instant feedback, and upcoming features to excel in your next technical interview. Start sharpening your skills today!

# Tech Quiz Pro

Tech Quiz Pro is an ongoing project designed to help individuals master technical interviews. Built with Python and React, this application offers a user-friendly interface for practicing common interview questions and receiving instant feedback.

## Features

- **Tailored Practice Sessions:** Specify your desired position, experience, and required technologies to receive a curated list of typical questions.
- **Instant Feedback:** Get immediate evaluation of your answers using the ChatGPT API, highlighting strengths and areas for improvement.
- **Upcoming Features:** Test your soft skills, input job postings directly for more tailored questions, and receive detailed explanations for any mistakes in your responses.

## Installation

1. Clone this repository to your local machine:

git clone https://github.com/Renaud-ia/TechQuizPro.git

2. Build Docker containers for the frontend and backend parts:
- For the frontend part:
  ```
  cd frontend
  docker build -t tech-quiz-pro-frontend .
  ```
- For the backend part:
  ```
  cd backend
  docker build -t tech-quiz-pro-backend .
  ```

3. Run the Docker containers:
- For the frontend part:
  ```
  docker run -d -p 3000:3000 tech-quiz-pro-frontend
  ```
- For the backend part:
  ```
  docker run -d -p 5000:5000 tech-quiz-pro-backend
  ```

4. Open your browser and go to http://localhost:3000 to use the application.


## License

This project is licensed under the [MIT License](LICENSE).
