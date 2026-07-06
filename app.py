import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import hashlib as hl
import db_comms as db

# ── Palette — ίδια με το website ───────────────────────────────────────────────
NAVY   = "#0D2B45"   # sidebar, topbar, τίτλοι
NAVY_L = "#152F48"   # sidebar hover
TEAL   = "#1A7080"   # secondary accent, labels
CYAN   = "#2AB5A0"   # success
GOLD   = "#C9A025"   # primary buttons, active indicator
GOLD_L = "#D4AD35"   # button active state
BG     = "#F4F8FA"   # app background
WHITE  = "#FFFFFF"   # cards, entries
TEXT   = "#0D2B45"   # main text
MUTED  = "#6B8299"   # secondary text
BORDER = "#D5E4EE"   # dividers, card borders
RED    = "#C0392B"   # errors

FONT_XS  = ("Segoe UI", 8,  "bold")
FONT_SM  = ("Segoe UI", 9)
FONT_MD  = ("Segoe UI", 11)
FONT_LG  = ("Segoe UI", 13, "bold")
FONT_XL  = ("Segoe UI", 19, "bold")


# ── Widget factories ───────────────────────────────────────────────────────────
def _entry(parent, **kwargs):
    return tk.Entry(
        parent, font=FONT_MD, bg=WHITE, fg=TEXT,
        insertbackground=TEAL, relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=TEAL,
        **kwargs,
    )


def _gold_btn(parent, text, cmd, **kwargs):
    return tk.Button(
        parent, text=text, command=cmd,
        font=("Segoe UI", 10, "bold"),
        bg=GOLD, fg=NAVY,
        activebackground=GOLD_L, activeforeground=NAVY,
        relief="flat", cursor="hand2",
        **kwargs,
    )


def _outline_btn(parent, text, cmd, **kwargs):
    return tk.Button(
        parent, text=text, command=cmd,
        font=("Segoe UI", 10),
        bg=WHITE, fg=TEAL,
        activebackground=BG, activeforeground=TEAL,
        relief="flat", cursor="hand2",
        highlightthickness=1, highlightbackground=TEAL,
        **kwargs,
    )


def _card(parent, **kwargs):
    """Λευκό panel με border."""
    return tk.Frame(
        parent, bg=WHITE,
        highlightthickness=1, highlightbackground=BORDER,
        **kwargs,
    )


def _section_header(parent, title):
    tk.Label(parent, text=title, font=FONT_XL,
             bg=BG, fg=NAVY).pack(anchor="w", padx=28, pady=(22, 0))
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=28, pady=(10, 16))


# ══════════════════════════════════════════════════════════════════════════════
class ExamTracker(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("ExamTracker")
        self.geometry("1000x620")
        self.minsize(1000, 620)
        self.configure(bg=BG)
        self.current_user: dict | None = None
        self._active_nav: str | None = None
        self._nav_rows: dict = {}
        self._build_ttk_style()
        self._show_login()

    # ── TTK ────────────────────────────────────────────────────────────────────
    def _build_ttk_style(self):
        s = ttk.Style(self)
        s.theme_use("default")
        s.configure("Treeview",
                    background=WHITE, foreground=TEXT,
                    fieldbackground=WHITE, rowheight=30,
                    font=FONT_MD, borderwidth=0)
        s.configure("Treeview.Heading",
                    background=NAVY, foreground=WHITE,
                    font=("Segoe UI", 10, "bold"), relief="flat")
        s.map("Treeview",
              background=[("selected", CYAN)],
              foreground=[("selected", WHITE)])

    # ── Helpers ────────────────────────────────────────────────────────────────
    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ══════════════════════════════════════════════════════════════════════════
    # LOGIN
    # ══════════════════════════════════════════════════════════════════════════
    def _show_login(self):
        self._clear()
        self.configure(bg=BG)

        # Λεπτή navy λωρίδα πάνω
        tk.Frame(self, bg=NAVY, height=5).pack(fill="x")

        outer = tk.Frame(self, bg=BG)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        # Two-tone logo
        logo_row = tk.Frame(outer, bg=BG)
        logo_row.pack(pady=(0, 24))
        tk.Label(logo_row, text="EXAM", font=("Segoe UI", 28, "bold"),
                 bg=BG, fg=NAVY).pack(side="left")
        tk.Label(logo_row, text="TRACKER", font=("Segoe UI", 28, "bold"),
                 bg=BG, fg=TEAL).pack(side="left")

        # Λευκή κάρτα σύνδεσης
        card = _card(outer)
        card.pack()

        inner = tk.Frame(card, bg=WHITE)
        inner.pack(padx=44, pady=38)

        tk.Label(inner, text="Σύνδεση στο λογαριασμό σου",
                 font=FONT_LG, bg=WHITE, fg=NAVY).pack(anchor="w", pady=(0, 4))
        tk.Label(inner, text="Εισάγαγε τα στοιχεία σου για να συνεχίσεις.",
                 font=FONT_SM, bg=WHITE, fg=MUTED).pack(anchor="w", pady=(0, 24))

        self._login_fields: dict[str, tk.Entry] = {}
        for lbl_txt, key, show in [
            ("ΟΝΟΜΑ ΧΡΗΣΤΗ", "username", ""),
            ("ΚΩΔΙΚΟΣ",      "password", "•"),
        ]:
            tk.Label(inner, text=lbl_txt, font=FONT_XS,
                     bg=WHITE, fg=MUTED).pack(anchor="w", pady=(0, 5))
            e = _entry(inner, width=30, show=show)
            e.pack(anchor="w", pady=(0, 18), ipady=9, fill="x")
            self._login_fields[key] = e

        self._login_err = tk.Label(inner, text="", font=FONT_SM,
                                   bg=WHITE, fg=RED)
        self._login_err.pack(pady=(0, 8))

        _gold_btn(inner, "Σύνδεση  →", self._do_login,
                  padx=0, pady=0).pack(fill="x", ipady=10)

        self._login_fields["username"].focus_set()
        self._login_fields["password"].bind("<Return>", lambda _: self._do_login())

    def _do_login(self):
        u = self._login_fields["username"].get().strip()
        p = self._login_fields["password"].get().strip()
        if not u or not p:
            self._login_err.config(text="Συμπλήρωσε και τα δύο πεδία.")
            return
        hashed = hl.sha256(p.encode()).hexdigest()
        result = db.Backend_user(u, hashed, None).log_in()
        if not result or result == "Error!":
            self._login_err.config(text="Λάθος στοιχεία σύνδεσης.")
        else:
            self.current_user = {"username": u, "type": result[0]}
            self._show_main()

    # ══════════════════════════════════════════════════════════════════════════
    # MAIN SHELL
    # ══════════════════════════════════════════════════════════════════════════
    def _show_main(self):
        self._clear()
        self._nav_rows = {}
        self._active_nav = None

        # ── Top bar ───────────────────────────────────────────────────────────
        top = tk.Frame(self, bg=NAVY, height=56)
        top.pack(fill="x")
        top.pack_propagate(False)

        # Two-tone logo
        logo_f = tk.Frame(top, bg=NAVY)
        logo_f.pack(side="left", padx=20, pady=0)
        tk.Label(logo_f, text="EXAM", font=("Segoe UI", 14, "bold"),
                 bg=NAVY, fg=WHITE).pack(side="left")
        tk.Label(logo_f, text="TRACKER", font=("Segoe UI", 14, "bold"),
                 bg=NAVY, fg=CYAN).pack(side="left")

        # Thin vertical separator
        tk.Frame(top, bg="#1E3F5A", width=1).pack(side="left", fill="y", pady=14)

        tk.Label(top, text=f"  {self.current_user['username']}",
                 font=("Segoe UI", 10, "bold"), bg=NAVY, fg=WHITE
                 ).pack(side="left", padx=6)
        tk.Label(top, text=f"· {self.current_user['type']}",
                 font=FONT_SM, bg=NAVY, fg="#7BA0BB").pack(side="left")

        # Logout button
        tk.Button(
            top, text="Αποσύνδεση", font=("Segoe UI", 9),
            bg="#1E3F5A", fg="#B0C8DC",
            activebackground="#28506E", activeforeground=WHITE,
            relief="flat", cursor="hand2", padx=12, pady=4,
            command=self._show_login,
        ).pack(side="right", padx=16, pady=14)

        # Thin separator under topbar
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # ── Body ──────────────────────────────────────────────────────────────
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        sidebar = tk.Frame(body, bg=NAVY, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Frame(sidebar, bg="#1E3F5A", height=1).pack(fill="x")  # top separator

        # Right-side separator (1px)
        tk.Frame(body, bg=BORDER, width=1).pack(side="left", fill="y")

        self.content = tk.Frame(body, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

        # Nav items
        tk.Frame(sidebar, bg=NAVY, height=10).pack()  # top spacer
        nav = [
            ("📊", "Στατιστικά",     self._page_stats),
            ("📝", "Καταχώρηση",     self._page_log_exam),
            ("💳", "Πληρωμές",       self._page_payments),
            ("👤", "Νέος Μαθητής",   self._page_add_student),
        ]
        for icon, label, cmd in nav:
            self._make_nav_item(sidebar, icon, label, cmd)

        self._set_active_nav("Στατιστικά")
        self._page_stats()

    def _make_nav_item(self, parent, icon, label, cmd):
        row = tk.Frame(parent, bg=NAVY, cursor="hand2")
        row.pack(fill="x")

        indicator = tk.Frame(row, bg=NAVY, width=3)
        indicator.pack(side="left", fill="y")

        content = tk.Frame(row, bg=NAVY)
        content.pack(side="left", fill="x", expand=True, padx=16, pady=12)

        ico = tk.Label(content, text=icon, font=("Segoe UI", 12),
                       bg=NAVY, fg=WHITE)
        ico.pack(side="left", padx=(0, 10))

        txt = tk.Label(content, text=label, font=("Segoe UI", 10),
                       bg=NAVY, fg="#8AAFC8", anchor="w")
        txt.pack(side="left")

        all_w = [row, content, ico, txt]

        self._nav_rows[label] = {
            "widgets": all_w, "indicator": indicator, "txt": txt
        }

        def enter(e):
            if self._active_nav != label:
                for w in all_w: w.config(bg=NAVY_L)
                indicator.config(bg=GOLD)
                txt.config(fg=WHITE)

        def leave(e):
            if self._active_nav != label:
                for w in all_w: w.config(bg=NAVY)
                indicator.config(bg=NAVY)
                txt.config(fg="#8AAFC8")

        def click(e):
            self._set_active_nav(label)
            cmd()

        for w in all_w:
            w.bind("<Enter>", enter)
            w.bind("<Leave>", leave)
            w.bind("<Button-1>", click)

    def _set_active_nav(self, label):
        # Deactivate previous
        if self._active_nav and self._active_nav in self._nav_rows:
            old = self._nav_rows[self._active_nav]
            for w in old["widgets"]: w.config(bg=NAVY)
            old["indicator"].config(bg=NAVY)
            old["txt"].config(fg="#8AAFC8")
        self._active_nav = label
        if label in self._nav_rows:
            new = self._nav_rows[label]
            for w in new["widgets"]: w.config(bg=NAVY_L)
            new["indicator"].config(bg=GOLD)
            new["txt"].config(fg=WHITE)

    # ══════════════════════════════════════════════════════════════════════════
    # ΣΕΛΙΔΑ: ΣΤΑΤΙΣΤΙΚΑ
    # ══════════════════════════════════════════════════════════════════════════
    def _page_stats(self):
        self._clear_content()
        f = self.content

        _section_header(f, "Στατιστικά")

        # ── Search card ───────────────────────────────────────────────────────
        sc = _card(f)
        sc.pack(fill="x", padx=28, pady=(0, 14))

        sc_inner = tk.Frame(sc, bg=WHITE)
        sc_inner.pack(fill="x", padx=22, pady=20)

        tk.Label(sc_inner, text="ΑΝΑΖΗΤΗΣΗ", font=FONT_XS,
                 bg=WHITE, fg=MUTED).pack(anchor="w", pady=(0, 14))

        inp_row = tk.Frame(sc_inner, bg=WHITE)
        inp_row.pack(anchor="w")

        tk.Label(inp_row, text="Μαθητής", font=("Segoe UI", 9, "bold"),
                 bg=WHITE, fg=TEAL).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self._s_name = _entry(inp_row, width=24)
        self._s_name.grid(row=1, column=0, padx=(0, 20), ipady=8, sticky="w")

        tk.Label(inp_row, text="Μάθημα", font=("Segoe UI", 9, "bold"),
                 bg=WHITE, fg=TEAL).grid(row=0, column=1, sticky="w", pady=(0, 5))
        self._s_subj = _entry(inp_row, width=20)
        self._s_subj.grid(row=1, column=1, ipady=8, sticky="w")

        btn_row = tk.Frame(sc_inner, bg=WHITE)
        btn_row.pack(anchor="w", pady=(16, 0))

        _gold_btn(btn_row, "Γεν. Μ.Ο.", self._stat_overall,
                  padx=14, pady=7).pack(side="left", padx=(0, 8))
        _gold_btn(btn_row, "Μ.Ο. Μαθήματος", self._stat_subject,
                  padx=14, pady=7).pack(side="left", padx=(0, 8))
        _outline_btn(btn_row, "Εμφάνιση Βαθμών", self._stat_grades,
                     padx=14, pady=7).pack(side="left")

        # ── Result strip ──────────────────────────────────────────────────────
        rc = _card(f)
        rc.pack(fill="x", padx=28, pady=(0, 14))

        self._stat_result = tk.Label(
            rc, text="  Επίλεξε μαθητή και πάτα κάποιο κουμπί.",
            font=("Segoe UI", 12), bg=WHITE, fg=MUTED,
            anchor="w", padx=22, pady=14,
        )
        self._stat_result.pack(fill="x")

        # ── Grades table ──────────────────────────────────────────────────────
        tc = _card(f)
        tc.pack(fill="both", expand=True, padx=28, pady=(0, 22))

        hdr = tk.Frame(tc, bg=WHITE)
        hdr.pack(fill="x", padx=18, pady=(14, 0))
        tk.Label(hdr, text="ΑΠΟΤΕΛΕΣΜΑΤΑ", font=FONT_XS,
                 bg=WHITE, fg=MUTED).pack(side="left")
        tk.Frame(tc, bg=BORDER, height=1).pack(fill="x", padx=18, pady=(8, 0))

        tree_wrap = tk.Frame(tc, bg=WHITE)
        tree_wrap.pack(fill="both", expand=True, padx=18, pady=(6, 18))

        self._tree = ttk.Treeview(
            tree_wrap,
            columns=("Μαθητής", "Μάθημα", "Βαθμός"),
            show="headings", height=8,
        )
        for col, w, anc in [
            ("Μαθητής", 270, "w"),
            ("Μάθημα",  270, "w"),
            ("Βαθμός",  120, "center"),
        ]:
            self._tree.heading(col, text=f"  {col}")
            self._tree.column(col, width=w, anchor=anc)

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    def _stat_overall(self):
        name = self._s_name.get().strip()
        if not name:
            messagebox.showerror("Προσοχή", "Εισάγαγε όνομα μαθητή.")
            return
        avg = db.Student(name, None, None).get_avg()
        if avg == -1:
            self._stat_result.config(
                text="  ⚠  Δεν βρέθηκαν εγγραφές για αυτόν τον μαθητή.", fg=GOLD)
        else:
            self._stat_result.config(
                text=f"  Γενικός μ.ο. για {name}:  {avg}", fg=CYAN)

    def _stat_subject(self):
        name = self._s_name.get().strip()
        subj = self._s_subj.get().strip()
        if not name or not subj:
            messagebox.showerror("Προσοχή", "Εισάγαγε όνομα μαθητή και μάθημα.")
            return
        avg = db.Student(name, None, None).get_avg_subj(subj)
        if avg == -1:
            self._stat_result.config(
                text="  ⚠  Δεν βρέθηκαν εγγραφές.", fg=GOLD)
        else:
            self._stat_result.config(
                text=f"  Μ.ο. {subj} για {name}:  {avg}", fg=CYAN)

    def _stat_grades(self):
        name = self._s_name.get().strip()
        subj = self._s_subj.get().strip()
        if not name or not subj:
            messagebox.showerror("Προσοχή", "Εισάγαγε όνομα μαθητή και μάθημα.")
            return
        self._tree.delete(*self._tree.get_children())
        grades = db.Student(name, None, None).list_grades(subj)
        for g in grades:
            self._tree.insert("", "end", values=(name, subj, g))
        count = len(grades)
        if count:
            self._stat_result.config(
                text=f"  {count} βαθμοί για {name} / {subj}", fg=CYAN)
        else:
            self._stat_result.config(
                text="  ⚠  Δεν βρέθηκαν βαθμοί.", fg=GOLD)

    # ══════════════════════════════════════════════════════════════════════════
    # ΣΕΛΙΔΑ: ΚΑΤΑΧΩΡΗΣΗ
    # ══════════════════════════════════════════════════════════════════════════
    def _page_log_exam(self):
        self._clear_content()
        f = self.content

        _section_header(f, "Καταχώρηση Εξέτασης")

        fc = _card(f)
        fc.pack(fill="x", padx=28, pady=(0, 14))

        fc_inner = tk.Frame(fc, bg=WHITE)
        fc_inner.pack(fill="x", padx=22, pady=20)

        tk.Label(fc_inner, text="ΣΤΟΙΧΕΙΑ ΕΞΕΤΑΣΗΣ", font=FONT_XS,
                 bg=WHITE, fg=MUTED).grid(row=0, column=0, columnspan=4,
                                            sticky="w", pady=(0, 16))

        # 2×2 grid layout
        fields = [
            ("ΟΝΟΜΑ ΜΑΘΗΤΗ",            "le_name", "", 0, 0),
            ("ΜΑΘΗΜΑ",                  "le_subj", "", 0, 2),
            ("ΗΜΕΡΟΜΗΝΙΑ (ΕΕΕΕ-ΜΜ-ΗΗ)", "le_date", str(date.today()), 2, 0),
            ("ΒΑΘΜΟΣ",                  "le_mark", "", 2, 2),
        ]

        self._le: dict[str, tk.Entry] = {}
        for lbl_txt, key, default, r, c in fields:
            tk.Label(fc_inner, text=lbl_txt, font=FONT_XS,
                     bg=WHITE, fg=TEAL
                     ).grid(row=r, column=c, sticky="w",
                             pady=(10 if r > 0 else 0, 5), padx=(0, 30))
            e = _entry(fc_inner, width=24)
            e.grid(row=r + 1, column=c, sticky="w", ipady=8, padx=(0, 30))
            if default:
                e.insert(0, default)
            self._le[key] = e

        # Status + button
        status_f = tk.Frame(fc, bg=WHITE)
        status_f.pack(fill="x", padx=22, pady=(10, 0))

        self._le_status = tk.Label(status_f, text="", font=FONT_MD,
                                    bg=WHITE, fg=CYAN, anchor="w")
        self._le_status.pack(anchor="w", pady=(0, 4))

        _gold_btn(fc, "  Καταχώρηση  ✓  ", self._do_log_exam,
                  padx=0, pady=0).pack(anchor="w", padx=22, pady=(0, 22), ipady=9, ipadx=6)

    def _do_log_exam(self):
        vals = {k: v.get().strip() for k, v in self._le.items()}
        if not all(vals.values()):
            messagebox.showerror("Προσοχή", "Όλα τα πεδία είναι υποχρεωτικά.")
            return
        try:
            mark = float(vals["le_mark"])
        except ValueError:
            messagebox.showerror("Μη έγκυρη τιμή", "Ο βαθμός πρέπει να είναι αριθμός.")
            return
        db.mock_exam(vals["le_name"], vals["le_date"], vals["le_subj"], mark).log_exam()
        self._le_status.config(
            text=f"  ✓  {vals['le_name']} · {vals['le_subj']} · {mark}  καταχωρήθηκε.",
            fg=CYAN,
        )
        for e in self._le.values():
            e.delete(0, "end")
        self._le["le_date"].insert(0, str(date.today()))

    # ══════════════════════════════════════════════════════════════════════════
    # ΣΕΛΙΔΑ: ΠΛΗΡΩΜΕΣ
    # ══════════════════════════════════════════════════════════════════════════
    def _page_payments(self):
        self._clear_content()
        f = self.content

        _section_header(f, "Πληρωμές")

        # ── Καταχώρηση πληρωμής ─────────────────────────────────────────────
        fc = _card(f)
        fc.pack(fill="x", padx=28, pady=(0, 14))

        fc_inner = tk.Frame(fc, bg=WHITE)
        fc_inner.pack(fill="x", padx=22, pady=20)

        tk.Label(fc_inner, text="ΝΕΑ ΠΛΗΡΩΜΗ", font=FONT_XS,
                 bg=WHITE, fg=MUTED).grid(row=0, column=0, columnspan=4,
                                            sticky="w", pady=(0, 16))

        fields = [
            ("ΟΝΟΜΑ ΜΑΘΗΤΗ",            "pay_name",   "", 0, 0),
            ("ΠΟΣΟ (€)",                "pay_amount", "", 0, 2),
            ("ΗΜΕΡΟΜΗΝΙΑ (ΕΕΕΕ-ΜΜ-ΗΗ)", "pay_date",   str(date.today()), 2, 0),
        ]

        self._pay: dict[str, tk.Entry] = {}
        for lbl_txt, key, default, r, c in fields:
            tk.Label(fc_inner, text=lbl_txt, font=FONT_XS,
                     bg=WHITE, fg=TEAL
                     ).grid(row=r, column=c, sticky="w",
                             pady=(10 if r > 0 else 0, 5), padx=(0, 30))
            e = _entry(fc_inner, width=24)
            e.grid(row=r + 1, column=c, sticky="w", ipady=8, padx=(0, 30))
            if default:
                e.insert(0, default)
            self._pay[key] = e

        status_f = tk.Frame(fc, bg=WHITE)
        status_f.pack(fill="x", padx=22, pady=(10, 0))

        self._pay_status = tk.Label(status_f, text="", font=FONT_MD,
                                     bg=WHITE, fg=CYAN, anchor="w")
        self._pay_status.pack(anchor="w", pady=(0, 4))

        _gold_btn(fc, "  Καταχώρηση Πληρωμής  ✓  ", self._do_log_payment,
                  padx=0, pady=0).pack(anchor="w", padx=22, pady=(0, 22), ipady=9, ipadx=6)

        # ── Αναζήτηση υπολοίπου ──────────────────────────────────────────────
        sc = _card(f)
        sc.pack(fill="x", padx=28, pady=(0, 14))

        sc_inner = tk.Frame(sc, bg=WHITE)
        sc_inner.pack(fill="x", padx=22, pady=20)

        tk.Label(sc_inner, text="ΑΝΑΖΗΤΗΣΗ ΥΠΟΛΟΙΠΟΥ", font=FONT_XS,
                 bg=WHITE, fg=MUTED).pack(anchor="w", pady=(0, 14))

        inp_row = tk.Frame(sc_inner, bg=WHITE)
        inp_row.pack(anchor="w")

        tk.Label(inp_row, text="Μαθητής", font=("Segoe UI", 9, "bold"),
                 bg=WHITE, fg=TEAL).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self._pay_search_name = _entry(inp_row, width=24)
        self._pay_search_name.grid(row=1, column=0, ipady=8, sticky="w")

        _gold_btn(sc_inner, "Εμφάνιση Υπολοίπου", self._show_balance,
                  padx=14, pady=7).pack(anchor="w", pady=(16, 0))

        # ── Result strip ──────────────────────────────────────────────────────
        rc = _card(f)
        rc.pack(fill="x", padx=28, pady=(0, 14))

        self._balance_result = tk.Label(
            rc, text="  Επίλεξε μαθητή και πάτα «Εμφάνιση Υπολοίπου».",
            font=("Segoe UI", 12), bg=WHITE, fg=MUTED,
            anchor="w", padx=22, pady=14,
        )
        self._balance_result.pack(fill="x")

        # ── Ιστορικό πληρωμών ────────────────────────────────────────────────
        tc = _card(f)
        tc.pack(fill="both", expand=True, padx=28, pady=(0, 22))

        hdr = tk.Frame(tc, bg=WHITE)
        hdr.pack(fill="x", padx=18, pady=(14, 0))
        tk.Label(hdr, text="ΙΣΤΟΡΙΚΟ ΠΛΗΡΩΜΩΝ", font=FONT_XS,
                 bg=WHITE, fg=MUTED).pack(side="left")
        tk.Frame(tc, bg=BORDER, height=1).pack(fill="x", padx=18, pady=(8, 0))

        tree_wrap = tk.Frame(tc, bg=WHITE)
        tree_wrap.pack(fill="both", expand=True, padx=18, pady=(6, 18))

        self._pay_tree = ttk.Treeview(
            tree_wrap,
            columns=("Ημερομηνία", "Ποσό"),
            show="headings", height=8,
        )
        for col, w, anc in [
            ("Ημερομηνία", 270, "w"),
            ("Ποσό",       270, "center"),
        ]:
            self._pay_tree.heading(col, text=f"  {col}")
            self._pay_tree.column(col, width=w, anchor=anc)

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self._pay_tree.yview)
        self._pay_tree.configure(yscrollcommand=vsb.set)
        self._pay_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    def _do_log_payment(self):
        vals = {k: v.get().strip() for k, v in self._pay.items()}
        if not all(vals.values()):
            messagebox.showerror("Προσοχή", "Όλα τα πεδία είναι υποχρεωτικά.")
            return
        try:
            amount = float(vals["pay_amount"])
        except ValueError:
            messagebox.showerror("Μη έγκυρη τιμή", "Το ποσό πρέπει να είναι αριθμός.")
            return
        db.payment(vals["pay_name"], vals["pay_date"], amount).log_payment()
        self._pay_status.config(
            text=f"  ✓  {vals['pay_name']} · {amount}€ καταχωρήθηκε.",
            fg=CYAN,
        )
        for e in self._pay.values():
            e.delete(0, "end")
        self._pay["pay_date"].insert(0, str(date.today()))

    def _show_balance(self):
        name = self._pay_search_name.get().strip()
        if not name:
            messagebox.showerror("Προσοχή", "Εισάγαγε όνομα μαθητή.")
            return
        student = db.Student(name, None, None)
        expected, paid, balance = student.get_balance()

        self._pay_tree.delete(*self._pay_tree.get_children())
        for c_date, amount in student.list_payments():
            self._pay_tree.insert("", "end", values=(c_date, amount))

        if expected == -1:
            self._balance_result.config(
                text=f"  ⚠  Δεν βρέθηκε τάξη/ημερομηνία εγγραφής (ή η τάξη δεν "
                     f"υπάρχει στο grade) για {name}. (N/A)",
                fg=GOLD,
            )
        else:
            color = RED if balance > 0 else CYAN
            self._balance_result.config(
                text=(f"  {name}  ·  Αναμενόμενο: {expected}€  ·  "
                      f"Πληρωμένο: {paid}€  ·  Υπόλοιπο: {balance}€"),
                fg=color,
            )

    # ══════════════════════════════════════════════════════════════════════════
    # ΣΕΛΙΔΑ: ΝΕΟΣ ΜΑΘΗΤΗΣ
    # ══════════════════════════════════════════════════════════════════════════
    def _page_add_student(self):
        self._clear_content()
        f = self.content

        _section_header(f, "Νέος Μαθητής")

        # Form card
        fc = _card(f)
        fc.pack(fill="x", padx=28, pady=(0, 14))

        fc_inner = tk.Frame(fc, bg=WHITE)
        fc_inner.pack(fill="x", padx=22, pady=20)

        tk.Label(fc_inner, text="ΣΤΟΙΧΕΙΑ ΜΑΘΗΤΗ", font=FONT_XS,
                 bg=WHITE, fg=MUTED).pack(anchor="w", pady=(0, 16))

        fields = [
            ("ΟΝΟΜΑ", "as_name"),
            ("ΗΛΙΚΙΑ", "as_age"),
            ("ΤΑΞΗ / ΤΜΗΜΑ", "as_grade"),
            ("ΗΜΕΡΟΜΗΝΙΑ ΕΓΓΡΑΦΗΣ (ΕΕΕΕ-ΜΜ-ΗΗ)", "as_enroll_date"),
        ]
        self._as: dict[str, tk.Entry] = {}
        for lbl_txt, key in fields:
            tk.Label(fc_inner, text=lbl_txt, font=FONT_XS,
                     bg=WHITE, fg=TEAL).pack(anchor="w", pady=(8, 5))
            e = _entry(fc_inner, width=32)
            e.pack(anchor="w", ipady=8, fill="x")
            if key == "as_enroll_date":
                e.insert(0, str(date.today()))
            self._as[key] = e

        self._as_status = tk.Label(fc, text="", font=FONT_SM,
                                    bg=WHITE, fg=MUTED,
                                    anchor="w", wraplength=620, justify="left")
        self._as_status.pack(anchor="w", padx=22, pady=(10, 0))

        _gold_btn(fc, "  Προσθήκη Μαθητή  ", self._do_add_student,
                  padx=0, pady=0).pack(anchor="w", padx=22, pady=(8, 22), ipady=9, ipadx=6)

    def _do_add_student(self):
        name        = self._as["as_name"].get().strip()
        age         = self._as["as_age"].get().strip()
        grade       = self._as["as_grade"].get().strip()
        enroll_date = self._as["as_enroll_date"].get().strip()
        if not all([name, age, grade, enroll_date]):
            messagebox.showerror("Προσοχή", "Όλα τα πεδία είναι υποχρεωτικά.")
            return
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Μη έγκυρη τιμή", "Η ηλικία πρέπει να είναι ακέραιος.")
            return
        db.Student(name, age, grade).save(grade, enroll_date)
        self._as_status.config(
            text=f"  ✓  Ο μαθητής {name} ({grade}) προστέθηκε επιτυχώς.",
            fg=CYAN,
        )
        for e in self._as.values():
            e.delete(0, "end")
        self._as["as_enroll_date"].insert(0, str(date.today()))


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = ExamTracker()
    app.mainloop()