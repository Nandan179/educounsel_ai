import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Resolve paths relative to the config/ directory (where the CSV files live)
_CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")

# Load CSV datasets
universities = pd.read_csv(os.path.join(_CONFIG_DIR, "world_universities_1000.csv"))
courses      = pd.read_csv(os.path.join(_CONFIG_DIR, "world_courses_5000.csv"))

# Merge datasets
data = courses.merge(
    universities,
    left_on="university",
    right_on="name"
)

# Feature Engineering
le_country = LabelEncoder()
le_type = LabelEncoder()
le_course = LabelEncoder()

data["country_encoded"] = le_country.fit_transform(data["location"])
data["type_encoded"] = le_type.fit_transform(data["university_type"])
data["course_encoded"] = le_course.fit_transform(data["course_name"])

# Create synthetic suitability score
data["suitability_score"] = (
    data["ranking_score"] * 0.5
    - (data["annual_fees"] / 100000) * 0.3
    + 10
)

# Features
X = data[[
    "ranking_score",
    "annual_fees",
    "country_encoded",
    "type_encoded",
    "course_encoded"
]]

y = data["suitability_score"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model + encoders
joblib.dump(model, "rf_model.pkl")
joblib.dump(le_country, "le_country.pkl")
joblib.dump(le_type, "le_type.pkl")
joblib.dump(le_course, "le_course.pkl")

print("Model trained and saved successfully.")