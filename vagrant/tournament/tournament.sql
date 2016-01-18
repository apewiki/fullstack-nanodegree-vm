-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--DROP DATABASE IF EXISTS tournament;
--CREATE DATABASE tournament;

DROP TABLE IF EXISTS players;
CREATE TABLE players (
id serial PRIMARY KEY,
name varchar(50) NOT NULL);

DROP TABLE IF EXISTS matches;
CREATE TABLE matches (
id serial,
points INTEGER,
round INTEGER);
--DELETE FROM players;
INSERT INTO players (name) VALUES ('Qin');
INSERT INTO players (name) VALUES ('Alex');
INSERT INTO players (name) VALUES ('Joe');
INSERT INTO players (name) VALUES ('Zeus');
INSERT INTO matches (SELECT a.id, 0, 0 FROM players a WHERE a.name = 'Alex');
INSERT INTO matches (SELECT a.id, 0, 0 FROM players a WHERE a.name = 'Qin');
INSERT INTO matches (SELECT a.id, 0, 0 FROM players a WHERE a.name = 'Joe');
INSERT INTO matches (SELECT a.id, 0, 0 FROM players a WHERE a.name = 'Zeus');
UPDATE matches SET points = points + 1, round = round + 1 from players AS b WHERE matches.id = b.id and b.name = 'Alex';
UPDATE matches SET round = round + 1 from players AS b WHERE matches.id = b.id and b.name = 'Qin';

UPDATE matches SET points = points + 1, round = round + 1 from players AS b WHERE matches.id = b.id and b.name = 'Zeus';
UPDATE matches SET round = round + 1 from players AS b WHERE matches.id = b.id and b.name = 'Joe';

UPDATE matches SET points = points + 1, round = round + 1 from players AS b WHERE matches.id = b.id and b.name = 'Alex';
UPDATE matches SET round = round + 1 from players AS b WHERE matches.id = b.id and b.name = 'Zeus';

UPDATE matches SET points = points + 1, round = round + 1 from players AS b WHERE matches.id = b.id and b.name = 'Joe';
UPDATE matches SET round = round + 1 from players AS b WHERE matches.id = b.id and b.name = 'Qin';

--INSERT INTO matches (SELECT a.id, b.id, 1, 2 FROM players a, players b WHERE a.name = 'Alex' AND b.name = 'Joe');
--INSERT INTO matches (SELECT a.id, b.id, 1, 1 FROM players a, players b WHERE a.name = 'Alex' AND b.name = 'Zeus');

--DELETE FROM matches;
SELECT * from players;
SELECT * from matches;

SELECT players.name, matches.points from players, matches WHERE matches.round = (SELECT max(round) FROM matches) AND players.id = matches.id order by matches.points DESC;