# Before you started
1. Create a new file called `.env`
2. Add secrets in `.env`
   * Assign JWT_SECRET_KEY. E.g. `JWT_SECRET_KEY=whoscall-secret`
   * Assign USER_PASSWORD. E.g. `USER_PASSWORD=whoscall-password`

# How to start this app
1. Install docker
2. Run `docker compose up`
3. Test by `curl http://localhost:5000/health_check`
4. If it is launched properly, you will see `OK`

# How to build this app
1. Install docker
2. Run `docker-compose build whoscall-app`
3. Wait and see `Building ... FINISHED`

# How to run unit test
1. Build testing docker image. `docker compose -f .\docker-compose-test.yaml build whoscall-app-test`
2. Run testing docker containers. `docker compose -f .\docker-compose-test.yaml up`
3. Run `docker exec whoscall-app-test pytest unit_tests`
4. You will see the result of pytest. E.g. `8 passes in 0.14s`

# How to run end-to-end(E2E) test
1. Build testing docker image. `docker compose -f .\docker-compose-test.yaml build whoscall-app-test`
2. Run testing docker containers. `docker compose -f .\docker-compose-test.yaml up`
3. Before sending any additional requests, run `docker exec whoscall-app-test python ./e2e_tests/e2e_tests_for_task_api.py`
4. You will see the result of end-to-end test. E.g. `Success!! ...`