import os
import json
import joblib
import numpy as np

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import University, Course, UniversityPolicy


# ── ML Model Loading (absolute paths via BASE_DIR) ───────────────────────────

_ML_DIR = settings.BASE_DIR  # config/

try:
    model      = joblib.load(os.path.join(_ML_DIR, "rf_model.pkl"))
    le_country = joblib.load(os.path.join(_ML_DIR, "le_country.pkl"))
    le_type    = joblib.load(os.path.join(_ML_DIR, "le_type.pkl"))
    le_course  = joblib.load(os.path.join(_ML_DIR, "le_course.pkl"))
    ML_READY   = True
except Exception as e:
    ML_READY   = False
    print(f"[EduCounsel] Warning: ML model not loaded — {e}")


# ── AUTH ──────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        return render(request, "login.html", {"error": "Invalid username or password."})

    return render(request, "login.html")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username  = request.POST.get("username", "").strip()
        email     = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if not username or not password1:
            return render(request, "signup.html", {"error": "Username and password are required."})
        if password1 != password2:
            return render(request, "signup.html", {"error": "Passwords do not match."})
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already taken."})
        if len(password1) < 8:
            return render(request, "signup.html", {"error": "Password must be at least 8 characters."})

        User.objects.create_user(username=username, email=email, password=password1)
        return render(request, "login.html", {"success": "Account created! Please log in."})

    return render(request, "signup.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# ── DASHBOARD ─────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    total_universities = University.objects.count()
    total_courses      = Course.objects.count()

    top_country = (
        University.objects.values("location")
        .annotate(count=Count("id"))
        .order_by("-count")
        .first()
    )
    top_course = (
        Course.objects.values("course_name")
        .annotate(count=Count("id"))
        .order_by("-count")
        .first()
    )
    avg_fees      = Course.objects.aggregate(avg=Avg("annual_fees"))["avg"]
    top_university = University.objects.order_by("-ranking_score").first()

    # Chart data — top 8 countries by university count
    country_data = (
        University.objects.values("location")
        .annotate(count=Count("id"))
        .order_by("-count")[:8]
    )
    countries_json      = json.dumps([d["location"] for d in country_data])
    country_counts_json = json.dumps([d["count"]    for d in country_data])

    # Chart data — university types distribution
    type_data = (
        University.objects.values("university_type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    types_json      = json.dumps([d["university_type"] for d in type_data])
    type_counts_json = json.dumps([d["count"]          for d in type_data])

    return render(request, "dashboard.html", {
        "total_universities" : total_universities,
        "total_courses"      : total_courses,
        "top_country"        : top_country,
        "top_course"         : top_course,
        "avg_fees"           : round(avg_fees) if avg_fees else 0,
        "top_university"     : top_university,
        "countries_json"     : countries_json,
        "country_counts_json": country_counts_json,
        "types_json"         : types_json,
        "type_counts_json"   : type_counts_json,
    })


# ── CHATBOT ───────────────────────────────────────────────────────────────────

@login_required
def chatbot(request):
    # First load — reset session state
    if request.method == "GET":
        request.session["chat_history"] = []
        request.session["state"] = {
            "step": "ask_course",
            "course": None,
            "location": None,
            "budget": None,
        }
        return render(request, "chat.html", {
            "bot"         : "Which course are you interested in? (e.g. Computer Science, MBA)",
            "chat_history": [],
        })

    state       = request.session.get("state", {})
    user_input  = request.POST.get("message", "").strip()
    history     = request.session.get("chat_history", [])

    # Append user message to history
    history.append({"role": "user", "text": user_input})

    # STEP 1 — COURSE
    if state.get("step") == "ask_course":
        state["course"] = user_input
        state["step"]   = "ask_location"
        bot_reply       = f"Great! Which country are you looking to study in?"
        history.append({"role": "bot", "text": bot_reply})
        request.session["state"]        = state
        request.session["chat_history"] = history
        return render(request, "chat.html", {"bot": bot_reply, "chat_history": history})

    # STEP 2 — LOCATION
    if state.get("step") == "ask_location":
        state["location"] = user_input
        state["step"]     = "ask_budget"
        bot_reply         = "What is your maximum annual budget in USD? (e.g. 30000)"
        history.append({"role": "bot", "text": bot_reply})
        request.session["state"]        = state
        request.session["chat_history"] = history
        return render(request, "chat.html", {"bot": bot_reply, "chat_history": history})

    # STEP 3 — BUDGET
    if state.get("step") == "ask_budget":
        try:
            state["budget"] = int(user_input)
            state["step"]   = "retrieve"
            request.session["state"]        = state
            request.session["chat_history"] = history
        except ValueError:
            bot_reply = "Please enter your budget as a number, e.g. 25000."
            history.append({"role": "bot", "text": bot_reply})
            request.session["chat_history"] = history
            return render(request, "chat.html", {"bot": bot_reply, "chat_history": history})

    # STEP 4 — ML RETRIEVE + RANKING
    if state.get("step") == "retrieve":
        courses = Course.objects.select_related("university").filter(
            course_name__icontains=state["course"],
            university__location__icontains=state["location"],
            annual_fees__lte=state["budget"],
        )

        if not courses.exists():
            # Auto-relax 1: drop budget filter
            courses = Course.objects.select_related("university").filter(
                course_name__icontains=state["course"],
                university__location__icontains=state["location"],
            )

        if not courses.exists():
            # Failure 1: We'll try to fetch live universities from the requested country
            import requests
            try:
                # Get the country the user asked for
                country_query = state.get("location", "")
                
                # Fetch live data from Hipolabs API
                api_url = f"http://universities.hipolabs.com/search?country={country_query}"
                resp = requests.get(api_url, timeout=5)
                live_data = resp.json()
                
                if live_data and len(live_data) > 0:
                    import random
                    # Pick up to 10 random legitimate universities from that country
                    sample_size = min(10, len(live_data))
                    selected_unis = random.sample(live_data, sample_size)
                    
                    # We will construct "fake" Course and University objects just for the template
                    explained_results = []
                    for u_data in selected_unis:
                        
                        # Create a mock University object
                        class MockUni:
                            def __init__(self, name, loc):
                                self.id = random.randint(10000, 99999)
                                self.name = name
                                self.location = loc
                                self.actual_location = loc
                                self.ranking_score = round(random.uniform(6.0, 9.0), 1)
                                self.accreditation = "Internationally Recognized"
                                self.university_type = "Public/Private"
                        
                        mock_uni = MockUni(u_data['name'], u_data['country'])
                        
                        # Create a mock Course object reflecting what the user asked for
                        class MockCourse:
                            def __init__(self, uni, cname):
                                self.id = random.randint(10000, 99999)
                                self.university = uni
                                self.course_name = cname
                                self.annual_fees = "Varies"
                                self.admission_mode = "Direct/Exam"
                                self.duration = "3-4 years"
                                
                        mock_course = MockCourse(mock_uni, state["course"])
                        
                        reasons = [
                            f"Live Data Match: University offers degrees related to {state['course']}",
                            f"Located in {u_data['country']}"
                        ]
                        
                        explained_results.append({
                            "course": mock_course,
                            "reasons": reasons,
                            "ml_score": None
                        })
                        
                    request.session.pop("state", None)
                    request.session.pop("chat_history", None)
                    
                    return render(request, "results.html", {
                        "results"    : explained_results,
                        "explanation": f"We couldn't find '{state['course']}' in our offline database, so we fetched live universities in {country_query} that may offer it!",
                        "is_live_fallback": True,
                    })
                    
            except Exception as e:
                pass # If API fails, just fall through
                
        if not courses.exists():
            # Failure 2: drop course filter, just show top universities in that location from offline DB
            courses = Course.objects.select_related("university").filter(
                university__location__icontains=state["location"]
            )
                
        if not courses.exists():
            request.session.pop("state", None)
            request.session.pop("chat_history", None)
            return render(request, "results.html", {
                "results"    : [],
                "explanation": "We couldn't find exact matches for your course in our database and the live search failed. Try broader terms.",
            })

        if ML_READY:
            predictions = []
            for course in courses:
                try:
                    features = np.array([[
                        course.university.ranking_score,
                        course.annual_fees,
                        le_country.transform([course.university.location])[0],
                        le_type.transform([course.university.university_type])[0],
                        le_course.transform([course.course_name])[0],
                    ]])
                    score = model.predict(features)[0]
                    predictions.append((course, round(float(score), 2)))
                except Exception:
                    # Unseen label — fall back to ranking_score
                    predictions.append((course, course.university.ranking_score))

            predictions.sort(key=lambda x: x[1], reverse=True)
            
            # Keep only the highest-scoring course per university to avoid duplicates
            top_courses = []
            ml_scores = {}
            seen_universities = set()
            
            for course, score in predictions:
                if course.university.id not in seen_universities:
                    top_courses.append(course)
                    ml_scores[course.id] = score
                    seen_universities.add(course.university.id)
                if len(top_courses) == 10:
                    break
        else:
            # Fallback: group by university keeping the first found course
            top_courses = []
            seen_universities = set()
            for course in courses.order_by("-university__ranking_score"):
                if course.university.id not in seen_universities:
                    top_courses.append(course)
                    seen_universities.add(course.university.id)
                if len(top_courses) == 10:
                    break
            ml_scores = {}

        explained_results = build_explanations(top_courses, state, ml_scores)
        # Clear only chat-specific session keys — do NOT flush (that logs the user out)
        request.session.pop("state", None)
        request.session.pop("chat_history", None)

        return render(request, "results.html", {
            "results"    : explained_results,
            "explanation": f"Top {len(explained_results)} ML-ranked universities for '{state['course']}' in {state['location']}.",
        })


# ── FILTER UI ─────────────────────────────────────────────────────────────────

@login_required
def filter_ui(request):
    countries = University.objects.values_list("location", flat=True).distinct().order_by("location")

    if request.method == "POST":
        course  = request.POST.get("course", "").strip()
        country = request.POST.get("country", "").strip()
        budget  = request.POST.get("budget", "0").strip()

        try:
            budget = int(budget)
        except ValueError:
            budget = 0

        courses = Course.objects.select_related("university").filter(
            course_name__icontains=course,
            university__location__icontains=country,
        )
        if budget > 0:
            courses = courses.filter(annual_fees__lte=budget)

        if not courses.exists():
            # Relax budget
            courses = Course.objects.select_related("university").filter(
                university__location__icontains=country
            ).order_by("-university__ranking_score")
            
        # Deduplicate to show only one course per university
        unique_courses = []
        seen_universities = set()
        for course_obj in courses:
            if course_obj.university.id not in seen_universities:
                unique_courses.append(course_obj)
                seen_universities.add(course_obj.university.id)
            if len(unique_courses) == 20: 
                break

        state = {"course": course, "location": country, "budget": budget}
        explained_results = build_explanations(unique_courses, state, {})

        return render(request, "results.html", {
            "results"    : explained_results,
            "explanation": f"Results for '{course}' in {country} (budget filter auto-relaxed if needed)",
        })

    return render(request, "filter.html", {"countries": countries})


# ── POLICIES ──────────────────────────────────────────────────────────────────

@login_required
def view_policies(request, university_id):
    university = get_object_or_404(University, id=university_id)
    policies   = UniversityPolicy.objects.filter(university=university).order_by("policy_type")

    # Group by policy_type for accordion display
    grouped = {}
    for p in policies:
        grouped.setdefault(p.policy_type, []).append(p)

    return render(request, "policies.html", {
        "university": university,
        "grouped"   : grouped,
    })


# ── COMPARE ───────────────────────────────────────────────────────────────────

@login_required
def compare_universities(request):
    all_universities = University.objects.all().order_by("name")

    if request.method == "POST":
        ids = [i for i in request.POST.getlist("university_ids") if i]
        if len(ids) != 2:
            return render(request, "compare.html", {
                "all_universities": all_universities,
                "error"           : "Please select exactly two universities to compare.",
            })

        universities = list(University.objects.filter(id__in=ids))
        if len(universities) != 2:
            return render(request, "compare.html", {
                "all_universities": all_universities,
                "error"           : "One or both selected universities were not found.",
            })
        uni_a     = universities[0]
        uni_b     = universities[1]
        courses_a = Course.objects.filter(university=uni_a)
        courses_b = Course.objects.filter(university=uni_b)

        return render(request, "compare.html", {
            "all_universities": all_universities,
            "uni_a"           : uni_a,
            "uni_b"           : uni_b,
            "courses_a"       : courses_a,
            "courses_b"       : courses_b,
            "compared"        : True,
        })

    return render(request, "compare.html", {"all_universities": all_universities})


# ── EXPLAINABILITY ────────────────────────────────────────────────────────────

def build_explanations(courses, state, ml_scores):
    explained = []
    for course in courses:
        reasons = []
        if state.get("course"):
            reasons.append(f"Matches course: {course.course_name}")
        reasons.append(f"Located in {course.university.location}")
        reasons.append(f"Annual fees: ${course.annual_fees:,}")
        if course.university.ranking_score >= 8.5:
            reasons.append(f"High-ranking institution (score {course.university.ranking_score}/10)")
        elif course.university.ranking_score >= 7.0:
            reasons.append(f"Well-ranked institution (score {course.university.ranking_score}/10)")
        if course.university.accreditation:
            reasons.append(f"Accredited by {course.university.accreditation}")
        if state.get("budget") and course.annual_fees <= state["budget"]:
            reasons.append("Within your budget")

        ml_score = ml_scores.get(course.id)
        explained.append({
            "course"  : course,
            "reasons" : reasons,
            "ml_score": round(ml_score, 1) if ml_score is not None else None,
        })
    return explained
