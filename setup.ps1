copier -r 535cf75
py -3.9 -m venv .venv
.venv/Scripts/activate
pip install -U pip  # throws [WinError 5], but still works on its own
pip install wheel
pip install -r requirements_dev.txt
flit install -s
