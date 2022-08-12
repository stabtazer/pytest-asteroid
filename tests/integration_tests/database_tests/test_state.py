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


class TestStatePersists:
    # Test cases to check data state persists between test classes if not reset

    def test_connection_insert(self, get_connection):
        conn = get_connection
        with conn.cursor() as cur:

            # reset -> verify artist
            cur.execute("SELECT * FROM superheroes WHERE name = 'Dr. Strange'")
            rows = cur.fetchall()
            assert len(rows) == 1


class TestResetState:
    # Test cases to check reset state works

    def test_connection_reset(self, get_connection, reset_or_save_db_state):
        reset_or_save_db_state("mysql_db", "superheroes")
        conn = get_connection

        with conn.cursor() as cur:

            # reset -> verify artist
            cur.execute("SELECT * FROM superheroes WHERE name = 'Dr. Strange'")
            rows = cur.fetchall()
            assert not rows
