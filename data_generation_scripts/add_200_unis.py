import pandas as pd
import random
import os

# Paths to CSVs
config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
uni_csv = os.path.join(config_dir, "world_universities_1000.csv")
course_csv = os.path.join(config_dir, "world_courses_5000.csv")

existing_unis = pd.read_csv(uni_csv)
existing_courses = pd.read_csv(course_csv)

indian_states = ["Maharashtra", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "Gujarat", "Kerala", "Rajasthan", "Madhya Pradesh", "West Bengal", "Punjab", "Haryana", "Telangana", "Andhra Pradesh", "Bihar", "Odisha"]
indian_cities = ["Mumbai", "Pune", "Bangalore", "Chennai", "Delhi", "Ahmedabad", "Surat", "Jaipur", "Kochi", "Lucknow", "Nagpur", "Indore", "Bhopal", "Patna", "Kolkata", "Hyderabad", "Chandigarh"]

german_states = ["Bavaria", "Baden-Württemberg", "North Rhine-Westphalia", "Hesse", "Saxony", "Lower Saxony", "Rhineland-Palatinate", "Berlin", "Hamburg", "Thuringia"]
german_cities = ["Munich", "Berlin", "Hamburg", "Frankfurt", "Stuttgart", "Cologne", "Düsseldorf", "Leipzig", "Dresden", "Hannover", "Nuremberg", "Bremen", "Bonn", "Münster", "Karlsruhe", "Aachen", "Heidelberg"]

india_prefixes = ["Institute of Technology", "National Institute", "University", "Vidyapeeth", "Academy", "Engineering College", "Institute of Management", "School of Computing", "Institute of Advanced Studies", "Polytechnic Institute"]
germany_prefixes = ["Technical University of", "University of Applied Sciences", "University of", "Institute of Technology", "Hochschule", "Fachhochschule", "International University"]

india_names = []
for s in indian_states:
    for p in india_prefixes:
        india_names.append((f"{s} {p}", s))
for c in indian_cities:
    for p in india_prefixes:
        india_names.append((f"{p} {c}", c))
    india_names.append((f"{c} State University", c))
random.shuffle(india_names)

germany_names = []
for s in german_states:
    for p in germany_prefixes:
        germany_names.append((f"{p} {s}", s))
for c in german_cities:
    for p in germany_prefixes:
        germany_names.append((f"{p} {c}", c))
    germany_names.append((f"Hochschule {c}", c))
random.shuffle(germany_names)

existing_names = set(existing_unis['name'].unique())
new_uni_records = []
new_course_records = []

types = ['Public', 'Private']
india_accreditations = ['NAAC A++', 'NAAC A+', 'UGC Approved', 'AICTE Approved', 'NBA Accredited']
germany_accreditations = ['Wissenschaftsrat', 'FIBAA', 'ASIIN', 'AQAS', 'State Accredited']

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

# Generate 100 India
added_india = 0
for name, loc in india_names:
    if added_india >= 100: break
    if name not in existing_names:
        uni_type = random.choice(types)
        ranking = round(random.uniform(6.0, 9.5), 1)
        accreditation = random.choice(india_accreditations)
        if random.random() > 0.5: accreditation += f", {random.choice(india_accreditations)}"
        actual_location = f"{loc}, India"
        new_uni_records.append([name, "India", uni_type, ranking, accreditation, actual_location])
        existing_names.add(name)
        
        num_courses = random.randint(3, 5)
        for c in random.sample(course_templates_india, num_courses):
            new_course_records.append([name, c[0], random.randint(c[1], c[2]), c[3], c[4]])
        added_india += 1

# Generate 100 Germany
added_germany = 0
for name, loc in germany_names:
    if added_germany >= 100: break
    if name not in existing_names:
        uni_type = "Public" if random.random() > 0.2 else "Private"  # Germany is mostly public
        ranking = round(random.uniform(7.0, 9.8), 1)
        accreditation = random.choice(germany_accreditations)
        actual_location = f"{loc}, Germany"
        new_uni_records.append([name, "Germany", uni_type, ranking, accreditation, actual_location])
        existing_names.add(name)
        
        num_courses = random.randint(3, 5)
        for c in random.sample(course_templates_germany, num_courses):
            fees = random.randint(c[1], c[2]) if uni_type == "Private" else random.choice([0, 500, 1500]) # Public is almost free
            new_course_records.append([name, c[0], fees, c[3], c[4]])
        added_germany += 1

print(f"Generated {added_india} India and {added_germany} Germany universities.")

df_new_unis = pd.DataFrame(new_uni_records, columns=['name','location','university_type','ranking_score','accreditation','actual_location'])
df_unis_final = pd.concat([existing_unis, df_new_unis], ignore_index=True)
df_unis_final.to_csv(uni_csv, index=False)

df_new_courses = pd.DataFrame(new_course_records, columns=['university','course_name','annual_fees','admission_mode','duration'])
df_courses_final = pd.concat([existing_courses, df_new_courses], ignore_index=True)
df_courses_final.to_csv(course_csv, index=False)

print(f"Total universities now: {len(df_unis_final['name'].unique())}")
print(f"Total courses now: {len(df_courses_final)}")
