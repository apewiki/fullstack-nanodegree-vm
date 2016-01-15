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
name varchar(50) UNIQUE NOT NULL);

DROP TABLE IF EXISTS matches;
CREATE TABLE matches (
id serial,
points INTEGER);
--DELETE FROM players;
INSERT INTO players (name) VALUES ('Qin');
INSERT INTO players (name) VALUES ('Alex');
INSERT INTO players (name) VALUES ('Joe');
INSERT INTO players (name) VALUES ('Zeus');
INSERT INTO matches (SELECT a.id, 1 FROM players a WHERE a.name = 'Alex');
UPDATE matches SET points = points + 1 from players AS b WHERE matches.id = b.id and b.name = 'Alex';

--INSERT INTO matches (SELECT a.id, b.id, 1, 2 FROM players a, players b WHERE a.name = 'Alex' AND b.name = 'Joe');
--INSERT INTO matches (SELECT a.id, b.id, 1, 1 FROM players a, players b WHERE a.name = 'Alex' AND b.name = 'Zeus');

--DELETE FROM matches;
SELECT * from players;
SELECT * from matches;

