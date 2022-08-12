-- Inserting data to mysql_db docker
SET @_default_id = 1;


INSERT INTO superheroes.superheroes (id, name, cape, height_cm, weigth_kg)
VALUES (@_default_id, 'Thor Odinson', true, 198, 290),
(@_default_id + 1, 'Spider-Man', false, 178, 76);

INSERT INTO superheroes.associations (id, name)
VALUES (@_default_id, 'Avengers'),
(@_default_id + 1, 'SHIELD');

-- Assigning Thor and Spider-Man to Avengers
INSERT INTO superheroes.member_of (superhero_id, associations_id)
VALUES (@_default_id, @_default_id),
(@_default_id + 1, @_default_id);
