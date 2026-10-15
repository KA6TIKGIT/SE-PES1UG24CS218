# Lab 5 Reflection: Static Code Analysis

## 1. What did you learn about static analysis tools?

Each of the three tools looks at a different side of the code. Pylint acted like a strict code reviewer (naming, docstrings, unused arguments, risky defaults), Flake8 checked PEP 8 formatting, and Bandit looked only for security problems. Running all three gave a much fuller picture than any one alone. On the original `event_manager.py`, Pylint scored 4.64/10, Bandit reported 4 issues (1 High, 1 Medium, 2 Low) and Flake8 reported 4 formatting errors. After the fixes, Pylint scored [FINAL PYLINT SCORE]/10 and Bandit and Flake8 reported no issues.

## 2. Which issues were the most important to fix, and why?

- **OS command injection (`os.system`, Bandit High).** Building a shell command from the event name meant a crafted name could run arbitrary commands. I replaced it with `subprocess.run` and a fixed argument list, so no shell is involved.
- **Unsafe `pickle.load` (Bandit Medium).** Loading a tampered pickle file can execute arbitrary code. I switched to JSON, which only stores data.
- **Mutable default argument `guests=[]` (Pylint).** This was the most interesting one because it was a real logic bug, not just a style issue. Every event created without a guest list shared the same list, so "Alumni Dinner" reported being full and the seat counts were wrong even though it had its own capacity. Using `None` as the default and creating a new list inside the function fixed it.

## 3. Were there any limits to what the tools could find?

Yes. The tools flagged the mutable default as a "dangerous default value", but they did not tell me about the actual symptom, which only showed up when I ran the program and read the output carefully (wrong seat counts and a false "full" message). Static analysis also cannot judge intent. For example, `printBadges` was never called, so the command injection was not exploitable in the demo, but it was still worth fixing. Some warnings also needed judgment: after moving to `subprocess`, Bandit still raised low-severity warnings about the module, which I handled with a documented `# nosec` comment because the command uses fixed arguments and no shell. Tools are a first pass and do not replace running and testing the code.

## 4. How would static analysis change the way you write code in future?

- Run Pylint, Flake8 and Bandit regularly while developing instead of only at the end, so problems are small when they are found.
- Follow naming (snake_case), docstring and formatting conventions from the start, which makes the code easier for others to read and maintain.
- Avoid risky patterns such as `os.system`, `pickle` for untrusted data, mutable default arguments and `random` where unpredictability matters.
- Use the tools in a team workflow, for example as a pre-commit hook or a CI check, so quality does not depend on one person remembering to run them.
- Treat tool output as a list to review, not a score to chase. I should understand why each warning appears before fixing or suppressing it.