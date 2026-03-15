from django.db import models

class University(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=100, db_index=True)   # country
    actual_location = models.CharField(max_length=300, blank=True, null=True)  # full address
    university_type = models.CharField(max_length=50)
    accreditation = models.CharField(max_length=100)
    ranking_score = models.FloatField(db_index=True)

    def __str__(self):
        return self.name



class Course(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        db_index=True
    )
    course_name = models.CharField(max_length=100, db_index=True)
    annual_fees = models.IntegerField(db_index=True)
    admission_mode = models.CharField(max_length=50)
    duration = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.course_name} - {self.university.name}"


class UniversityPolicy(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        db_index=True
    )
    policy_type = models.CharField(max_length=100, db_index=True)
    policy_title = models.CharField(max_length=200)
    policy_description = models.TextField()
    effective_year = models.IntegerField(db_index=True)

    def __str__(self):
        return f"{self.policy_type} - {self.university.name}"

