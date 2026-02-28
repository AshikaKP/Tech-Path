# TechPath - Skill Development Gamified Web Application

A gamified web application for learning tech skills through interactive missions, XP rewards, and career progression.

## Features

### 🎮 Gamification Elements
- **XP System**: Earn experience points for completing lessons and quizzes
- **Leveling**: Progress through levels (0-499 XP: Level 1, 500-999 XP: Level 2, etc.)
- **Badges**: Unlock achievements like Starter, Consistency Master, Skill Builder
- **Skill Tree**: Visual progression map with locked/unlocked skills

### 📚 Learning System
- **Career Paths**: Start with Frontend Development (expandable to more careers)
- **Skill Missions**: Each skill includes lessons and interactive quizzes
- **Progressive Unlocking**: Skills unlock based on user level
- **Final Assessment**: Complete quiz, mini-project, and resume checklist for certification

### 🏆 Achievement System
- **Login Streaks**: Track daily engagement (7-day streak badge)
- **Skill Completion**: Track completed skills (5 skills completed badge)
- **Career Completion**: Final challenge rewards (+200 XP)
- **Certificates**: Generate completion certificates

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, Font Awesome Icons
- **Authentication**: Session-based login system

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open http://127.0.0.1:5000 in your browser

## Project Structure

```
TechPath/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── database.db           # SQLite database (auto-created)
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
│   ├── base.html         # Base template with styling
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── careers.html      # Career selection
│   ├── skills.html       # Skill tree view
│   ├── skill_mission.html# Individual skill missions
│   ├── final.html        # Final assessment
│   └── certificate.html  # Completion certificate
└── README.md            # This file
```

## How It Works

### User Journey
1. **Register** → Create account with name, email, password
2. **Login** → Daily login streak tracking begins
3. **Choose Career** → Select Frontend Development path
4. **Skill Tree** → View available and locked skills
5. **Complete Missions** → Read lessons, take quizzes (+20 XP each)
6. **Level Up** → Unlock new skills as you gain XP
7. **Final Challenge** → Complete quiz, project, resume (+200 XP)
8. **Get Certificate** → Download completion certificate

### XP & Leveling System
- **Skill Completion**: +20 XP per skill
- **Final Challenge**: +200 XP
- **Level Thresholds**:
  - Level 1: 0-60 XP
  - Level 2: 61-120 XP
  - Level 3: 121-180 XP
  - Level 4: 181+ XP

### Badge System
- **Starter**: Default badge for new users
- **Consistency Master**: 7-day login streak
- **Skill Builder**: Complete 5 skills
- **Career Finisher**: Complete final challenge

## Frontend Development Career Path

Skills included:
1. **HTML Fundamentals** (Level 1)
2. **CSS Basics & Layouts** (Level 1)
3. **JavaScript Fundamentals** (Level 1)
4. **Responsive Design** (Level 2)
5. **DOM Manipulation** (Level 2)
6. **Async JavaScript & APIs** (Level 3)
7. **Modern CSS Frameworks** (Level 3)
8. **React Fundamentals** (Level 4)

## Future Enhancements

- Add more career paths (Backend Development, Data Science, etc.)
- Implement real quiz scoring and validation
- Add project submission and review system
- Integrate with GitHub for project portfolios
- Add multiplayer features and leaderboards
- Implement email notifications and reminders
- Add mobile app support

## Contributing

This project was built as a demonstration of gamified learning concepts. Feel free to extend and modify for educational purposes.

## License

Open source - feel free to use and modify for learning purposes.
