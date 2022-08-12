import os
import pymysql
import pytest

###############################################################################
# Setting environment variables:
# - MYSQL_DATABASE: Should match the name defined in create_database.sql
# - MYSQL_ROOT_PASSWORD
os.environ["MYSQL_DATABASE"] = "superheroes"
os.environ["MYSQL_ROOT_PASSWORD"] = "my_secret_password"
###############################################################################


@pytest.fixture(scope="session")
def docker_compose_files(pytestconfig):
    """Get the docker-compose.yml absolute path.
    Override this fixture in your tests if you need a custom location.
    NOTE: Added because default path tests/ for docker-compose has been changed
    """
    return [
        os.path.join(
            str(pytestconfig.rootdir),
            "tests/integration_tests/database_tests",
            "docker-compose.yml",
        )
    ]


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
