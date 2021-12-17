import os

print(os.environ)
if not os.environ.get("ALADIN_TTB_KEY"):
    raise EnvironmentError("NO SECRET KEY")
