import pickle

config = {"결과 저장 경로":"", "작업자":[], "권한":{}}
with open('config.pickle', 'wb') as f:
    pickle.dump(config, f)