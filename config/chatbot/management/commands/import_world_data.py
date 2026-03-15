from django.core.management.base import BaseCommand
from chatbot.models import University, Course, UniversityPolicy
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Map abbreviated/alternate names used in courses CSV → full names in universities CSV
UNIVERSITY_ALIASES = {
    "IIT Bombay":  "Indian Institute of Technology Bombay",
    "IIT Delhi":   "Indian Institute of Technology Delhi",
    "IIT Madras":  "Indian Institute of Technology Madras",
    "IIT Kanpur":  "Indian Institute of Technology Kanpur",
    "IIT Kharagpur": "Indian Institute of Technology Kharagpur",
    "IIT Roorkee": "Indian Institute of Technology Roorkee",
    "Anna University": "Anna University",
}

class Command(BaseCommand):
    help = "Import worldwide university data"

    def handle(self, *args, **kwargs):
        self.import_universities()
        self.import_courses()
        self.import_policies()
        self.stdout.write(self.style.SUCCESS("✅ World data imported successfully"))

    def import_universities(self):
        with open(os.path.join(BASE_DIR, "world_universities_1000.csv"), encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                University.objects.get_or_create(
                    name=row["name"],
                    defaults={
                        "location": row["location"],
                        "actual_location": row.get("actual_location", row["location"]),
                        "university_type": row["university_type"],
                        "accreditation": row["accreditation"],
                        "ranking_score": float(row["ranking_score"])
                    }
                )
        self.stdout.write("✔ Universities imported")

    def _resolve_university_name(self, name):
        """Return the canonical university name, applying alias mapping if needed."""
        return UNIVERSITY_ALIASES.get(name, name)

    def import_courses(self):
        with open(os.path.join(BASE_DIR, "world_courses_5000.csv"), encoding="utf-8") as file:
            reader = csv.DictReader(file)
            skipped = 0

            for row in reader:
                try:
                    canonical_name = self._resolve_university_name(row["university"])
                    university = University.objects.get(name=canonical_name)
                    Course.objects.create(
                        university=university,
                        course_name=row["course_name"],
                        annual_fees=int(row["annual_fees"]),
                        admission_mode=row["admission_mode"],
                        duration=row["duration"]
                    )
                except University.DoesNotExist:
                    skipped += 1

        self.stdout.write(f"✔ Courses imported (skipped {skipped} unmatched)")

    def import_policies(self):
        with open(os.path.join(BASE_DIR, "world_policies_3000.csv"), encoding="utf-8") as file:
            reader = csv.DictReader(file)
            skipped = 0

            for row in reader:
                try:
                    canonical_name = self._resolve_university_name(row["university"])
                    university = University.objects.get(name=canonical_name)
                    UniversityPolicy.objects.create(
                        university=university,
                        policy_type=row["policy_type"],
                        policy_title=row["policy_title"],
                        policy_description=row["policy_explanation"],
                        effective_year=int(row["effective_year"])
                    )
                except University.DoesNotExist:
                    skipped += 1

        self.stdout.write(f"✔ Policies imported (skipped {skipped} unmatched)")
