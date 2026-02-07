import difflib

t1 = "Pelosi's Power Play: Why the Former Speaker Is Betting on a Kennedy in New York"
t2 = "Pelosi's Power Play: The Kennedy Comeback Kid Gets Her Blessing"
t3 = "Pelosi's Power Play: The Kennedy Comeback in New York's 12th District"

def check(a, b):
    ratio = difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()
    print(f"Ratio: {ratio:.3f} | Match (>0.85): {ratio > 0.85}")

check(t1, t2)
check(t1, t3)
check(t2, t3)
