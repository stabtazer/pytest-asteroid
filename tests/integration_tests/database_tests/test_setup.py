import pymysql
import pytest


class TestDockerMySQL:
    # Test cases to check docker-compose can connect to mysql docker image

    def test_pytest_timeout_error(self, get_docker_db_port):
        with pytest.raises(Exception) as excinfo:
            _ = get_docker_db_port("mysql_db", timeout=0.1)
        assert "Timeout reached" in str(excinfo.value)

    def test_pytest_public_port(self, get_docker_db_port):
        assert get_docker_db_port("mysql_db") == 3307

    def test_connection_to_mysql_docker(self, get_connection):
        conn = get_connection
        assert conn.open

    def test_preloaded_data_exists(self, get_connection):
        conn = get_connection
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM superheroes WHERE name = 'Thor Odinson'")
            rows = cur.fetchall()
        assert len(rows) == 1

    def test_connection_insert(self, get_connection):
        conn = get_connection
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO superheroes (name, cape, height_cm, weigth_kg)
                VALUES('Hulk', false, 244, 635)
                """
            )
            cur.execute("SELECT * FROM superheroes")
            rows = cur.fetchall()
        assert len(rows) == 3

    def test_new_data_exists(self, get_connection):
        conn = get_connection
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM superheroes
                WHERE name = "Hulk"
                """
            )
            rows = cur.fetchall()
        assert len(rows) == 1

    def test_data_not_exists(self, get_connection):
        conn = get_connection
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM superheroes
                WHERE name = "Green Goblin"
                """
            )
            rows = cur.fetchall()
        assert len(rows) == 0


class TestResetStateByRollback:
    # Check that all inserts from previous test class runs are not committed
    def test_insert_data_and_count(self, get_connection):
        conn = get_connection
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO superheroes (name, cape, height_cm, weigth_kg)
                VALUES('She-Hulk', false, 201, 318)
                """
            )
            cur.execute("SELECT * FROM superheroes")
            rows = cur.fetchall()
        assert len(rows) == 3


class TestCheckMissingTable:
    def test_query_on_non_existing_table(self, get_connection):
        def get_non_existing_table():
            conn = get_connection
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM CarMakers
                    """
                )
            return cur.fetchall()

        with pytest.raises(
            pymysql.err.ProgrammingError, match=r"Table '.*' doesn't exist"
        ):
            get_non_existing_table()
