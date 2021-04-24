py -3.9 -m venv .venv
.venv/Scripts/activate
pip install -U pip  # throws [WinError 5], but still works on its own
pip install -U setuptools wheel
pip install -r dev_requirements.txt  # packages for development
