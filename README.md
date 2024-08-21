# aban_test

##installation: 
first of all, create docker network and volumes and run dev requirements in detached mode
then run wen compose and celery compose seperately 'docker-compose -f <compose name>.yaml up -d'

for testing, this command must be runned pnce inside container or any shell:
    './manage.py submit_test_data'

most of methods info is available at swagger page (/jkc3Em1/swagger/) 
each new registered user will automatically earn enough assets to be able to trade
