import datetime
import random


class TestData:

    JOB_TITLES = [
        "Software Engineer", "QA Engineer", "Backend Developer",
        "Frontend Developer", "DevOps Engineer", "Data Analyst",
        "Project Manager", "Automation Tester", "Cloud Engineer", "Business Analyst"
    ]

    SKILLS = [
        "Python", "Java", "Selenium", "SQL", "React",
        "AWS", "Docker", "Kubernetes", "API Testing", "Jenkins"
    ]

    WORDS = [
        "development", "testing", "automation", "design", "analysis",
        "integration", "deployment", "scalability", "performance", "security"
    ]

    @staticmethod
    def get_unique_job_title():
        return f"{random.choice(TestData.JOB_TITLES)}_{datetime.datetime.now().strftime('%d%m%y_%H%M%S')}"

    @staticmethod
    def get_rate(min_val=106, max_val=150):
        return str(random.randint(min_val, max_val))

    @staticmethod
    def get_skills(count=3):
        return ", ".join(random.sample(TestData.SKILLS, count))

    @staticmethod
    def get_duration(min_val=6, max_val=12):
        return str(random.randint(min_val, max_val))

    @staticmethod
    def get_positions(min_val=1, max_val=2):
        return str(random.randint(min_val, max_val))

    @staticmethod
    def get_description(max_chars=250):
        text = " ".join(random.choices(TestData.WORDS, k=40))
        return text[:max_chars]

    JOB_TERMS = ["Contract", "Contract-to-Hire", "Permanent"]

    @staticmethod
    def generate_requirement_data():
        job_term = random.choice(TestData.JOB_TERMS)
        data = {
            "job_title": TestData.get_unique_job_title(),
            "job_term": job_term,
            "rate": TestData.get_rate(),
            "skills": TestData.get_skills(),
            "positions": TestData.get_positions(),
            "job_description": TestData.get_description(),
            "additional_info": TestData.get_description(180),
        }
        if job_term in ("Contract", "Contract-to-Hire"):
            data["duration"] = TestData.get_duration()
        return data