from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = "secretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -------------------------
# DATABASE MODELS
# -------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    career = db.Column(db.String(100))
    badge = db.Column(db.String(100), default="Starter")
    skills_completed = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime)
    login_streak = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    career = db.Column(db.String(100))
    name = db.Column(db.String(100))
    required_level = db.Column(db.Integer)

class UserSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    skill_id = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)

# -------------------------
# LEVEL CALCULATION
# -------------------------

def calculate_level(xp):
    if xp < 60:
        return 1
    elif xp < 120:
        return 2
    elif xp < 180:
        return 3
    else:
        return 4

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    return redirect("/login")

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session["user_id"] = user.id
            
            # Update login streak
            now = datetime.utcnow()
            if user.last_login:
                days_since_last = (now - user.last_login).days
                if days_since_last == 1:
                    user.login_streak += 1
                    # Check for 7-day streak badge
                    if user.login_streak >= 7:
                        user.badge = "Consistency Master"
                elif days_since_last > 1:
                    user.login_streak = 1
            else:
                user.login_streak = 1
                user.badge = "Starter"
            
            user.last_login = now
            db.session.commit()
            return redirect("/dashboard")

    return render_template("login.html")

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])
    user.level = calculate_level(user.xp)
    
    # Fix incorrect Career Finisher badge
    if user.badge == "Career Finisher":
        user_skills = UserSkill.query.filter_by(user_id=user.id).all()
        completed_skills = [us for us in user_skills if us.completed]
        if len(completed_skills) < 8:
            user.badge = "Skill Builder" if user.skills_completed >= 5 else "Starter"
    
    db.session.commit()
    return render_template("dashboard.html", user=user)

# CAREER SELECTION
@app.route("/careers")
def careers():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("careers.html")

@app.route("/choose_career/<career>")
def choose_career(career):
    user = User.query.get(session["user_id"])
    user.career = career
    db.session.commit()
    return redirect("/skills")

# SKILLS PAGE
@app.route("/skills")
def skills():
    if "user_id" not in session:
        return redirect("/login")
    
    user = User.query.get(session["user_id"])
    if not user.career:
        return redirect("/careers")
    
    all_skills = Skill.query.filter_by(career=user.career).order_by(Skill.required_level).all()
    user_skills = UserSkill.query.filter_by(user_id=user.id).all()
    completed_skill_ids = [us.skill_id for us in user_skills if us.completed]
    
    return render_template("skills.html", user=user, skills=all_skills, completed_skill_ids=completed_skill_ids)

# SKILL MISSION
@app.route("/skill_mission/<int:skill_id>")
def skill_mission(skill_id):
    if "user_id" not in session:
        return redirect("/login")
    
    user = User.query.get(session["user_id"])
    skill = Skill.query.get(skill_id)
    
    # Check if skill is unlocked based on level
    if user.level < skill.required_level:
        flash("You need to reach level {} to unlock this skill!".format(skill.required_level))
        return redirect("/skills")
    
    return render_template("skill_mission.html", user=user, skill=skill)

# COMPLETE SKILL WITH QUIZ
@app.route("/complete_skill/<int:skill_id>", methods=["POST"])
def complete_skill(skill_id):
    if "user_id" not in session:
        return redirect("/login")
    
    user = User.query.get(session["user_id"])
    skill = Skill.query.get(skill_id)
    
    # Get quiz answers
    q1 = request.form.get("q1")
    q2 = request.form.get("q2") 
    q3 = request.form.get("q3")
    
    # Define correct answers based on skill
    correct_answers = {}
    if skill.name == "HTML Fundamentals":
        correct_answers = {"q1": "a", "q2": "a", "q3": "a"}
    elif skill.name == "CSS Basics & Layouts":
        correct_answers = {"q1": "a", "q2": "a", "q3": "a"}
    else:  # JavaScript and other skills
        correct_answers = {"q1": "a", "q2": "a", "q3": "a"}
    
    # Check if all answers are correct
    score = 0
    if q1 == correct_answers["q1"]:
        score += 1
    if q2 == correct_answers["q2"]:
        score += 1
    if q3 == correct_answers["q3"]:
        score += 1
    
    # Require all 3 answers correct (100%) to pass
    if score == 3:
        user.xp += 20
        user.skills_completed += 1
        user.level = calculate_level(user.xp)
        
        # Mark skill as completed
        user_skill = UserSkill.query.filter_by(user_id=user.id, skill_id=skill_id).first()
        if not user_skill:
            user_skill = UserSkill(user_id=user.id, skill_id=skill_id, completed=True)
            db.session.add(user_skill)
        else:
            user_skill.completed = True
        
        # Badge logic
        if user.skills_completed >= 5:
            user.badge = "Skill Builder"
        
        db.session.commit()
        flash(f"🎉 Congratulations! You completed {skill.name} and earned 20 XP!", "success")
        return redirect("/skills")
    else:
        flash(f"❌ Quiz failed! You got {score}/3 correct. Please study the lesson and try again.", "danger")
        return redirect(f"/skill_mission/{skill_id}")

# FINAL COMPLETION (+200 XP)
@app.route("/final")
def final():
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    user_skills = UserSkill.query.filter_by(user_id=user.id).all()
    completed_skills = [us for us in user_skills if us.completed]

    if len(completed_skills) < 12:
        flash("You need to complete all skills before taking the final challenge!")
        return redirect("/skills")

    # 🔥 THIS MUST BE OUTSIDE THE IF
    user.xp += 200
    user.level = calculate_level(user.xp)
    user.badge = "Career Finisher"

    db.session.commit()

    return redirect("/certificate")

# CERTIFICATE
@app.route("/certificate")
def certificate():
    user = User.query.get(session["user_id"])
    return render_template("certificate.html", user=user)

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# DATABASE DEBUG ROUTE
@app.route("/debug")
def debug():
    if "user_id" not in session:
        return redirect("/login")
    
    user = User.query.get(session["user_id"])
    user_skills = UserSkill.query.filter_by(user_id=user.id).all()
    completed_skills = [us for us in user_skills if us.completed]
    
    debug_info = f"""
    <h2>Database Debug Info</h2>
    <p><strong>User:</strong> {user.name}</p>
    <p><strong>XP in Database:</strong> {user.xp}</p>
    <p><strong>Level:</strong> {user.level}</p>
    <p><strong>Skills Completed Counter:</strong> {user.skills_completed}</p>
    <p><strong>Actual Completed Skills:</strong> {len(completed_skills)}</p>
    <p><strong>Badge:</strong> {user.badge}</p>
    
    <h3>Completed Skills:</h3>
    <ul>
    """
    
    for us in completed_skills:
        skill = Skill.query.get(us.skill_id)
        debug_info += f"<li>{skill.name}</li>"
    
    debug_info += """
    </ul>
    <a href="/reset_progress" class="btn btn-warning">Reset Progress to Match Completed Skills</a>
    <br><br>
    <a href="/dashboard" class="btn btn-primary">Back to Dashboard</a>
    """
    
    return debug_info

# RESET PROGRESS ROUTE
@app.route("/reset_progress")
def reset_progress():
    if "user_id" not in session:
        return redirect("/login")
    
    user = User.query.get(session["user_id"])
    user_skills = UserSkill.query.filter_by(user_id=user.id).all()
    completed_skills = [us for us in user_skills if us.completed]
    
    # Reset XP and level to match actual completed skills
    actual_completed = len(completed_skills)
    user.xp = actual_completed * 20  # 20 XP per skill
    user.level = calculate_level(user.xp)
    user.skills_completed = actual_completed
    
    # Fix badge
    if user.badge == "Career Finisher" and actual_completed < 8:
        user.badge = "Skill Builder" if actual_completed >= 5 else "Starter"
    
    db.session.commit()
    flash("Progress reset to match your actual completed skills!")
    return redirect("/dashboard")

# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
   with app.app_context():
    db.create_all()

    # Add default skills if empty
    if Skill.query.count() == 0:
        skills = [
            # Frontend Development Career Path
            Skill(career="Frontend Development", name="HTML Fundamentals", required_level=1),
            Skill(career="Frontend Development", name="CSS Basics & Layouts", required_level=1),
            Skill(career="Frontend Development", name="JavaScript Fundamentals", required_level=1),
            Skill(career="Frontend Development", name="Responsive Design", required_level=2),
            Skill(career="Frontend Development", name="DOM Manipulation", required_level=2),
            Skill(career="Frontend Development", name="Async JavaScript & APIs", required_level=3),
            Skill(career="Frontend Development", name="Modern CSS Frameworks", required_level=3),
            Skill(career="Frontend Development", name="React Fundamentals", required_level=4),
        ]

        db.session.bulk_save_objects(skills)
        db.session.commit()
    app.run(debug=True)