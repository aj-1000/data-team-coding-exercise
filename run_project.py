from fastlogging import LogInit
from subprocess import call

logger = LogInit(pathName='logs/master.log', console=True, colors=True)

python_scripts = [
    './src/data_ingestion.py',
    './src/data_transformation.py',
    './src/data_analysis.py'
]

for script in python_scripts:
    logger.info(f"--- Executing {script} --- \n")
    call(['python', script])
    logger.info(f"--- Finished executing {script} --- \n")