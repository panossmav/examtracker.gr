
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import hashlib as hl
import db_comms as db

# ── Palette (Catppuccin Mocha) ─────────────────────────────────────────────────
BG      = "#1e1e2e"
SURFACE = "#313244"
OVERLAY = "#45475a"
ACCENT  = "#89b4fa"
TEXT    = "#cdd6f4"
MUTED   = "#6c7086"
GREEN   = "#a6e3a1"
RED     = "#f38ba8"
YELLOW  = "#f9e2af"

FONT_SM = ("Segoe UI", 10)
FONT_MD = ("Segoe UI", 12)
FONT_LG = ("Segoe UI", 14, "bold")
FONT_XL = ("Segoe UI", 20, "bold")


# ── Widget helpers ─────────────────────────────────────────────────────────────
def _entry(parent, **kwargs):
    return tk.Entry(
        parent, font=FONT_MD, bg=SURFACE, fg=TEXT,
        insertbackground=TEXT, relief="flat",
        highlightthickness=1, highlightbackground=OVERLAY,
        highlightcolor=ACCENT, **kwargs,
    )


def _btn(parent, text, cmd, color=ACCENT, **kwargs):
    return tk.Button(
        parent, text=text, command=cmd,
        font=("Segoe UI", 11, "bold"),
        bg=color, fg=BG, activebackground=color, activeforeground=BG,
        relief="flat", cursor="hand2", **kwargs,
    )


# ══════════════════════════════════════════════════════════════════════════════
class ExamTracker(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("ExamTracker")
        self.geometry("920x580")
        self.minsize(920, 580)
        self.configure(bg=BG)
        self.current_user: dict | None = None
        self._build_ttk_style()
        self._show_login()

    # ── TTK style ──────────────────────────────────────────────────────────────
    def _build_ttk_style(self):
        s = ttk.Style(self)
        s.theme_use("default")
        s.configure("Treeview",
                    background=SURFACE, foreground=TEXT,
                    fieldbackground=SURFACE, rowheight=28,
                    font=FONT_MD, borderwidth=0)
        s.configure("Treeview.Heading",
                    background=OVERLAY, foreground=ACCENT,
                    font=("Segoe UI", 11, "bold"), relief="flat")
        s.map("Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", BG)])

    # ── Helpers ────────────────────────────────────────────────────────────────
    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ══════════════════════════════════════════════════════════════════════════
    # ΣΥΝΔΕΣΗ
    # ══════════════════════════════════════════════════════════════════════════
    def _show_login(self):
        self._clear()
        wrap = tk.Frame(self, bg=BG)
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(wrap, text="ExamTracker", font=FONT_XL,
                 bg=BG, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(wrap, text="Σύνδεση για συνέχεια", font=FONT_SM,
                 bg=BG, fg=MUTED).pack(pady=(0, 26))

        self._login_fields: dict[str, tk.Entry] = {}
        for lbl_txt, key, show in [
            ("Όνομα χρήστη", "username", ""),
            ("Κωδικός",      "password", "•"),
        ]:
            tk.Label(wrap, text=lbl_txt, font=FONT_SM,
                     bg=BG, fg=MUTED, anchor="w").pack(fill="x")
            e = _entry(wrap, width=30, show=show)
            e.pack(pady=(3, 14), ipady=7)
            self._login_fields[key] = e

        self._login_err = tk.Label(wrap, text="", font=FONT_SM,
                                   bg=BG, fg=RED)
        self._login_err.pack(pady=(0, 6))

        _btn(wrap, "Σύνδεση", self._do_login, width=22).pack(ipady=8)
        self._login_fields["password"].bind("<Return>", lambda _: self._do_login())

    def _do_login(self):
        username = self._login_fields["username"].get().strip()
        pwd      = self._login_fields["password"].get().strip()

        if not username or not pwd:
            self._login_err.config(text="Συμπλήρωσε και τα δύο πεδία.")
            return

        hashed = hl.sha256(pwd.encode()).hexdigest()
        result = db.Backend_user(username, hashed, None).log_in()

        if not result or result == "Error!":
            self._login_err.config(text="Λάθος στοιχεία σύνδεσης.")
        else:
            self.current_user = {"username": username, "type": result[0]}
            self._show_main()

    # ══════════════════════════════════════════════════════════════════════════
    # ΚΥΡΙΟ ΠΑΡΑΘΥΡΟ
    # ══════════════════════════════════════════════════════════════════════════
    def _show_main(self):
        self._clear()

        # ── Top bar ────────────────────────────────────────────────────────────
        top = tk.Frame(self, bg=SURFACE, height=48)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="ExamTracker", font=FONT_LG,
                 bg=SURFACE, fg=ACCENT).pack(side="left", padx=16)
        tk.Label(top,
                 text=f"  {self.current_user['username']}  ·  {self.current_user['type']}",
                 font=FONT_SM, bg=SURFACE, fg=MUTED).pack(side="left")
        _btn(top, "Αποσύνδεση", self._show_login, color=RED
             ).pack(side="right", padx=12, pady=8)

        # ── Body ───────────────────────────────────────────────────────────────
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        sidebar = tk.Frame(body, bg=SURFACE, width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        self.content = tk.Frame(body, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

        # Sidebar nav
        nav = [
            ("📊  Στατιστικά",     self._page_stats),
            ("📝  Καταχώρηση",     self._page_log_exam),
            ("👤  Νέος Μαθητής",   self._page_add_student),
        ]
        tk.Frame(sidebar, bg=OVERLAY, height=1).pack(fill="x", pady=(8, 0))
        for text, cmd in nav:
            tk.Button(
                sidebar, text=text, font=("Segoe UI", 11),
                bg=SURFACE, fg=TEXT, activebackground=BG,
                activeforeground=ACCENT, relief="flat",
                anchor="w", cursor="hand2", command=cmd,
            ).pack(fill="x", padx=6, pady=2, ipady=12)

        self._page_stats()

    # ══════════════════════════════════════════════════════════════════════════
    # ΣΕΛΙΔΑ: ΣΤΑΤΙΣΤΙΚΑ
    # ══════════════════════════════════════════════════════════════════════════
    def _page_stats(self):
        self._clear_content()
        f = self.content

        tk.Label(f, text="Στατιστικά", font=FONT_XL,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=24, pady=(20, 14))

        # Input row
        inp = tk.Frame(f, bg=BG)
        inp.pack(anchor="w", padx=24)

        tk.Label(inp, text="Όνομα μαθητή", font=FONT_SM,
                 bg=BG, fg=MUTED).grid(row=0, column=0, sticky="w")
        self._s_name = _entry(inp, width=22)
        self._s_name.grid(row=1, column=0, padx=(0, 14), ipady=6)

        tk.Label(inp, text="Μάθημα", font=FONT_SM,
                 bg=BG, fg=MUTED).grid(row=0, column=1, sticky="w")
        self._s_subj = _entry(inp, width=18)
        self._s_subj.grid(row=1, column=1, ipady=6)

        # Action buttons
        btn_row = tk.Frame(f, bg=BG)
        btn_row.pack(anchor="w", padx=24, pady=12)
        for text, cmd in [
            ("Γεν. Μ.Ο.",       self._stat_overall),
            ("Μ.Ο. Μαθήματος",  self._stat_subject),
            ("Βαθμοί",          self._stat_grades),
        ]:
            _btn(btn_row, text, cmd).pack(side="left",
                                          padx=(0, 8), ipady=6, ipadx=10)

        # Result label
        self._stat_result = tk.Label(f, text="", font=("Segoe UI", 13),
                                     bg=BG, fg=GREEN)
        self._stat_result.pack(anchor="w", padx=24, pady=(0, 8))

        # Treeview
        tree_wrap = tk.Frame(f, bg=BG)
        tree_wrap.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self._tree = ttk.Treeview(
            tree_wrap,
            columns=("Μαθητής", "Μάθημα", "Βαθμός"),
            show="headings", height=10,
        )
        for col, w in [("Μαθητής", 220), ("Μάθημα", 220), ("Βαθμός", 100)]:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, anchor="center")

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical",
                             command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    def _stat_overall(self):
        name = self._s_name.get().strip()
        if not name:
            messagebox.showerror("Απαιτείται είσοδος", "Εισάγαγε όνομα μαθητή.")
            return
        avg = db.Student(name, None, None).get_avg()
        if avg == -1:
            self._stat_result.config(text="Δεν βρέθηκαν εγγραφές.", fg=YELLOW)
        else:
            self._stat_result.config(
                text=f"Γενικός μ.ο. για {name}: {avg}", fg=GREEN)

    def _stat_subject(self):
        name = self._s_name.get().strip()
        subj = self._s_subj.get().strip()
        if not name or not subj:
            messagebox.showerror("Απαιτείται είσοδος",
                                 "Εισάγαγε όνομα μαθητή και μάθημα.")
            return
        avg = db.Student(name, None, None).get_avg_subj(subj)
        if avg == -1:
            self._stat_result.config(text="Δεν βρέθηκαν εγγραφές.", fg=YELLOW)
        else:
            self._stat_result.config(
                text=f"Μ.ο. {subj} για {name}: {avg}", fg=GREEN)

    def _stat_grades(self):
        name = self._s_name.get().strip()
        subj = self._s_subj.get().strip()
        if not name or not subj:
            messagebox.showerror("Απαιτείται είσοδος",
                                 "Εισάγαγε όνομα μαθητή και μάθημα.")
            return
        self._tree.delete(*self._tree.get_children())
        grades = db.Student(name, None, None).list_grades(subj)
        for g in grades:
            self._tree.insert("", "end", values=(name, subj, g))
        count = len(grades)
        self._stat_result.config(
            text=f"Εμφάνιση {count} βαθμ. για {name} / {subj}",
            fg=MUTED if count else YELLOW,
        )

    # ══════════════════════════════════════════════════════════════════════════
    # ΣΕΛΙΔΑ: ΚΑΤΑΧΩΡΗΣΗ ΕΞΕΤΑΣΗΣ
    # ══════════════════════════════════════════════════════════════════════════
    def _page_log_exam(self):
        self._clear_content()
        f = self.content

        tk.Label(f, text="Καταχώρηση Εξέτασης", font=FONT_XL,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=24, pady=(20, 16))

        form = tk.Frame(f, bg=BG)
        form.pack(anchor="w", padx=24)

        fields = [
            ("Όνομα μαθητή",          "le_name", ""),
            ("Ημερομηνία (ΕΕΕΕ-ΜΜ-ΗΗ)", "le_date", str(date.today())),
            ("Μάθημα",                "le_subj", ""),
            ("Βαθμός",                "le_mark", ""),
        ]

        self._le: dict[str, tk.Entry] = {}
        for i, (lbl_txt, key, default) in enumerate(fields):
            tk.Label(form, text=lbl_txt, font=FONT_SM,
                     bg=BG, fg=MUTED).grid(row=i * 2, column=0,
                                            sticky="w", pady=(10, 2))
            e = _entry(form, width=30)
            e.grid(row=i * 2 + 1, column=0, sticky="w", ipady=7)
            if default:
                e.insert(0, default)
            self._le[key] = e

        self._le_status = tk.Label(f, text="", font=FONT_SM, bg=BG, fg=GREEN)
        self._le_status.pack(anchor="w", padx=24, pady=10)

        _btn(f, "Καταχώρηση", self._do_log_exam).pack(
            anchor="w", padx=24, ipady=8, ipadx=20)

    def _do_log_exam(self):
        vals = {k: v.get().strip() for k, v in self._le.items()}
        if not all(vals.values()):
            messagebox.showerror("Απαιτείται είσοδος",
                                 "Όλα τα πεδία είναι υποχρεωτικά.")
            return
        try:
            mark = float(vals["le_mark"])
        except ValueError:
            messagebox.showerror("Μη έγκυρη τιμή",
                                 "Ο βαθμός πρέπει να είναι αριθμός.")
            return

        exam = db.mock_exam(vals["le_name"], vals["le_date"],
                            vals["le_subj"], mark)
        exam.log_exam()
        self._le_status.config(
            text=f"✓  {vals['le_name']} · {vals['le_subj']} · {mark}  καταχωρήθηκε.",
            fg=GREEN,
        )
        for e in self._le.values():
            e.delete(0, "end")
        self._le["le_date"].insert(0, str(date.today()))

    # ══════════════════════════════════════════════════════════════════════════
    # ΣΕΛΙΔΑ: ΝΕΟΣ ΜΑΘΗΤΗΣ
    # ══════════════════════════════════════════════════════════════════════════
    def _page_add_student(self):
        self._clear_content()
        f = self.content

        tk.Label(f, text="Νέος Μαθητής", font=FONT_XL,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=24, pady=(20, 4))
        tk.Label(f,
                 text="⚠  Η Student.save() δεν υλοποιείται στο db_comms.py — "
                      "το αντικείμενο δημιουργείται μόνο στη μνήμη.",
                 font=FONT_SM, bg=BG, fg=YELLOW,
                 ).pack(anchor="w", padx=24, pady=(0, 14))

        form = tk.Frame(f, bg=BG)
        form.pack(anchor="w", padx=24)

        fields = [
            ("Όνομα",       "as_name"),
            ("Ηλικία",      "as_age"),
            ("Τάξη / Τμήμα", "as_grade"),
        ]
        self._as: dict[str, tk.Entry] = {}
        for i, (lbl_txt, key) in enumerate(fields):
            tk.Label(form, text=lbl_txt, font=FONT_SM,
                     bg=BG, fg=MUTED).grid(row=i * 2, column=0,
                                            sticky="w", pady=(10, 2))
            e = _entry(form, width=30)
            e.grid(row=i * 2 + 1, column=0, sticky="w", ipady=7)
            self._as[key] = e

        self._as_status = tk.Label(f, text="", font=FONT_SM, bg=BG, fg=MUTED,
                                   wraplength=560, justify="left")
        self._as_status.pack(anchor="w", padx=24, pady=10)

        _btn(f, "Προσθήκη", self._do_add_student).pack(
            anchor="w", padx=24, ipady=8, ipadx=20)

    def _do_add_student(self):
        name  = self._as["as_name"].get().strip()
        age   = self._as["as_age"].get().strip()
        grade = self._as["as_grade"].get().strip()

        if not all([name, age, grade]):
            messagebox.showerror("Απαιτείται είσοδος",
                                 "Όλα τα πεδία είναι υποχρεωτικά.")
            return
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Μη έγκυρη τιμή",
                                 "Η ηλικία πρέπει να είναι ακέραιος.")
            return

        db.Student(name, age, grade)
        self._as_status.config(
            text=f"✓  Student(name='{name}', age={age}, grade='{grade}') δημιουργήθηκε.\n"
                  "   Υλοποίησε Student.save() για αποθήκευση στη βάση δεδομένων.",
            fg=MUTED,
        )


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = ExamTracker()
    app.mainloop()