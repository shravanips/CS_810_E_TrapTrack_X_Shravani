from z3 import *

click = Bool("user_clicked_accept")
script_runs = Bool("script_activated")
data_sent = Bool("user_data_sent")

s = Solver()
s.add(Implies(click, script_runs))
s.add(Implies(script_runs, data_sent))

if s.check() == sat:
    print("✔️ Possible data leak path:")
    print(s.model())
else:
    print("❌ No path detected")