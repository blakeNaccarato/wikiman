pip install -U pip wheel
pip install pipx
pipx install copier==6.0.0a7
copier -f -r 369ec2c
pip install -r tooling/requirements_cicd.txt
flit install
