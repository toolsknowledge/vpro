# load_iris() is the predefined function
# load_iris() provides the ready made dataset (flowers)
from sklearn.datasets import load_iris

# train_test_split() is the predefined functions
# used to devide data into 1) training data(80%) and 2) testing data(20%)
from sklearn.model_selection import train_test_split

# RandomForestClassifier is the "model" to build RandomForest Application
# RandomForestClassifier (scikit-learn) (1lakh +) (average,std dev,wt std deviation)
from sklearn.ensemble import RandomForestClassifier

# accuracy
from sklearn.metrics import accuracy_score, classification_report

# --------------------------------------------------
# 1. Load Dataset
# --------------------------------------------------

iris = load_iris()

X = iris.data
y = iris.target

print("Features:")
print(iris.feature_names)

print("\nClasses:")
print(iris.target_names)

# --------------------------------------------------
# 2. Split Data into Training and Testing
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining samples:", len(X_train))      
print("Testing samples :", len(X_test))

# --------------------------------------------------
# 3. Create Random Forest
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    max_features="sqrt",
    bootstrap=True,
    random_state=42
)

# --------------------------------------------------
# 4. Train the Random Forest
# --------------------------------------------------

model.fit(X_train, y_train)

print("\nRandom Forest training completed.")

# --------------------------------------------------
# 5. Test the Model
# --------------------------------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=iris.target_names
))

# --------------------------------------------------
# 6. Feature Importance
# --------------------------------------------------

print("\nFeature Importance:")

for name, importance in zip(
    iris.feature_names,
    model.feature_importances_
):
    print(f"{name}: {importance:.3f}")

# --------------------------------------------------
# 7. Predict a New Flower
# --------------------------------------------------

sepal_length = float(input("\nEnter Sepal Length: "))
sepal_width = float(input("Enter Sepal Width: "))
petal_length = float(input("Enter Petal Length: "))
petal_width = float(input("Enter Petal Width: "))

new_flower = [[
    sepal_length,
    sepal_width,
    petal_length,
    petal_width
]]

prediction = model.predict(new_flower)

print("\nPredicted Flower:",
      iris.target_names[prediction[0]])