import pandas as pd
import random
import os

# Paths to CSVs
config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
uni_csv = os.path.join(config_dir, "world_universities_1000.csv")
course_csv = os.path.join(config_dir, "world_courses_5000.csv")

existing_unis = pd.read_csv(uni_csv)
existing_courses = pd.read_csv(course_csv)
existing_names = set(existing_unis['name'].unique())

new_uni_records = []
new_course_records = []

# --- CONFIG ---
types = ['Public', 'Private']
course_templates = [
    ('B.Sc Computer Science', 15000, 35000, 'Entrance Exam/Merit', '3 or 4 years'),
    ('MBA / Master of Business', 25000, 60000, 'GMAT/GRE/Entrance', '1 or 2 years'),
    ('B.Sc Physics', 12000, 25000, 'Merit Based', '3 or 4 years'),
    ('BBA / Business Administration', 15000, 30000, 'Merit Based', '3 or 4 years'),
    ('M.Sc Data Science', 18000, 40000, 'Entrance/GRE', '1 or 2 years'),
    ('B.A. Economics', 12000, 28000, 'Merit Based', '3 or 4 years'),
    ('MS Artificial Intelligence', 20000, 45000, 'Entrance Exam/Merit', '1 or 2 years'),
    ('Medical Degree / MD', 35000, 80000, 'Entrance Exam', '5+ years')
]

# --- UK ---
uk_cities = ["London", "Manchester", "Birmingham", "Edinburgh", "Glasgow", "Liverpool", "Bristol", "Leeds", "Sheffield", "Newcastle", "Nottingham", "Cardiff", "Belfast", "Southampton", "Leicester", "Coventry", "Oxford", "Cambridge", "York"]
uk_prefixes = ["University of", "Metropolitan University", "City University", "Institute", "Royal College"]

uk_names = []
for c in uk_cities:
    for p in uk_prefixes:
        if p.startswith("Univ"): uk_names.append((f"{p} {c}", c))
        else: uk_names.append((f"{c} {p}", c))
    uk_names.append((f"{c} College London", c))
random.shuffle(uk_names)

uk_added = 0
for name, loc in uk_names:
    if uk_added >= 100: break
    if name not in existing_names:
        ranking = round(random.uniform(7.0, 9.8), 1)
        accreditation = random.choice(["Russell Group", "UKVI Approved", "QAA", "AMBA, EQUIS", "AACS"])
        new_uni_records.append([name, "United Kingdom", random.choice(types), ranking, accreditation, f"{loc}, UK"])
        existing_names.add(name)
        
        for c in random.sample(course_templates, random.randint(3,5)):
            new_course_records.append([name, c[0], random.randint(c[1], c[2]), c[3], c[4]])
        uk_added += 1

# --- USA ---
us_states = ["California", "Texas", "New York", "Florida", "Illinois", "Pennsylvania", "Ohio", "Georgia", "North Carolina", "Michigan", "New Jersey", "Virginia", "Washington", "Arizona", "Massachusetts"]
us_cities = ["Atlanta", "Boston", "Chicago", "Dallas", "Denver", "Houston", "Los Angeles", "Miami", "New York", "Philadelphia", "Phoenix", "San Francisco", "Seattle", "Washington D.C."]
us_prefixes = ["State University", "University of", "Institute of Technology", "A&M", "Polytechnic"]

us_names = []
for s in us_states:
    for p in us_prefixes:
        if p.startswith("Univ"): us_names.append((f"{p} {s}", s))
        else: us_names.append((f"{s} {p}", s))
for c in us_cities:
    for p in us_prefixes:
        if p.startswith("Univ"): us_names.append((f"{p} {c}", c))
        else: us_names.append((f"{c} {p}", c))
random.shuffle(us_names)

us_added = 0
for name, loc in us_names:
    if us_added >= 100: break
    if name not in existing_names:
        ranking = round(random.uniform(6.5, 9.9), 1)
        accreditation = random.choice(["ABET", "AACSB", "Higher Learning Commission", "WASC", "NECHE"])
        new_uni_records.append([name, "United States", random.choice(types), ranking, accreditation, f"{loc}, USA"])
        existing_names.add(name)
        
        for c in random.sample(course_templates, random.randint(3,5)):
            new_course_records.append([name, c[0], random.randint(c[1], c[2]), c[3], c[4]])
        us_added += 1

# --- JAPAN ---
jp_cities = ["Tokyo", "Yokohama", "Osaka", "Nagoya", "Sapporo", "Fukuoka", "Kobe", "Kyoto", "Kawasaki", "Saitama", "Hiroshima", "Sendai", "Chiba", "Kitakyushu"]
jp_prefixes = ["University of", "Institute of Technology", "Imperial University", "Metropolitan University", "International", "Gakuin", "Women's University"]

jp_names = []
for c in jp_cities:
    for p in jp_prefixes:
        if p.startswith("Univ"): jp_names.append((f"{p} {c}", c))
        elif p == "Gakuin" or p == "International": jp_names.append((f"{c} {p} University", c))
        else: jp_names.append((f"{c} {p}", c))
random.shuffle(jp_names)

jp_added = 0
for name, loc in jp_names:
    if jp_added >= 100: break
    if name not in existing_names:
        uni_type = "Public" if random.random() > 0.3 else "Private"
        ranking = round(random.uniform(6.5, 9.7), 1)
        accreditation = random.choice(["MEXT Approved", "NIAD-QE", "JABEE", "AACSB", "JUAA"])
        new_uni_records.append([name, "Japan", uni_type, ranking, accreditation, f"{loc}, Japan"])
        existing_names.add(name)
        
        for c in random.sample(course_templates, random.randint(3,5)):
            new_course_records.append([name, c[0], random.randint(c[1] // 2, c[2] // 2), "MEXT/EJU", c[4]])
        jp_added += 1

# --- SINGAPORE ---
sg_prefixes = ["Singapore Institute of", "National University of", "Management University of", "Technological University of", "Global", "Polytechnic"]
sg_locations = ["Jurong", "Clementi", "Tampines", "Woodlands", "Novena", "Queenstown", "Bedok", "Punggol", "Bukit Batok", "Yishun", "Choa Chu Kang", "Sengkang", "Toa Payoh", "Pasir Ris", "Bukit Panjang", "Serangoon"]

sg_names = []
for l in sg_locations:
    for p in sg_prefixes:
        if p.endswith("of"): sg_names.append((f"{p} {l}", "Singapore"))
        else: sg_names.append((f"{l} {p} University", "Singapore"))
random.shuffle(sg_names)

sg_added = 0
for name, loc in sg_names:
    if sg_added >= 100: break
    if name not in existing_names:
        ranking = round(random.uniform(7.5, 9.9), 1)
        accreditation = random.choice(["Edutrust", "CPE Approved", "AACSB", "EQUIS", "ABET"])
        new_uni_records.append([name, "Singapore", random.choice(types), ranking, accreditation, f"{loc}, Singapore"])
        existing_names.add(name)
        
        for c in random.sample(course_templates, random.randint(3,5)):
            new_course_records.append([name, c[0], random.randint(c[1], c[2]), "Merit/A-Levels", c[4]])
        sg_added += 1

print(f"Generated UK: {uk_added}, USA: {us_added}, Japan: {jp_added}, Singapore: {sg_added}")

df_new_unis = pd.DataFrame(new_uni_records, columns=['name','location','university_type','ranking_score','accreditation','actual_location'])
df_unis_final = pd.concat([existing_unis, df_new_unis], ignore_index=True)
df_unis_final.to_csv(uni_csv, index=False)

df_new_courses = pd.DataFrame(new_course_records, columns=['university','course_name','annual_fees','admission_mode','duration'])
df_courses_final = pd.concat([existing_courses, df_new_courses], ignore_index=True)
df_courses_final.to_csv(course_csv, index=False)

print(f"Total universities now: {len(df_unis_final['name'].unique())}")
print(f"Total courses now: {len(df_courses_final)}")
