A Flask-based vocabulary learning application with performance-driven revision.

Vocab Improver
Vocab Improver is a Flask-based web application that helps users improve their vocabulary through multiple-choice quizzes, performance tracking, and mistake-focused revision. The system prioritizes words the user struggles with instead of relying on fixed time-based repetition.

Features
Vocabulary management
Add new words with definitions
View all stored words and meanings
MCQ-based quizzes
Each question shows a definition
Users choose the correct word from multiple options
Distractors are selected based on word difficulty (weights)
Accuracy tracking
Tracks how many times each word is asked
Tracks correct attempts per word
Calculates per-word accuracy and overall accuracy
Mistake-focused learning
Words answered incorrectly are more likely to reappear
No fixed spaced-repetition schedule, only performance-based prioritization
User system
Login and signup support
Vocabulary progress stored in a SQLite database

Tech Stack
Backend: Python, Flask
Database: SQLite
Frontend: HTML, Jinja templates
Version Control: Git, GitHub

Project Structure
Vocab_improver/
│
├── main.py            # Flask app and routes
├── trainer.py         # Quiz logic, word selection, stats handling
├── models.py          # Database schema and DB utilities
│
├── templates/
│   ├── home.html
│   ├── add.html
│   ├── quiz.html
│   ├── result.html
│   ├── all_words.html
│   ├── login.html
│   ├── signup.html
│
├── words.db           # SQLite database (ignored in production)
└── README.md

How It Works
Users add vocabulary words.
Each word is stored with a weight representing difficulty.

During quizzes:
A word is selected based on weight.
MCQ options are generated from words in a similar difficulty range.

After each answer:
Accuracy statistics are updated.
Incorrect words gain priority in future quizzes.
Users can view detailed results and overall accuracy.
Why This Project
This project demonstrates:
Backend logic beyond basic CRUD
Database-driven decision making
Performance-based learning systems
Clean separation of logic, database, and templates
It is suitable as an internship-level backend project and can be extended further.

Future Improvements
Pandas-based analytics for deeper insights
Visual charts for accuracy trends
Improved MCQ distractor generation
Better UI styling
Deployment to a cloud platform

Setup Instructions
git clone https://github.com/keshavmodi07/Vocab_improver.git
cd Vocab_improver
pip install flask
python main.py

Open http://127.0.0.1:5000/ in your browser.

Author

Keshav Modi
Student | Python | Backend Development
