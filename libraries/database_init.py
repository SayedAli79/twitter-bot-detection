import sqlite3
import numpy as np
from collections import defaultdict

class DataBase(object):
    def __init__(self, database_name,table_name):
        self.database_name = database_name
        self.table_name = table_name

    def create_table(self): 
        conn = sqlite3.connect(self.database_name)
        conn.execute('''DROP TABLE IF EXISTS {tn};'''.format(tn=self.table_name))
        conn.execute('''CREATE TABLE {tn}
           (NAME            TEXT     NOT NULL,
           IS_BOT          INTEGER NOT NULL,
           DATE            TEXT     NOT NULL,
           TEXT            TEXT     NOT NULL,
           MENTIONS        TEXT     NOT NULL);'''.format(tn=self.table_name))
        conn.close()

    def feed_table(self, user, is_bot, tweet_date, tweet_text, tweet_mentions):
        conn = sqlite3.connect(self.database_name)
        conn.execute("INSERT INTO {tn} (NAME, IS_BOT, DATE,TEXT,MENTIONS) VALUES (?, ?,?,?,?)".format(tn=self.table_name),
                     (user, is_bot, tweet_date, tweet_text, tweet_mentions))

        conn.commit()
        conn.close()

    def avg_mentions_per_user(self, is_bot=False):
        conn = sqlite3.connect(self.database_name)
        res = conn.execute("""
                SELECT NAME, MENTIONS
                FROM {tn}
                WHERE IS_BOT = {is_bot:d}
            """.format(tn=self.table_name, is_bot=is_bot))

        mentions_per_user = defaultdict(lambda: [])
        for (name, mention) in res:
            count = 0
            if len(mention) > 0:
                count = len(mention.split(","))
            mentions_per_user[name].append(count)

        avg_per_user = {}
        for (user, mentions) in mentions_per_user.iteritems():
            avg_per_user[user] = np.mean(mentions)

        conn.close()

        return avg_per_user
