import pickle

with open("config.pickle","rb") as fr:
    config = pickle.load(fr)

print(config["경로"])
config["경로"] = "data"

with open("config.pickle","wb") as f:
    pickle.dump(config, f)