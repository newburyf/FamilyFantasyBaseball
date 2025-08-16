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