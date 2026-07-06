# ExamTracker

ExamTracker is a small desktop app for tutoring schools (φροντιστήρια) that keeps track of two things every small institution cares about: how students are doing on their mock exams, and whether their tuition is paid up. It is built with a Tkinter front end and a plain-Python object-oriented back end, talking to a local PostgreSQL database. The interface is in Greek, since that is who the app is for.

There is no server, no cloud account, no sync. Each client runs their own copy against their own local database, configured through a `.env` file that stays on their machine.

## What it does

Once you log in, the app opens on a sidebar with four sections:

- **Statistics (Στατιστικά)** — look up a student and get their overall grade average, their average in a specific subject, or a full table of their recorded marks.
- **Exam entry (Καταχώρηση)** — record a mock exam result: student, subject, date, and mark.
- **Payments (Πληρωμές)** — record tuition payments, and check a student's balance. The balance is calculated from the monthly fee of the student's class and the number of months since enrollment, minus everything they have paid so far. A payment history table is shown alongside.
- **New student (Νέος Μαθητής)** — register a student with their name, age, class, and enrollment date.

## Project layout

```
examtracker.gr/
├── app.py                     # Tkinter GUI (login, navigation, all four pages)
├── db_comms.py                # Database layer: Student, mock_exam, payment, Backend_user
├── requirements.txt
├── setup/
│   ├── .env.example           # Template for your database connection string
│   └── initial_commands.sql   # Creates the five tables the app needs
├── demo_app/
│   ├── app_demo.py            # Same GUI, wired to an in-memory data store
│   └── db_comms_demo.py       # Fake backend with sample Greek students — no DB needed
├── images/                    # Logo
└── info/                      # Design notes and scratch files
```

## Requirements

- Python 3.10 or newer (the code uses modern type-hint syntax like `dict | None`)
- PostgreSQL running locally
- Two Python packages: `python-dotenv` and `psycopg2-binary`

## Trying it out first (demo mode)

If you just want to see the app without setting up a database, the demo version runs entirely in memory with a few sample students already loaded:

```bash
cd demo_app
python app_demo.py
```

Log in with username `demo` and password `demo123`. Anything you add lives only until you close the window.

## Setting up the real thing

1. **Install the dependencies.**

   ```bash
   pip install -r requirements.txt
   ```

2. **Create a PostgreSQL database** and run the schema script against it:

   ```bash
   psql -d your_database -f setup/initial_commands.sql
   ```

   This creates five tables: `students`, `exams`, `payments`, `grade` (one row per class, holding its monthly fee), and `users` (app logins).

3. **Configure the connection.** Copy the example env file into the project root and fill in your connection string:

   ```bash
   cp setup/.env.example .env
   ```

   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/your_database
   ```

   The `.env` file is git-ignored on purpose — every client gets their own.

4. **Create at least one login.** Passwords are stored as SHA-256 hashes, and the app hashes what you type before checking it, so the value in the database must be the hash, not the plain password. For example, to create a user `admin` with password `mypassword`:

   ```sql
   INSERT INTO users (username, pwd)
   VALUES ('admin', encode(sha256('mypassword'::bytea), 'hex'));
   ```

5. **Add your classes to the `grade` table** so balance calculations work. Each row is a class name and its monthly fee:

   ```sql
   INSERT INTO grade (c_name, is_active, student_amount)
   VALUES ('Β Λυκείου', 1, 120);
   ```

   The class name here must match what you type in the "ΤΑΞΗ / ΤΜΗΜΑ" field when registering a student — that is how the app finds the fee.

6. **Run it.**

   ```bash
   python app.py
   ```

## How balances are calculated

When you ask for a student's balance, the app looks up their class and enrollment date, finds the class's monthly fee in the `grade` table, and counts the months from enrollment through the current month (the enrollment month counts as month one). Expected total is fee times months; the balance is that minus the sum of recorded payments. If the student has no class, no enrollment date, or their class is missing from `grade`, the app tells you it cannot compute a balance rather than guessing.

## A few honest notes

- Students are matched by name across tables, so names need to be typed consistently. Two students with the same name will get mixed together.
- Dates are stored as text in `YYYY-MM-DD` format; the forms pre-fill today's date, but nothing stops a typo.
- There is currently one user role — everyone who logs in sees the same four pages.
- Upgrading an older database that predates the payments feature? The comments at the top of `setup/initial_commands.sql` list the `ALTER TABLE` statements to run.

## Updating existing installations

Since each client has their own local database, schema changes have to be applied manually per installation. Keep an eye on `setup/initial_commands.sql` — migration notes live there as SQL comments.
