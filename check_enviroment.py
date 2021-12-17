import os

if not os.environ.get("ALADIN_TTB_KEY"):
    raise EnvironmentError("NO SECRET KEY")
