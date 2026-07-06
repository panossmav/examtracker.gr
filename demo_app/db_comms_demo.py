from datetime import date as _date
import hashlib as _hl

# ── In-memory demo data store (no DB / .env required) ──────────────────────────
# Demo login: username "demo" / password "demo123"

_users = {
    "demo": _hl.sha256("demo123".encode()).hexdigest(),
}

_students = {
    # name -> {age, grade, enroll_date}
    "Γιώργος Παπαδόπουλος": {"age": 16, "grade": "Β Λυκείου", "enroll_date": "2026-01-10"},
    "Μαρία Νικολάου":       {"age": 17, "grade": "Γ Λυκείου", "enroll_date": "2025-09-15"},
    "Ελένη Κωνσταντίνου":   {"age": 15, "grade": "Α Λυκείου", "enroll_date": "2026-02-01"},
}

_exams = [
    # (s_name, c_date, subj, mark)
    ("Γιώργος Παπαδόπουλος", "2026-02-10", "Μαθηματικά", 17.5),
    ("Γιώργος Παπαδόπουλος", "2026-03-14", "Μαθηματικά", 15.0),
    ("Γιώργος Παπαδόπουλος", "2026-02-20", "Φυσική",     14.0),
    ("Μαρία Νικολάου",       "2026-01-05", "Έκθεση",     18.0),
    ("Μαρία Νικολάου",       "2026-02-05", "Έκθεση",     16.5),
    ("Ελένη Κωνσταντίνου",   "2026-03-01", "Χημεία",     12.5),
]

_payments = [
    # (s_name, c_date, amount)
    ("Γιώργος Παπαδόπουλος", "2026-01-15", 80.0),
    ("Γιώργος Παπαδόπουλος", "2026-02-15", 80.0),
    ("Μαρία Νικολάου",       "2025-10-01", 100.0),
]

_grade_fees = {
    # c_name -> monthly fee
    "Α Λυκείου": 60.0,
    "Β Λυκείου": 70.0,
    "Γ Λυκείου": 80.0,
}


def _months_elapsed(enroll_date_str):
    try:
        y, m, _d = [int(p) for p in enroll_date_str.split("-")]
        today = _date.today()
        return (today.year - y) * 12 + (today.month - m) + 1
    except Exception as e:
        print(f"Error in _months_elapsed: {e}")
        return -1


class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def get_avg_subj(self, subject):
        marks = [m for (n, _d, s, m) in _exams if n == self.name and s == subject]
        if not marks:
            return -1
        return round(sum(marks) / len(marks), 2)

    def get_avg(self):
        marks = [m for (n, _d, _s, m) in _exams if n == self.name]
        if not marks:
            return -1
        return round(sum(marks) / len(marks), 2)

    def list_grades(self, subject):
        return [m for (n, _d, s, m) in _exams if n == self.name and s == subject]

    def save(self, c_name, enroll_date):
        _students[self.name] = {"age": self.age, "grade": c_name, "enroll_date": enroll_date}
        print("Η εγγραφή του μαθητή έγινε επιτυχώς! (demo)")

    def get_total_paid(self):
        paid = [a for (n, _d, a) in _payments if n == self.name]
        return round(sum(paid), 2) if paid else 0

    def list_payments(self):
        return [(d, a) for (n, d, a) in _payments if n == self.name]

    def get_balance(self):
        info = _students.get(self.name)
        if not info or not info.get("grade") or not info.get("enroll_date"):
            return (-1, -1, -1)
        c_name = info["grade"]
        enroll_date = info["enroll_date"]

        monthly_fee = _grade_fees.get(c_name)
        if monthly_fee is None:
            return (-1, -1, -1)

        months = _months_elapsed(enroll_date)
        if months < 1:
            months = 1

        expected_total = round(monthly_fee * months, 2)
        paid = self.get_total_paid()
        balance = round(expected_total - paid, 2)
        return (expected_total, paid, balance)


class mock_exam:
    def __init__(self, s_name, date, subject, mark):
        self.s_name = s_name
        self.date = date
        self.subject = subject
        self.mark = mark

    def log_exam(self):
        _exams.append((self.s_name, self.date, self.subject, self.mark))
        print("Η εγγραφή της εξέτασης έγινε επιτυχώς! (demo)")


class payment:
    def __init__(self, s_name, date, amount):
        self.s_name = s_name
        self.date = date
        self.amount = amount

    def log_payment(self):
        _payments.append((self.s_name, self.date, self.amount))
        print("Η καταχώρηση της πληρωμής έγινε επιτυχώς! (demo)")


class Grade:
    def __init__(self, name):
        self.name = name


class Backend_user:
    def __init__(self, username, pwd, user_type):
        self.username = username
        self.pwd = pwd
        self.user_type = user_type

    def log_in(self):
        # self.pwd φτάνει ήδη hashed (sha256) από το app, όπως και στο κανονικό backend.
        if _users.get(self.username) == self.pwd:
            return ("Εκπαιδευτικός (Demo)",)
        print("Login failed: Λάθος username ή password. (demo: χρησιμοποίησε demo/demo123)")
        return None
