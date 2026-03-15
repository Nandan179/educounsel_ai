"""
Master Data Generation Script for EduCounsel AI
================================================
This single script consolidates all university data generation previously
spread across add_300_unis.py, add_200_unis.py, and add_400_unis.py.

Run this from the project root (educounsel_ai/) to regenerate all data:
    python data_generation_scripts/generate_all_universities.py
"""

import pandas as pd
import random
import os

# Paths to CSVs - relative to project root
config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config")
uni_csv = os.path.join(config_dir, "world_universities_1000.csv")
course_csv = os.path.join(config_dir, "world_courses_5000.csv")

existing_unis = pd.read_csv(uni_csv)
existing_courses = pd.read_csv(course_csv)
existing_names = set(existing_unis['name'].unique())

new_uni_records = []
new_course_records = []

# ---------------------------------------------------------
# COMMON COURSE TEMPLATES
# ---------------------------------------------------------
course_templates_global = [
    ('B.Sc Computer Science', 15000, 35000, 'Entrance Exam/Merit', '3 or 4 years'),
    ('MBA / Master of Business', 25000, 60000, 'GMAT/GRE/Entrance', '1 or 2 years'),
    ('B.Sc Physics', 12000, 25000, 'Merit Based', '3 or 4 years'),
    ('BBA / Business Administration', 15000, 30000, 'Merit Based', '3 or 4 years'),
    ('M.Sc Data Science', 18000, 40000, 'Entrance/GRE', '1 or 2 years'),
    ('B.A. Economics', 12000, 28000, 'Merit Based', '3 or 4 years'),
    ('MS Artificial Intelligence', 20000, 45000, 'Entrance Exam/Merit', '1 or 2 years'),
    ('Medical Degree / MD', 35000, 80000, 'Entrance Exam', '5+ years')
]
course_templates_india = [
    ('B.Tech Computer Science', 2000, 10000, 'JEE Main / State CET', '4 years'),
    ('MBA', 4000, 15000, 'CAT / MAT / CMAT', '2 years'),
    ('B.Sc Information Technology', 1000, 5000, 'Merit Based', '3 years'),
    ('BBA', 1500, 6000, 'Merit Based', '3 years'),
    ('M.Tech Data Science', 3000, 8000, 'GATE', '2 years')
]
course_templates_germany = [
    ('B.Sc. Informatics', 0, 3000, 'Abitur / Studienkolleg', '3 years'),
    ('M.Sc. Data Engineering', 0, 3000, 'Bachelor Degree', '2 years'),
    ('B.A. Business Administration', 0, 3000, 'Abitur', '3 years'),
    ('M.Sc. Automotive Engineering', 0, 3000, 'Bachelor Degree', '2 years'),
    ('M.Sc. Renewable Energy', 0, 3000, 'Bachelor / IELTS', '2 years')
]


def add_universities(names_locs, country, accreditations, templates, target, uni_type_fn=None):
    """Helper to add up to target universities for a given country."""
    added = 0
    for name, loc in names_locs:
        if added >= target:
            break
        if name not in existing_names:
            uni_type = uni_type_fn() if uni_type_fn else random.choice(['Public', 'Private'])
            ranking = round(random.uniform(6.0, 9.9), 1)
            accreditation = random.choice(accreditations)
            actual_location = f"{loc}, {country}"
            new_uni_records.append([name, country, uni_type, ranking, accreditation, actual_location])
            existing_names.add(name)
            for c in random.sample(templates, min(random.randint(3, 4), len(templates))):
                fees = random.randint(c[1], c[2]) if c[2] > 0 else random.choice([0, 500, 1500])
                new_course_records.append([name, c[0], fees, c[3], c[4]])
            added += 1
    return added


# ---------------------------------------------------------
# SECTION 1: USA
# ---------------------------------------------------------
us_states = ["California", "Texas", "New York", "Florida", "Illinois", "Pennsylvania", "Ohio", "Georgia",
             "North Carolina", "Michigan", "New Jersey", "Virginia", "Washington", "Arizona", "Massachusetts"]
us_cities = ["Atlanta", "Boston", "Chicago", "Dallas", "Denver", "Houston", "Los Angeles", "Miami",
             "New York", "Philadelphia", "Phoenix", "San Francisco", "Seattle", "Washington D.C."]
us_prefixes = ["State University", "University of", "Institute of Technology", "A&M", "Polytechnic"]
us_names = []
for s in us_states:
    for p in us_prefixes:
        us_names.append((f"{p} {s}" if p.startswith("Univ") else f"{s} {p}", s))
for c in us_cities:
    for p in us_prefixes:
        us_names.append((f"{p} {c}" if p.startswith("Univ") else f"{c} {p}", c))
random.shuffle(us_names)
us_added = add_universities(us_names, "United States",
    ["ABET", "AACSB", "Higher Learning Commission", "WASC", "NECHE"], course_templates_global, 100)

# ---------------------------------------------------------
# SECTION 2: UK
# ---------------------------------------------------------
uk_cities = ["London", "Manchester", "Birmingham", "Edinburgh", "Glasgow", "Liverpool", "Bristol",
             "Leeds", "Sheffield", "Newcastle", "Nottingham", "Cardiff", "Belfast", "Oxford", "Cambridge"]
uk_prefixes = ["University of", "Metropolitan University", "City University", "Royal College", "Business School"]
uk_names = []
for c in uk_cities:
    for p in uk_prefixes:
        uk_names.append((f"{p} {c}" if p.startswith("Univ") else f"{c} {p}", c))
random.shuffle(uk_names)
uk_added = add_universities(uk_names, "United Kingdom",
    ["Russell Group", "UKVI Approved", "QAA", "AMBA", "EQUIS"], course_templates_global, 100)

# ---------------------------------------------------------
# SECTION 3: JAPAN
# ---------------------------------------------------------
jp_cities = ["Tokyo", "Yokohama", "Osaka", "Nagoya", "Sapporo", "Fukuoka", "Kobe", "Kyoto",
             "Kawasaki", "Saitama", "Hiroshima", "Sendai", "Chiba", "Kitakyushu"]
jp_prefixes = ["University of", "Institute of Technology", "Imperial University", "Metropolitan University", "International University"]
jp_names = []
for c in jp_cities:
    for p in jp_prefixes:
        jp_names.append((f"{p} {c}", c))
random.shuffle(jp_names)
jp_added = add_universities(jp_names, "Japan",
    ["MEXT Approved", "NIAD-QE", "JABEE", "AACSB"], course_templates_global, 100,
    lambda: "Public" if random.random() > 0.3 else "Private")

# ---------------------------------------------------------
# SECTION 4: SINGAPORE
# ---------------------------------------------------------
sg_regions = ["Jurong", "Clementi", "Tampines", "Woodlands", "Novena", "Queenstown", "Bedok",
              "Punggol", "Bukit Batok", "Yishun", "Sengkang", "Serangoon", "Pasir Ris"]
sg_prefixes = ["Singapore Institute of", "National University of", "Management University of", "Polytechnic", "Global University"]
sg_names = []
for l in sg_regions:
    for p in sg_prefixes:
        sg_names.append((f"{p} {l}" if p.endswith("of") else f"{l} {p}", "Singapore"))
random.shuffle(sg_names)
sg_added = add_universities(sg_names, "Singapore",
    ["Edutrust", "CPE Approved", "AACSB", "EQUIS", "ABET"], course_templates_global, 100)

# ---------------------------------------------------------
# SECTION 5: INDIA
# ---------------------------------------------------------
indian_states = ["Maharashtra", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "Gujarat", "Kerala",
                 "Rajasthan", "Madhya Pradesh", "West Bengal", "Punjab", "Haryana", "Telangana"]
indian_cities = ["Mumbai", "Pune", "Bangalore", "Chennai", "Delhi", "Ahmedabad", "Surat", "Jaipur",
                 "Kochi", "Lucknow", "Nagpur", "Indore", "Hyderabad"]
india_prefixes = ["Institute of Technology", "National Institute", "University", "Vidyapeeth",
                  "Academy", "Engineering College", "Institute of Management"]
india_names = []
for s in indian_states:
    for p in india_prefixes:
        india_names.append((f"{s} {p}", s))
for c in indian_cities:
    for p in india_prefixes:
        india_names.append((f"{p} {c}", c))
random.shuffle(india_names)
india_added = add_universities(india_names, "India",
    ["NAAC A++", "NAAC A+", "UGC Approved", "AICTE Approved", "NBA Accredited"], course_templates_india, 100)

# ---------------------------------------------------------
# SECTION 6: GERMANY
# ---------------------------------------------------------
german_states = ["Bavaria", "Baden-Württemberg", "North Rhine-Westphalia", "Hesse", "Saxony",
                 "Lower Saxony", "Rhineland-Palatinate", "Berlin", "Hamburg", "Thuringia"]
german_cities = ["Munich", "Berlin", "Hamburg", "Frankfurt", "Stuttgart", "Cologne", "Düsseldorf",
                 "Leipzig", "Dresden", "Hannover", "Nuremberg", "Aachen", "Heidelberg"]
germany_prefixes = ["Technical University of", "University of Applied Sciences", "University of",
                    "Hochschule", "Fachhochschule", "International University"]
germany_names = []
for s in german_states:
    for p in germany_prefixes:
        germany_names.append((f"{p} {s}", s))
for c in german_cities:
    for p in germany_prefixes:
        germany_names.append((f"{p} {c}", c))
random.shuffle(germany_names)
germany_added = add_universities(germany_names, "Germany",
    ["Wissenschaftsrat", "FIBAA", "ASIIN", "AQAS", "State Accredited"], course_templates_germany, 100,
    lambda: "Public" if random.random() > 0.2 else "Private")

# ---------------------------------------------------------
# SAVE RESULTS
# ---------------------------------------------------------
df_new_unis = pd.DataFrame(new_uni_records, columns=['name', 'location', 'university_type', 'ranking_score', 'accreditation', 'actual_location'])
df_unis_final = pd.concat([existing_unis, df_new_unis], ignore_index=True)
df_unis_final.to_csv(uni_csv, index=False)

df_new_courses = pd.DataFrame(new_course_records, columns=['university', 'course_name', 'annual_fees', 'admission_mode', 'duration'])
df_courses_final = pd.concat([existing_courses, df_new_courses], ignore_index=True)
df_courses_final.to_csv(course_csv, index=False)

print("== Data Generation Complete ==")
print(f"  USA:       {us_added} new universities")
print(f"  UK:        {uk_added} new universities")
print(f"  Japan:     {jp_added} new universities")
print(f"  Singapore: {sg_added} new universities")
print(f"  India:     {india_added} new universities")
print(f"  Germany:   {germany_added} new universities")
print(f"\n  TOTAL UNIQUE UNIVERSITIES: {len(df_unis_final['name'].unique())}")
print(f"  TOTAL COURSES:             {len(df_courses_final)}")
