import pandas as pd
import random
import os

# Paths to CSVs
config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
uni_csv = os.path.join(config_dir, "world_universities_1000.csv")
course_csv = os.path.join(config_dir, "world_courses_5000.csv")

# Load existing
existing_unis = pd.read_csv(uni_csv)
existing_courses = pd.read_csv(course_csv)

current_unique_count = len(existing_unis['name'].unique())
needed_count = 300 - current_unique_count

print(f"Currently have {current_unique_count} universities. Need {needed_count} more.")

if needed_count <= 0:
    print("Already have 300+ universities.")
    exit()

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

cities = ["Houston", "Chicago", "Philadelphia", "Phoenix", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington", "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City", "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore", "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Mesa", "Sacramento", "Atlanta", "Kansas City", "Colorado Springs", "Miami", "Raleigh", "Omaha", "Long Beach", "Virginia Beach", "Oakland", "Minneapolis", "Tulsa", "Arlington", "Tampa", "New Orleans"]

prefixes = ["Tech", "Institute of Technology", "A&M", "Global University", "International University"]

all_potential_names = []
for s in states:
    all_potential_names.append((f"University of {s}", s))
    all_potential_names.append((f"{s} State University", s))
    all_potential_names.append((f"{s} {random.choice(prefixes)}", s))

for c in cities:
    all_potential_names.append((f"University of {c}", c))
    all_potential_names.append((f"{c} State University", c))
    all_potential_names.append((f"{c} {random.choice(prefixes)}", c))

random.shuffle(all_potential_names)

existing_names = set(existing_unis['name'].unique())
new_uni_records = []
new_course_records = []

types = ['Public', 'Private']
accreditations = ['ABET', 'AACSB', 'EQUIS', 'AMBA', 'NAAC A++', 'NAAC A+', 'Regional Accreditation', 'National Accreditation', 'WASC']
course_templates = [
    ('B.Tech Computer Science', 15000, 30000, 'Entrance Exam', '4 years'),
    ('MBA', 20000, 50000, 'GMAT/GRE/Entrance', '2 years'),
    ('B.Sc Physics', 8000, 18000, 'Merit Based', '3 or 4 years'),
    ('BBA', 10000, 25000, 'Merit Based', '3 or 4 years'),
    ('M.Sc Data Science', 12000, 35000, 'Entrance/GRE', '2 years'),
    ('B.A. Economics', 9000, 22000, 'Merit Based', '3 or 4 years'),
    ('MS Artificial Intelligence', 14000, 32000, 'Entrance Exam', '2 years'),
    ('MD / Medical Degree', 30000, 70000, 'MCAT/Equivalent', '5+ years')
]

added_count = 0
for name, loc in all_potential_names:
    if added_count >= needed_count:
        break
        
    country = "United States"
    
    if name not in existing_names:
        uni_type = random.choice(types)
        ranking = round(random.uniform(5.0, 9.9), 1)
        accreditation = random.choice(accreditations)
        if random.random() > 0.5:
            accreditation += f", {random.choice(accreditations)}"
            
        actual_location = f"{loc}, USA"
             
        new_uni_records.append([
            name,
            country,
            uni_type,
            ranking,
            accreditation,
            actual_location
        ])
        existing_names.add(name)
        
        num_courses = random.randint(3, 5)
        selected_courses = random.sample(course_templates, num_courses)
        for c in selected_courses:
            course_name = c[0]
            fees = random.randint(c[1], c[2])
            admission_mode = c[3]
            duration = c[4]
            new_course_records.append([
                name,
                course_name,
                fees,
                admission_mode,
                duration
            ])
            
        added_count += 1

print(f"Generated data for {added_count} new universities.")

df_new_unis = pd.DataFrame(new_uni_records, columns=['name','location','university_type','ranking_score','accreditation','actual_location'])
df_unis_final = pd.concat([existing_unis, df_new_unis], ignore_index=True)
df_unis_final.to_csv(uni_csv, index=False)

df_new_courses = pd.DataFrame(new_course_records, columns=['university','course_name','annual_fees','admission_mode','duration'])
df_courses_final = pd.concat([existing_courses, df_new_courses], ignore_index=True)
df_courses_final.to_csv(course_csv, index=False)

print(f"Total universities now in CSV: {len(df_unis_final['name'].unique())}")
print(f"Total courses now in CSV: {len(df_courses_final)}")
