import os
import shlex

import pymysql
import pytest

###############################################################################
# Globals
###############################################################################

# Variables
root_password = None
restarted = False

# Constants
STANDARD_TIMEOUT = 60.0

###############################################################################
# Docker compose
###############################################################################
# "By default the fixture will look for the docker-compose.yml file in the
# tests subfolder of the path where pytest.ini resides (or the project's root
# directory if no ini file is given - as in the tests example)."
# (from documentation https://github.com/lovelysystems/lovely-pytest-docker)
###############################################################################


def mysql_availability_check(docker_ip, public_port) -> bool:
    """Try to connect as root user to the database from outside of the container

    Inspired by
    https://github.com/docker-library/docs/blob/9660a0cccb87d8db842f33bc0578d769caaf3ba9/bonita/stack.yml#L28-L44
    """
    try:
        conn = pymysql.connect(port=public_port, user="root", password=root_password)
    except pymysql.err.OperationalError:
        return False
    conn.close()
    return True


@pytest.fixture(scope="session")
def get_docker_db_port(request, docker_services):
    """Starts a Docker database container and returns port for connection.
    The Docker image will automatically be shutdown after PyTest run,
    unless the optional flag --keepalive is set.

    Args:
        service_name (str): The name of the database service
    """

    def _inject_params(service_name, timeout=STANDARD_TIMEOUT):
        global restarted
        # using global boolean 'restarted' to ensure one restart only per test run
        if not restarted and request.config.getoption("--restart", False):
            docker_services.shutdown()
            restarted = True

        docker_services.start()
        global root_password
        root_password = os.environ["MYSQL_ROOT_PASSWORD"]
        public_port = docker_services.wait_for_service(
            service_name,
            3306,
            check_server=mysql_availability_check,
            timeout=timeout,
        )
        return public_port

    return _inject_params


###############################################################################
# State dependency solution
# -----------------------------------------------------------------------------


def save_state(services, service_name, db_name):
    command = [
        "mysqldump",
        "-uroot",
        f"--password={root_password}",
        "--add-drop-table",  # overwrites when calling reset
        "--skip-lock-tables",
        "--routines",
        f"--result-file={db_name}_saved_state.sql",
        f"{db_name}",
    ]
    return services.execute(service_name, *command)


def reset_state(services, service_name, db_name):
    command = shlex.split(
        f'sh -c "mysql -uroot --password={root_password} {db_name} < {db_name}_saved_state.sql"'
    )
    return services.execute(service_name, *command)


@pytest.fixture(scope="function")
def reset_or_save_db_state(docker_services):
    """Reset the state of a database if previous state has been saved,
    otherwise save the state

    :param docker_services: docker-compose service (fixture)
    :return: A function that takes in a docker service name and a database name.
    """

    def _inject_params(service_name, db_name):
        try:
            output = reset_state(docker_services, service_name, db_name)
        except Exception as exc:
            if (
                "cannot open" in exc.args[0]
                or "No such file or directory" in exc.args[0]
            ):  # file does not appear to exist
                output = save_state(docker_services, service_name, db_name)
            else:
                raise exc
        return output

    return _inject_params


###############################################################################
# Command line options

# NOTE: This function should be implemented only in plugins or conftest.py files
# situated at the tests root directory due to how pytest discovers plugins during startup.
def pytest_addoption(parser):
    """Add custom options to pytest.
    Add the --restart option for pytest.
    """
    parser.addoption(
        "--restart",
        "-R",
        action="store_true",
        default=False,
        help="Force restart on docker containers",
    )
