import copy
import random
import numpy as np
from wxshahe.models import Diet
from wxshahe.models import User
from wxshahe.models import Cook
from wxshahe.models import Log
from wxshahe.models import Attribution
from wxshahe.models import Group
from wxshahe.kmeans import distEclud
from wxshahe.kmeans import randCent
from wxshahe.kmeans import kMeans
from wxshahe.kmeans import biKmeans
#from apscheduler.scheduler import Scheduler

#sched = Scheduler()
# @sched.interval_schedule(seconds=60)


def personality():
    # 个性化推荐20个菜品
    user_list = User.objects.all()
    dataSet1 = []
    dataSet2 = []
    for user in user_list:
        us = []
        user_logs = Log.objects.filter(log_user_id=user.user_id)
        for log in user_logs:
            attribution = Attribution.objects.get(diet_id=log.log_diet_id)
            attri = []
            attri.append(attribution.attribution1)
            attri.append(attribution.attribution2)
            attri.append(attribution.attribution3)
            attri.append(attribution.attribution4)
            attri.append(attribution.attribution5)
            attri.append(attribution.attribution6)
            attri.append(attribution.attribution7)
            attri.append(attribution.attribution8)
            attri.append(attribution.attribution9)
            us.append(attri)
        us = np.array(us)
        us = np.mean(us, axis=0).tolist()
        dataSet1.append(us)  # dataSet1用于计算簇心

        us.append(user.user_id)  # 在尾部插入id
        dataSet2.append(us)
    print("dataSet1")
    print(dataSet1)
    print("dataSet2")
    print(dataSet2)
    a, b = biKmeans(dataSet1, 5)
    print("a")
    print(a)

    for user in dataSet2:
        min_dic = 0
        min_index = 0
        for clust in range(len(a)):
            dic = distEclud(user[0:len(user)], a[clust])
            if dic < min_dic:
                min_dic = dic
                min_index = clust
        us = Group(user_id=user[-1], group=min_index)
        us.save()
