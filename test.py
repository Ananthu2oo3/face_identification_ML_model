import pickle

with open('model.pkl', 'rb') as file:
    model_content = pickle.load(file)

print(model_content)