pip install -U pip         # throws [WinError 5], but still works on its own
pip install -U wheel       # speed up subsequent package installs
pip install -U setuptools  # update bundled setuptools
pip install -U -r .config\dev_requirements.txt  # packages for development
