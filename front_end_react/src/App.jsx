import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Question from './components/Question';
import axios from 'axios';
import { Alert } from 'bootstrap';
import cors from 'cors';

function App() {
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState([]);

    const questions = [
        {
            question: 'What kind of developer job are you looking for?',
            options: ['Frontend', 'Backend', 'FullStack'],
        },
        {
            question: 'How much experience do you have?',
            options: ['Junior', 'Senior'],
        },
        {
            question: 'What type of Frontend language do they use?',
            options: ['React', 'Angular', 'Vue'],
            condition: (answers) => answers.some(answer => answer.answer === 'Frontend'),
        },
        {
            question: 'What backend language do they use?',
            options: ['Node.js', 'Python', 'Java'],
            condition: (answers) => answers.some(answer => answer.answer === 'Backend'),
        }
    ];

    const getNextQuestionIndex = () => {
        for (let i = currentQuestionIndex + 1; i < questions.length; i++) {
            if (!questions[i].condition || questions[i].condition(answers)) {
                return i;
            }
        }
        return questions.length;
    };

    const handleAnswer = (answer) => {
        const updatedAnswers = [...answers, { question: questions[currentQuestionIndex].question, answer }];
        setAnswers(updatedAnswers);

        const nextQuestionIndex = getNextQuestionIndex();
        setCurrentQuestionIndex(nextQuestionIndex);
        console.log(answers.length)
        if (answers.length == 2) {
          sendAnswersToServer(answers);
      }
    };


    const sendAnswersToServer = async (answers) => {
      try {
          const response = await axios.post('http://localhost:3000/', { "job":answers[0],"experience":answers[1],"technologies":[answers[2]] },
        );
          console.log('response:', response.data);
      } catch (error) {
          console.error('Error server:', error);
      }
  };
    return (
        <div className="App container">
            <header className="App-header">
                <h1>Training Interview Job</h1>
            </header>
            {currentQuestionIndex < questions.length ? (
                <Question
                    question={questions[currentQuestionIndex].question}
                    options={questions[currentQuestionIndex].options}
                    handleAnswer={handleAnswer}
                />
            ) : (
                <div>
                    <h2>Results:</h2>
                    <ul>
                        {answers.map((answer, index) => (
                            <li key={index}>{answer.question}: {answer.answer}</li>
                        )) }
                    </ul>
                </div>
                
            )}
        </div>
    );
}

export default App;
