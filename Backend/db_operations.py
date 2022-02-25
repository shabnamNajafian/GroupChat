from flask import g
from datetime import datetime


def insert_profile(uid, pid, name1, name2, name3, minority, persuasive, boss_in_minority):
    from flask import g
    current_time = datetime.now()
    g.db.execute("INSERT INTO profile(uid, pid, name1, name2, name3, minority, persuasive, boss,"
                 " current_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (uid, pid, name1, name2, name3, minority, persuasive, boss_in_minority, current_time))
    g.db.commit()


def insert_rating(uid, poi_list, selected_poi, minority):
    from flask import g
    current_time = datetime.now()
    g.db.execute("INSERT INTO poisratings(uid, items, selected, minority, current_time) VALUES (?, ?, ?, ?, ?)",
                 (uid, poi_list, selected_poi, minority, current_time))
    g.db.commit()


def get_selected_place(uuid):
    p = 0
    for place in query_db('select selected from poisratings where (uid = ?) LIMIT ?', [uuid, 1]):
        if place is not None:
            p = place
    return p


def insert_information(uid, emo, loc, fin, rel, health, sex, alc, minority, persuasive, boss):
    from flask import g
    current_time = datetime.now()

    g.db.execute("INSERT INTO information(uid, emo, loc, fin, rel, health, sex, alc, minority, persuasive, boss, current_time) "
                 "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (uid, emo, loc, fin, rel, health, sex, alc, minority, persuasive, boss, current_time))
    g.db.commit()


def get_selected_info(uuid, info_type):
    p = 0
    for info_selected in query_db('select ' + info_type + ' from information where (uid = ?) LIMIT ?', [uuid, 1]):
        if info_selected is not None:
            p = info_selected
    return p[info_type]


def insert_demographics(uid, age, gender, nationality, education, application):
    from flask import g
    current_time = datetime.now()

    g.db.execute("INSERT INTO demographics(uid, age, gender, nationality, education, application, current_time) "
                 "VALUES (?, ?, ?, ?, ?, ?, ?)",
                 (uid, age, gender, nationality, education, application, current_time))
    g.db.commit()


def insert_info(uid, info_type, ben, risk, cmt):
    from flask import g
    current_time = datetime.now()

    g.db.execute("INSERT INTO " + info_type + " (uid, ben, risk, cmt, current_time) "
                 "VALUES (?, ?, ?, ?, ?)",
                 (uid, ben, risk, cmt, current_time))
    g.db.commit()


def insert_risk(uid, r1, r2, r3, r4, r5, r6, r7, c1):
    from flask import g
    current_time = datetime.now()

    g.db.execute("INSERT INTO risk(uid, r1, r2, r3, r4, r5, r6, r7, c1, current_time) "
                 "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (uid, r1, r2, r3, r4, r5, r6, r7, c1, current_time))
    g.db.commit()


def insert_privacy(uid, g1, g2, g3, g4, g5, g6, g7, g8):
    from flask import g
    current_time = datetime.now()

    g.db.execute("INSERT INTO privacy(uid, g1, g2, g3, g4, g5, g6, g7, g8, current_time) "
                 "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (uid, g1, g2, g3, g4, g5, g6, g7, g8, current_time))
    g.db.commit()


def insert_trust(uid, t1, t2, t3, t4, t5):
    from flask import g
    current_time = datetime.now()

    g.db.execute("INSERT INTO trust(uid, t1, t2, t3, t4, t5, current_time) "
                 "VALUES (?, ?, ?, ?, ?, ?, ?)",
                 (uid, t1, t2, t3, t4, t5, current_time))
    g.db.commit()


def insert_personality1(uid, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10):
    from flask import g
    current_time = datetime.now()

    g.db.execute("INSERT INTO personality1(uid, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, current_time) "
                 "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (uid, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, current_time))
    g.db.commit()


def insert_personality2(uid, p11, p12, p13, ac1, p14, p15, p16, p17, p18, p19):
    from flask import g
    current_time = datetime.now()

    g.db.execute("INSERT INTO personality2(uid, p11, p12, p13, ac1, p14, p15, p16, p17, p18, p19, current_time) "
                 "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (uid, p11, p12, p13, ac1, p14, p15, p16, p17, p18, p19, current_time))
    g.db.commit()


def insert_personality3(uid, p20, p21, p22, p23, p24, p25, p26, ac2, p27, p28):
    from flask import g
    current_time = datetime.now()

    g.db.execute("INSERT INTO personality3(uid, p20, p21, p22, p23, p24, p25, p26, ac2, p27, p28, current_time) "
                 "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (uid, p20, p21, p22, p23, p24, p25, p26, ac2, p27, p28, current_time))
    g.db.commit()


def insert_personality4(uid, p29, p30, p31, p32, p33, p34, p35, p36, p37, p38):
    from flask import g
    current_time = datetime.now()

    g.db.execute("INSERT INTO personality4(uid, p29, p30, p31, p32, p33, p34, p35, p36, p37, p38, current_time) "
                 "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (uid, p29, p30, p31, p32, p33, p34, p35, p36, p37, p38, current_time))
    g.db.commit()


def insert_personality5(uid, p39, p40, p41, p42, ac3, p43, p44, c2):
    from flask import g
    current_time = datetime.now()

    g.db.execute("INSERT INTO personality5(uid, p39, p40, p41, p42, ac3, p43, p44, c2, current_time) "
                 "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                 (uid, p39, p40, p41, p42, ac3, p43, p44, c2, current_time))
    g.db.commit()


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def get_privacy_selection(query, args=()):
    prvcy = []
    for prvcy in query_db(query, args):
        if prvcy is not None:
            prvcy = prvcy
    return prvcy