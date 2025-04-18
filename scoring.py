def score_resume(text, ai_keywords):
    """Enhanced scoring function with more comprehensive criteria"""
    score = 0
    feedback = []
    
    # Content length (10%)
    if len(text) > 1500:
        score += 10
        feedback.append("Excellent content length and detail ✅")
    elif len(text) > 1000:
        score += 7
        feedback.append("Good content length 👍")
    else:
        feedback.append("Resume content too short ❌")
    
    
    # Education (20%)
    education_score = 0
    if "phd" in text.lower() or "doctorate" in text.lower():
        education_score += 20
        feedback.append("PhD level education detected 🎓")
    elif "master" in text.lower():
        education_score += 15
        feedback.append("Master's degree detected 🎓")
    elif "bachelor" in text.lower():
        education_score += 10
        feedback.append("Bachelor's degree detected 🎓")
    score += education_score
    
    # Experience (30%)
    experience_score = 0
    if "experience" in text.lower() or "work history" in text.lower():
        experience_score += 15
        feedback.append("Professional experience noted 💼")
    if "intern" in text.lower():
        experience_score += 5
        feedback.append("Internship experience noted 📝")
    if "project" in text.lower():
        experience_score += 10
        feedback.append("Project experience noted 📂")
    score += experience_score
    
    # AI Keywords (20%)
    if ai_keywords and ai_keywords[0] != "None":
        score += 20
        feedback.append(f"AI keywords found: {', '.join(ai_keywords)} 🧠")
    else:
        feedback.append("No AI keywords detected ❌")
    
    # Formatting (10%)
    word_count = len(text.split())
    if 300 < word_count < 800:
        score += 10
        feedback.append("Good formatting and clarity 👍")
    elif word_count >= 800:
        score += 5
        feedback.append("Content might be too dense 📝")
    else:
        feedback.append("Formatting may be too sparse 📝")
    
    # Skills section (10%)
    if "skills" in text.lower():
        score += 10
        feedback.append("Skills section detected ✅")
    
    # Ensure score doesn't exceed 100
    score = min(score, 100)
    
    return {
        "score": score,
        "feedback": feedback
    }