# Overview

### __ASTEROID__: Automated, Solution for Testing Efficiently on Replicable, Operative, and Isolated Databases.

This pytest plugin is made for testing with MySQL docker images and is based on the great [lovely-pytest-docker](https://github.com/lovelysystems/lovely-pytest-docker "lovely-pytest-docker GitHub") plugin by Lovely Systems.

__pytest-asteroid__ extends the lovely-pytest-docker plugin by adding:
- an availability check to make sure the MySQL image is ready for connection before running the database test suite.
- a simple reset state functionality to handle state dependency issues between tests.

---
## How do I get set up?

### Dependencies
Make sure your system has [Docker Engine](https://docs.docker.com/engine/install/) installed and that the docker daemon is running before executing your tests.

### Installation

Install __pytest-asteroid__ using pip or poetry. We prefer to use [poetry](https://python-poetry.org/) as it reduces the amount of files needed in the project and simplifies dependency management and virtual environments.

_Install with poetry:_
```shell
$ poetry add pytest-asteroid --dev
```

---
## Examples of usage

In order to use ASTEROID make sure to have the following environmental variables set for the test DB docker image:
* MYSQL_DATABASE
* MYSQL_ROOT_PASSWORD

#### Using the get_docker_db_port fixture
```python
# content from conftest.py

###############################################################################
# * Connection to test database
# This fixture uses the ASTEROID fixture get_docker_db_port which, on first
# session-scoped call, will envoke the docker_service startup.
###############################################################################
# Overwrite this fixture if a custom connection type is required
###############################################################################


# NOTE: Here we are using class fixture as we need the connection to close again
# after each test class run if we want to reset state.
# If attemting to reset state, while a connection is open,
# we will have a deadlock.
@pytest.fixture(scope="class")
def get_connection(get_docker_db_port):
    conn = pymysql.connect(
        database=os.environ["MYSQL_DATABASE"],
        port=get_docker_db_port("mysql_db", timeout=30.0),
        user="root",
        password=os.environ["MYSQL_ROOT_PASSWORD"],
        cursorclass=pymysql.cursors.DictCursor,
    )
    # Start a transaction and rollback to reset state after each test class execution
    yield conn
    conn.close()

```

#### Using the get_connection and reset_or_save_db_state fixtures
```python
# content from test_state.py

class TestSaveState:
    # Test cases to check reset state works

    def test_connection_insert(self, get_connection, reset_or_save_db_state):
        reset_or_save_db_state("mysql_db", "superheroes")

        conn = get_connection
        # setup: insert new data
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO superheroes (name, cape, height_cm, weigth_kg)
                VALUES('Dr. Strange', true, 188, 82)
                """
            )
            conn.commit()
            cur.execute("SELECT * FROM superheroes WHERE name = 'Dr. Strange'")
            rows = cur.fetchall()
            assert len(rows) == 1

```

### Clarification
Use the examples in the project repository folder _*tests/*_ for inspiration on how to use __pytest-asteroid__ and to see examples of test file structure.
