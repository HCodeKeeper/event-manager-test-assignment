# event-manager-test-assignment

Simple event manager, using users by email, custom jwt endpoints, authentication tests, validations.

## Run
```shell
# The app itself
docker compose -f local.yml up
# Tests
docker compose -f tests.yml up
```
When the server is up, visit:

http://0.0.0.0:8000/

(prepopulated superuser may not work)
