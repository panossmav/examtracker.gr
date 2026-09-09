# ExamTracker

A desktop app for Greek tutoring schools (φροντιστήρια). A teacher logs in, then tracks student exam marks and tuition payments from a single Tkinter window. The interface is entirely in Greek.

## Stack

- **Python 3** with **Tkinter/ttk** for the GUI
- **PostgreSQL** via `psycopg2` for storage
- **python-dotenv** for reading the database connection string from a `.env` file

No web server, no ORM. `app.py` calls straight into `db_comms.py`, which runs raw SQL against five tables.

## Features

The sidebar has four sections:

- **Στατιστικά (Statistics)**: search a student and pull their overall average, their average in one subject, or a table of every mark they've logged for a subject.
- **Καταχώρηση (Exam entry)**: log a mock exam with student name, subject, date, and mark.
- **Πληρωμές (Payments)**: log a tuition payment and look up a student's balance. The balance comes from `monthly_fee × months_since_enrollment − total_paid`. The app looks up the monthly fee by the student's class in the `grade` table and counts months from the enrollment date to the current month. A payment history table sits below the search.
- **Νέος Μαθητής (New student)**: register a student with name, age, class, and enrollment date.

Login checks a username/password pair against the `users` table. Passwords are hashed client-side with SHA-256 before the query runs; there's no salting or hashing on the server side beyond that.

## Project layout

```
examtracker.gr/
├── app.py                     # Tkinter GUI: login, navigation, all four pages
├── db_comms.py                # DB layer: Student, mock_exam, payment, Backend_user
├── requirements.txt
├── setup/
│   ├── .env.example           # Template for DATABASE_URL
│   └── initial_commands.sql   # Creates the five tables
├── demo_app/
│   ├── app_demo.py            # Same GUI, imports db_comms_demo instead of db_comms
│   └── db_comms_demo.py       # In-memory backend, no database required
├── images/                    # Logo
└── info/                      # Design scratch files (isolated GUI prototype, drawio diagram)
```

## Database

Five tables, created by `setup/initial_commands.sql`:

| Table | Purpose |
|---|---|
| `students` | name, date-of-birth field (repurposed to store age; see note below), class, enrollment date |
| `exams` | one row per mock exam mark: student, subject, date, mark |
| `payments` | one row per tuition payment: student, amount, date |
| `grade` | one row per class name, holding its monthly fee and an active flag |
| `users` | login credentials |

Everything is keyed on student name (uppercased on write and on lookup) rather than a foreign key to `students.id`. There's no seed data for `grade` in `initial_commands.sql`, so a fresh database needs rows added there before balances can resolve.

One deliberate schema shortcut: the `students.dob` column is `NOT NULL` but the UI has no date-of-birth field, so `Student.save()` writes the student's age into it as a string instead.

## Running it

### With a real database

1. `pip install -r requirements.txt`
2. Create a PostgreSQL database and run `setup/initial_commands.sql` against it.
3. Copy `setup/.env.example` to `.env` and set `DATABASE_URL` to your connection string.
4. Add at least one row to `users` (with a SHA-256 password hash) and one row per class to `grade`.
5. `python app.py`

### Demo mode, no database

```
python demo_app/app_demo.py
```

Login with `demo` / `demo123`. `db_comms_demo.py` swaps every SQL call for lookups against in-memory Python dicts and lists, pre-populated with three sample students, some exam marks, payments, and per-class fees. Nothing persists between runs.

## Notes on `info/`

`info/isolated_gui.py` strips things down further: same visual layout as `app.py`, but every button handler returns a canned status message. It has no `db_comms` import, no real or fake data store, nothing wired up. It reads as a UI-only prototype kept for reference. `class_view.drawio` diagrams the class structure. `error_codes.md` and `setup.md` sit empty.
