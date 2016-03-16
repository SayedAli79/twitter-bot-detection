from config import app_config as cfg
import numpy as np
import scipy.stats as stats
import pylab as pl

from libraries.database_init import DataBase

db = DataBase(cfg.database["name"], cfg.database["tweet_table"])

avg_mention_per_user = db.avg_mentions_per_user()
h = sorted(avg_mention_per_user.values())
print h
fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
pl.plot(h,fit,'-o')
pl.hist(h,normed=True)
pl.show()