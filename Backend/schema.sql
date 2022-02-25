CREATE table profile (
    uid TEXT NOT NULL,
    pid TEXT,
    name1 TEXT NOT NULL,
    name2 TEXT,
    name3 TEXT,
    minority INTEGER,
    persuasive INTEGER,
    boss INTEGER,
    current_time TEXT,
    PRIMARY KEY (uid)
);

CREATE table poisratings (
    uid TEXT NOT NULL,
    items TEXT,
    selected INTEGER,
    minority INTEGER,
    current_time TEXT,
    PRIMARY KEY (uid)
);

CREATE TABLE information (
  uid TEXT NOT NULL,
  emo INTEGER,
  loc INTEGER,
  fin INTEGER,
  rel INTEGER,
  health INTEGER,
  sex INTEGER,
  alc INTEGER,
  minority INTEGER,
  persuasive INTEGER,
  boss INTEGER,
  current_time TEXT,
  PRIMARY KEY (uid)
 );

CREATE table demographics (
    uid TEXT NOT NULL,
    age INTEGER,
    gender INTEGER,
    nationality TEXT,
    education INTEGER,
    application INTEGER,
    current_time TEXT,
    PRIMARY KEY (uid)
);

-- CREATE TABLE benefit (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   uid TEXT NOT NULL,
--   b1 INTEGER,
--   b2 INTEGER,
--   b3 INTEGER,
--   b4 INTEGER,
--   b5 INTEGER,
--   b6 INTEGER,
--   b7 INTEGER,
--   current_time TEXT
-- );

-- CREATE TABLE risk (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   uid TEXT NOT NULL,
--   r1 INTEGER,
--   r2 INTEGER,
--   r3 INTEGER,
--   r4 INTEGER,
--   r5 INTEGER,
--   r6 INTEGER,
--   r7 INTEGER,
--   c1 TEXT,
--   current_time TEXT
-- );

CREATE TABLE emotion (
  uid TEXT NOT NULL,
  ben INTEGER,
  risk INTEGER,
  cmt TEXT,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE location (
  uid TEXT NOT NULL,
  ben INTEGER,
  risk INTEGER,
  cmt TEXT,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE financial (
  uid TEXT NOT NULL,
  ben INTEGER,
  risk INTEGER,
  cmt TEXT,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE religion (
  uid TEXT NOT NULL,
  ben INTEGER,
  risk INTEGER,
  cmt TEXT,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE sexuality (
  uid TEXT NOT NULL,
  ben INTEGER,
  risk INTEGER,
  cmt TEXT,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE health (
  uid TEXT NOT NULL,
  ben INTEGER,
  risk INTEGER,
  cmt TEXT,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE alcohol (
  uid TEXT NOT NULL,
  ben INTEGER,
  risk INTEGER,
  cmt TEXT,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE privacy (
  uid TEXT NOT NULL,
  g1 INTEGER,
  g2 INTEGER,
  g3 INTEGER,
  g4 INTEGER,
  g5 INTEGER,
  g6 INTEGER,
  g7 INTEGER,
  g8 INTEGER,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE trust (
  uid TEXT NOT NULL,
  t1 INTEGER,
  t2 INTEGER,
  t3 INTEGER,
  t4 INTEGER,
  t5 INTEGER,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE personality1 (
  uid TEXT NOT NULL,
  p1 INTEGER,
  p2 INTEGER,
  p3 INTEGER,
  p4 INTEGER,
  p5 INTEGER,
  p6 INTEGER,
  p7 INTEGER,
  p8 INTEGER,
  p9 INTEGER,
  p10 INTEGER,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE personality2 (
  uid TEXT NOT NULL,
  p11 INTEGER,
  p12 INTEGER,
  p13 INTEGER,
  ac1 INTEGER,
  p14 INTEGER,
  p15 INTEGER,
  p16 INTEGER,
  p17 INTEGER,
  p18 INTEGER,
  p19 INTEGER,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE personality3 (
  uid TEXT NOT NULL,
  p20 INTEGER,
  p21 INTEGER,
  p22 INTEGER,
  p23 INTEGER,
  p24 INTEGER,
  p25 INTEGER,
  p26 INTEGER,
  ac2 INTEGER,
  p27 INTEGER,
  p28 INTEGER,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE personality4 (
  uid TEXT NOT NULL,
  p29 INTEGER,
  p30 INTEGER,
  p31 INTEGER,
  p32 INTEGER,
  p33 INTEGER,
  p34 INTEGER,
  p35 INTEGER,
  p36 INTEGER,
  p37 INTEGER,
  p38 INTEGER,
  current_time TEXT,
  PRIMARY KEY (uid)
);

CREATE TABLE personality5 (
  uid TEXT NOT NULL,
  p39 INTEGER,
  p40 INTEGER,
  p41 INTEGER,
  p42 INTEGER,
  ac3 INTEGER,
  p43 INTEGER,
  p44 INTEGER,
  c2 TEXT,
  current_time TEXT,
  PRIMARY KEY (uid)
);