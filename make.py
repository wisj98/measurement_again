import pickle

recipes = {"가": [["first", 10, 1],["second", 5, 2],["third", 3, 0.1]],
           "다": [["first", 10, 1],["second", 5, 2],["third", 3, 0.1]],
           "나": [["first", 10, 1],["second", 5, 2],["third", 3, 0.1]],
           "라": [["first", 10, 1],["second", 5, 2],["third", 3, 0.1]],
           "마": [["first", 10, 1],["second", 5, 2],["third", 3, 0.1]],
           "바": [["first", 10, 1],["second", 5, 2],["third", 3, 0.1]],
           "사": [["first", 10, 1],["second", 5, 2],["third", 3, 0.1]],
           "아": [["first", 10, 1],["second", 5, 2],["third", 3, 0.1]],
           "차": [["first", 10, 1],["second", 5, 2],["third", 3, 0.1]],
           "카": [["first", 10, 1],["second", 5, 2],["third", 3, 0.1]],
           "타": [["first", 10, 1],["second", 5, 2],["third", 3, 0.1],["second", 5, 2],["third", 3, 0.1],["second", 5, 2],["third", 3, 0.1],["second", 5, 2],["third", 3, 0.1],["second", 5, 2],["third", 3, 0.1]]}

with open('recipe.pickle', 'wb') as f:
    pickle.dump(recipes, f)


