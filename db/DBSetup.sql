DROP TABLE IF EXISTS teams;

DROP TABLE IF EXISTS rounds;

DROP TABLE IF EXISTS positions;

DROP TABLE IF EXISTS participants;

DROP TABLE IF EXISTS players;

DROP TABLE IF EXISTS games;

DROP TABLE IF EXISTS gameStats;

DROP TABLE IF EXISTS draft;

CREATE TABLE teams (
    mlbID INTEGER PRIMARY KEY,
    code TEXT NOT NULL,
    teamName TEXT NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE rounds (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE positions (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participantName TEXT NOT NULL
);

CREATE TABLE players (
    mlbID INTEGER PRIMARY KEY,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL
);

CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teamOne INTEGER REFERENCES teams(mlbID),
    teamTwo INTEGER REFERENCES teams(mlbID),
    roundCode TEXT REFERENCES rounds(code),
    day INTEGER NOT NULL,
    month TEXT NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE gameStats (
    playerID INTEGER REFERENCES players(mlbID),
    gameID INTEGER REFERENCES games(id),
    hTB INTEGER NOT NULL,
    hRBI INTEGER NOT NULL,
    hR INTEGER NOT NULL,
    hSB INTEGER NOT NULL,
    hBB INTEGER NOT NULL,
    hK INTEGER NOT NULL,
    pIP INTEGER NOT NULL,
    pW INTEGER NOT NULL,
    pL INTEGER NOT NULL,
    pHD INTEGER NOT NULL,
    pSV INTEGER NOT NULL,
    pER INTEGER NOT NULL,
    pH INTEGER NOT NULL,
    pK INTEGER NOT NULL,
    pBB INTEGER NOT NULL,
    points INTEGER NOT NULL,
    PRIMARY KEY(playerID, gameID)
);

CREATE TABLE draft (
    playerID INTEGER REFERENCES players(mlbID),
    participantName TEXT REFERENCES participants(participantName),
    positionCode TEXT REFERENCES positions(code),
    teamCode INTEGER REFERENCES teams(mlbID),
    draftRoundCode TEXT REFERENCES rounds(code),
    year INTEGER NOT NULL,
    PRIMARY KEY(participantName, playerID, year)
);

INSERT INTO teams (location, teamName, code, mlbID) 
VALUES
    ('Arizona','Diamondbacks','ARI',109),
    ('Atlanta','Braves','ATL',144),
    ('Baltimore','Orioles','BAL',110),
    ('Boston','Red Sox','BOS',111),
    ('Chicago','Cubs','CHC',112),
    ('Chicago','White Sox','CWS',145),
    ('Cincinnati','Reds','CIN',113),
    ('Cleveland','Guardians','CLE',114),
    ('Colorado','Rockies','COL',115),
    ('Detroit','Tigers','DET',116),
    ('Miami','Marlins','MIA',146),
    ('Houston','Astros','HOU',117),
    ('Kansas City','Royals','KC',118),
    ('Los Angeles','Angels','LAA',108),
    ('Los Angeles','Dodgers','LAD',119),
    ('Milwaukee','Brewers','MIL',158),
    ('Minnesota','Twins','MIN',142),
    ('New York','Mets','NYM',121),
    ('New York','Yankees','NYY',147),
    ('Sacramento','Athletics','ATH',133),
    ('Philadelphia','Phillies','PHI',143),
    ('Pittsburgh','Pirates','PIT',134),
    ('San Diego','Padres','SD',135),
    ('San Francisco','Giants','SF',137),
    ('Seattle','Mariners','SEA',136),
    ('St. Louis','Cardinals','STL',138),
    ('Tampa Bay','Rays','TB',139),
    ('Texas','Rangers','TEX',140),
    ('Toronto','Blue Jays','TOR',141),
    ('Washington','Nationals','WAS',120);

INSERT INTO rounds (code, name)
VALUES
    ('WC','Wild Card'),
    ('DS','Division Series'),
    ('CS','Championship Series'),
    ('WS','World Series');

INSERT INTO positions (code, name)
VALUES
    ('IF','Infield'),
    ('OF','Outfield'),
    ('P','Pitcher');