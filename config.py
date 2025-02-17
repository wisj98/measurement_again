import pickle

config = {"경로":"data", "작업자":{"지시자":["위성진1","위성진2","위성진3","위성진4","위성진5"], "작업자":["아래성진"], "배합자":["중간성진"], "가마":["a", "b", "c"]}, "권한":{"order":True, "measurement": True, "recipe": True, "mix": True, "ingredient": True}}
with open('config.pickle', 'wb') as f:
    pickle.dump(config, f)