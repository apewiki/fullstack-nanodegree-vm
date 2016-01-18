#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    if db:
        cursor = db.cursor()
        query = "DELETE FROM matches;"
        cursor.execute(query)
        db.commit()
        db.close()
        return True
    else:
        print "db connection problem!"
        return False


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    if db:
        cursor = db.cursor()
        query = "DELETE FROM players;"
        cursor.execute(query)
        db.commit()
        db.close()
        return True
    else:
        print "db connection problem!"
        return False


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    count = 0
    if db:
        cursor = db.cursor()
        query = "SELECT COUNT(*) FROM players;"
        cursor.execute(query)
        rows = cursor.fetchone()
        count = rows[0]
        db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    if db:
        cursor = db.cursor()
        query = "INSERT INTO players (name) VALUES (%s) "
        cursor.execute(query, (name,))
        db.commit()
        # When a player is registered but before each match,
        # a record of 0 points and 0 round is inserted into matches table
        query = ('INSERT INTO matches (id, points, round)'
                 'VALUES ((SELECT id FROM players WHERE name = %s), 0, 0)')
        cursor.execute(query, (name,))
        db.commit()
        db.close()
        return True
    else:
        return False


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or
    a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    standings = ()
    if db:
        cursor = db.cursor()
        query = "SELECT id, name, points, round FROM standings;"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            standings += ((row[0], row[1], row[2], row[3]),)
        db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
       Increment points by 1 if the player wins.
       Increment round for the player once result is in
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    if db:
        cursor = db.cursor()
        query = ('UPDATE matches SET points = points + 1, round = round + 1'
                 'WHERE matches.id = %s')
        cursor.execute(query, (winner,))
        query = "UPDATE matches SET round = round + 1 WHERE matches.id = %s"
        cursor.execute(query, (loser,))
        db.commit()
        db.close()
        return True
    else:
        return False


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairs = []
    num_players = countPlayers()
    db = connect()
    if db:
        cursor = db.cursor()
        query = "SELECT max(round) FROM matches;"
        cursor.execute(query)
        curr_round = cursor.fetchone()[0]
        db.close()
    # Number of players have to be even
    if num_players % 2 != 0:
        print "Number of players must be even"
    standings = playerStandings()
    # This check is to avoid pairing where a round of match is not yet finished
    if len(standings) != num_players * curr_round:
        print "Current match is not finished yet"
    pair_count = 0
    pair = ()
    # Assign pair for players with equal or closest points
    for s in standings:
        if s[3] == curr_round:
            if len(pair)/2 < 2:
                pair += (s[0], s[1],)
            if pair_count % 2 == 1:
                pairs.append(pair)
                pair = ()
            pair_count += 1
    return pairs
