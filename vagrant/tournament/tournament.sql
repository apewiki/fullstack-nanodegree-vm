-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament;

--Create the table to store player information
DROP TABLE IF EXISTS players;
CREATE TABLE players (
id serial PRIMARY KEY,
name varchar(50) NOT NULL);

--Create the table to store point for each player in each round
--Points increment by 1 if player wins a round
DROP TABLE IF EXISTS matches;
CREATE TABLE matches (
id serial,
points INTEGER,
round INTEGER);


-- Create a view for standings that is sorted by desceding order
DROP VIEW IF EXISTS views;
CREATE VIEW standings (id, name, points, round) 
	AS SELECT players.id, players.name, matches.points, matches.round 
	FROM players, matches WHERE players.id = matches.id 
	ORDER BY matches.round, matches.points DESC;
