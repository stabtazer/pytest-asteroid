# Database testing

## All tests that connects to a database. These should in all cases connect to a test database using a Docker image like MySQL.Dockerfile.

Make sure to group tests into the same class when the same transaction is needed.
All transactions using **get_connection** fixture will be reset on each new class of tests.

See templates for examples of use.

### Keep alive
Instead of the having the Docker container shut down automatically after tests, if you want to keep it running to manually verify data after test run then add the optional flag -K or --keepalive:
```
$ pytest --keepalive
```
