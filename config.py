import pickle

config = {"경로":"data", "작업자":[], "권한":{"order":False, "measurement": True, "recipe": True, "mix": True, "ingredient": True}}
with open('config.pickle', 'wb') as f:
    pickle.dump(config, f)