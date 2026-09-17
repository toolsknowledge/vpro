import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB


# --------------------------------
# 1. Dataset
# --------------------------------

data = {
    "Outlook": [
        "Sunny", "Sunny", "Overcast", "Rain",
        "Rain", "Rain", "Overcast", "Sunny",
        "Sunny", "Rain", "Sunny", "Overcast",
        "Overcast", "Rain"
    ],

    "Temperature": [
        "Hot", "Hot", "Hot", "Mild",
        "Cool", "Cool", "Cool", "Mild",
        "Cool", "Mild", "Mild", "Mild",
        "Hot", "Mild"
    ],

    "Humidity": [
        "High", "High", "High", "High",
        "Normal", "Normal", "Normal", "High",
        "Normal", "Normal", "Normal", "High",
        "Normal", "High"
    ],

    "Wind": [
        "Weak", "Strong", "Weak", "Weak",
        "Weak", "Strong", "Strong", "Weak",
        "Weak", "Weak", "Strong", "Strong",
        "Weak", "Strong"
    ],

    "PlayTennis": [
        "No", "No", "Yes", "Yes",
        "Yes", "No", "Yes", "No",
        "Yes", "Yes", "Yes", "Yes",
        "Yes", "No"
    ]
}


df = pd.DataFrame(data)


# --------------------------------
# 2. Encode categorical data
# --------------------------------

encoder = LabelEncoder()

df["Outlook"] = encoder.fit_transform(df["Outlook"])
df["Temperature"] = encoder.fit_transform(df["Temperature"])
df["Humidity"] = encoder.fit_transform(df["Humidity"])
df["Wind"] = encoder.fit_transform(df["Wind"])
df["PlayTennis"] = encoder.fit_transform(df["PlayTennis"])


# --------------------------------
# 3. Separate X and y
# --------------------------------

X = df[
    [
        "Outlook",
        "Temperature",
        "Humidity",
        "Wind"
    ]
]

y = df["PlayTennis"]


# --------------------------------
# 4. Create Naive Bayes model
# --------------------------------

model = GaussianNB()


# --------------------------------
# 5. Train model
# --------------------------------

model.fit(X, y)


# --------------------------------
# 6. New weather data
# --------------------------------

# Sunny = 2
# Cool = 0
# High = 0
# Strong = 1

new_data = [[2, 0, 0, 1]]


# --------------------------------
# 7. Prediction
# --------------------------------

prediction = model.predict(new_data)


# --------------------------------
# 8. Display result
# --------------------------------

if prediction[0] == 1:
    print("Prediction: Play Tennis = YES")
else:
    print("Prediction: Play Tennis = NO")







"""
    new_data_yes = pd.DataFrame({
    "Outlook": ["Sunny"],
    "Temperature": ["Cool"],
    "Humidity": ["Normal"],
    "Wind": ["Weak"]
})

prediction = model.predict(new_data_yes)

print("Prediction:", prediction[0])
"""