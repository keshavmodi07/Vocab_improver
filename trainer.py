import random
import requests
from models import get_db,login
class WordTrainer:
    def add_word(self,word):
        r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if r.status_code!=200:
            return "Invalid word!"
        definition= r.json()[0]["meanings"][0]["definitions"][0]["definition"]
        try:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO words (word, definition) VALUES (?, ?)",
                    (word,definition)
                )
        except:
            return "The word already exists! "
        return definition
    def get_active_words(self):
        with get_db() as conn:
            return conn.execute(
                "SELECT * FROM words WHERE weight < 100"
            ).fetchall()
        
    def pick_word(self):
        words = self.get_active_words()
        inv_weights = [float(1 / w[3]) if w[3] > 0 else 1.0 for w in words]
        if inv_weights:       
            return (random.choices(words,weights=inv_weights)[0])
    def update_stats(self, word_id, correct):
        with get_db() as conn:
            if correct:
                conn.execute("""
                    UPDATE words
                    SET weight = weight + 10,
                        times_correct = times_correct + 1,
                        times_asked = times_asked + 1
                    WHERE id = ?
                """, (word_id,))
            else:
                conn.execute("""
                    UPDATE words
                    SET weight = weight + 5,
                        times_asked = times_asked + 1
                    WHERE id = ?
                """, (word_id,))
            conn.commit()
    def get_stats(self):
        with get_db() as conn:
            return conn.execute(
                "SELECT * FROM words ",
            ).fetchall()
    def results(self, stats):
        words=[stat[1]for stat in stats]
        asked=[stat[4]for stat in stats]
        correct=[stat[5]for stat in stats]
        accuracy=[(stat[5]/stat[4]*100)if stat[4]>0 else 0 for stat in stats]
        total_correct=sum(correct)
        total_asked=sum(asked)
        total_accuracy=sum(accuracy)/len(accuracy)if len(accuracy)>0 else 0
        length=len(words)
        progress={
            "words":words,
            "asked":asked,
            "correct":correct,
            "accuracy":accuracy,
            "total_correct":total_correct,
            "total_asked":total_asked,
            "total_accuracy":total_accuracy,
            "length":length
        }
        return progress
    def generate_mcq(self, word):
        ranges = [25, 50, 100, 300]
        rows=[]
        with get_db() as conn:
            for r in ranges:
                ro=(conn.execute("""
                SELECT * FROM words
                WHERE id != ?
                  AND weight BETWEEN ? AND ?
                ORDER BY RANDOM()
                LIMIT 3
                """, (word[0], abs(int(word[3]) - r), int(word[3]) + r)).fetchall())
                if ro:
                    rows.append(ro)
                if len(rows) >= 3:
                    break
            if len(rows) < 3:
                ro=conn.execute("""
                SELECT * FROM words
                WHERE id != ?
                ORDER BY RANDOM()
                LIMIT 3
                """, (word[0],)).fetchall()
                if ro:
                    rows.append(ro)
        if len(rows) >3:
            rows = rows[:3]
        rows=rows[0]
        options_pool=[rows[i][1]for i in range(len(rows))]
        options_pool.append(word[1])
        random.shuffle(options_pool)
        labels = ['A', 'B', 'C', 'D']
        correct_label = labels[options_pool.index(word[1])]
        return options_pool, labels, correct_label
    def quiz_generator(self,word):
        options, labels, correct_label = self.generate_mcq(word)
        word_id=word[0]
        definition=word[2]
        quiz_data={
            "options":options,
            "labels":labels,
            "correct_label":correct_label,
            "word_id":word_id,
            "definition":definition
        }
        return quiz_data
    def login_me(self, username, password):
        with get_db() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            ).fetchone()
            if user:
                for data in user:
                    if data[1]==username and data[2]==password:
                        return True
                    else:
                        return False
            else:
                return None
    def signup_me(self, username, password):
        with get_db() as conn:
            try:
                conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
                return True
            except:
                return False
    def get_all_words(self):
        with get_db() as conn:
            words=conn.execute(
                "SELECT * FROM words"
            ).fetchall()
            word,meaning=[words[i][1]for i in range(len(words))],[words[i][2]for i in range(len(words))]
            return word,meaning