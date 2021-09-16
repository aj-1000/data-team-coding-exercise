import sys

from subprocess import run

python_scripts = [
    './src/test_data_transformation.py',
    './src/test_data_analysis.py'
]

for script in python_scripts:
    run([sys.executable, '-m', 'pytest', script])