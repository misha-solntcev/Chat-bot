import json
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

RANDOM_STATE = 42

with open("BOT_CONFIG.json", "r", encoding="utf8") as file:
    BOT_CONFIG = json.load(file)
X = []
y = []
count = 0
for intent in BOT_CONFIG["intents"].keys():
    try:
        for example in BOT_CONFIG["intents"][intent]["examples"]:
            X.append(example)
            y.append(intent)
    except KeyError:
        print("")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE)

vectorizer = CountVectorizer(ngram_range=(1, 2), analyzer="char_wb")
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

model = LogisticRegression(
    C=10, random_state=RANDOM_STATE, solver="lbfgs", max_iter=1000)
model.fit(X_train_vectorized, y_train)
print(model.predict(vectorizer.transform(["как погода?"])))
print(model.score(X_train_vectorized, y_train))
print(model.score(X_test_vectorized, y_test))

print("------")

model = RandomForestClassifier(
    random_state=RANDOM_STATE, n_estimators=200)
model.fit(X_train_vectorized, y_train)
print(model.predict(vectorizer.transform(["как погода?"])))
print(model.score(X_train_vectorized, y_train))
print(model.score(X_test_vectorized, y_test))


def get_intent(input_text):
    return model.predict(vectorizer.transform([input_text]))[0]


def bot(input_text):
    intent = get_intent(input_text)
    return random.choice(BOT_CONFIG["intents"][intent]["responses"])


input_text = ""
print("Для выхода из диалога напишите Пока")
print("----------------")

while True:
    input_text = input()
    if input_text == "":
        print("Вы ничего не ввели")
        continue
    if input_text == "Пока":
        break
    else:
        print(bot(input_text))
