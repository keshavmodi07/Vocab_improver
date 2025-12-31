from flask import Flask,render_template,request,redirect,url_for
from trainer import WordTrainer
from models import init_db,reset_db,login
app=Flask(__name__)
trainer = WordTrainer()
init_db()
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/add",methods=["GET","POST"])
def add_word():
    msg=None
    if request.method=="POST":
        if "reset" in request.form:
            return redirect(url_for("reset"))
        else:
            word=request.form["word"].strip()
            msg=trainer.add_word(word)
    return render_template("add.html",msg=msg)
    
@app.route("/quiz")
def quiz():
    word = trainer.pick_word()
    quiz_data=trainer.quiz_generator(word) if word else None
    if quiz_data:
        return render_template("quiz.html",quiz_data=quiz_data,zip=zip)
    else:
        return redirect(url_for("add_word"))
@app.route("/answer",methods=["POST"])
def answer():
    if "results" in request.form:
        return redirect(url_for("result"))
    word_id=request.form["word_id"]
    user_answer=request.form["answer"].strip().upper()
    correct=request.form["correct"]
    trainer.update_stats(word_id,user_answer==correct)
    return redirect(url_for("quiz"))

@app.route("/results")
def result():
    stats=trainer.get_stats()
    progress=trainer.results(stats)
    return render_template("result.html", progress=progress)
@app.route("/reset")
def reset():
    reset_db()
    return redirect(url_for("add_word"))
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        user_data = trainer.login_me(username, password)
        if user_data==True:
            return redirect(url_for("add_word"))
        elif user_data==None:
            msg = "User not found. Please sign up."
            return render_template("login.html", msg=msg)
        else:
            msg="Invalid credentials Try signing up."
            return render_template("login.html", msg=msg)
    return render_template("login.html")
@app.route("/signup",methods=["GET","POST"])
def signup():
    msg=None
    if request.method=="POST":
        username=request.form["new_username"]
        password=request.form["new_password"]
        signup_status=trainer.signup_me(username,password)
        if signup_status==True:
            return redirect(url_for("home"))
        else:
            msg="Username already exists. Try a different one or login."
    return render_template("signup.html", msg=msg)
@app.route("/all_words")
def all_words():
    word,meaning=trainer.get_all_words()
    return render_template("all_words.html",word=word,meaning=meaning,zip=zip)
if __name__=="__main__":
    app.run(debug=True)