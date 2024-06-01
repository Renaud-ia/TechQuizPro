
import React from 'react';

function Question({ question, options, handleAnswer }) {
    return (
        <div className="question-container">
            <h2>{question}</h2>
            {options.map((option, index) => (
                <div key={index} className="form-check">
                    <input
                        className="form-check-input"
                        type="radio"
                        name="option"
                        id={`option${index}`}
                        value={option}
                        onChange={() => handleAnswer(option)}
                    />
                    <label className="form-check-label" htmlFor={`option${index}`}>
                        {option}
                    </label>
                </div>
            ))}
        </div>
    );
}

export default Question;
