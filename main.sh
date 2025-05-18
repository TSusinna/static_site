# This script is used to run the static site generator.
python3 src/main.py
cd docs && python3 -m http.server 8888