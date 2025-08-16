CREATE TABLE teams (
    mlbID INTEGER PRIMARY KEY
    code TEXT NOT NULL,
    teamName TEXT NOT NULL,
    location TEXT NOT NULL,
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
    FOREIGN KEY(teamOne) REFERENCES teams(code),
    FOREIGN KEY(teamTwo) REFERENCES teams(code),
    FOREIGN KEY(roundCode) REFERENCES rounds(code),
    day INTEGER NOT NULL,
    month TEXT NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE gameStats (
    FOREIGN KEY(playerID) REFERENCES players(id),
    FOREIGN KEY(gameID) REFERENCES games(id),

    # Hitting
    # TB: 1
    # RBIs: 1
    # R: 1
    # SB: 1
    # BB: 1
    # K: -1
    hTB INTEGER NOT NULL,
    hRBI INTEGER NOT NULL,
    hR INTEGER NOT NULL,
    hSB INTEGER NOT NULL,
    hBB INTEGER NOT NULL,
    hK INTEGER NOT NULL,

    # Pitching
    # IP: 3 / Outs: 1
    # W: 2
    # L: -2
    # HD (Hold): 2
    # SV (Save): 5
    # ER: -2
    # H: -1
    # K: 1
    # BB: -1
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
    FOREIGN KEY(playerID) REFERENCES players(id),
    FOREIGN KEY(participantName) REFERENCES participants(participantName),
    FOREIGN KEY(positionCode) REFERENCES positions(code),
    FOREIGN KEY(teamCode) REFERENCES teams(code),
    FOREIGN KEY(draftRoundCode) REFERENCES rounds(code),
    year INTEGER NOT NULL,
    PRIMARY KEY(participantName, playerID, year)
);
