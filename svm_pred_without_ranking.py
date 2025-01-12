import pandas as pd
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

file_type = "gossipcop"

# Load training dataset (only the main data, no additional data)
train_main = pd.read_csv(f"./{file_type}/{file_type}_resized.csv", sep=',', header=None)

# Ensure the training file is loaded correctly
print(f"Training data size: {len(train_main)}")

# Load testing dataset (only the main data, no additional data)
test_main = pd.read_csv(f"./{file_type}/{file_type}_resized_test.csv", sep=',', header=None)

# Ensure the testing file is loaded correctly
print(f"Testing data size: {len(test_main)}")

# Extract training data and labels
train_data = train_main.values
Ytrain = train_data[:, -1]  # Last column contains labels
Xtrain = train_data[:, :-1]  # All columns except the last one

# Extract testing data and labels
test_data = test_main.values
Ytest = test_data[:, -1]  # Last column contains labels
Xtest = test_data[:, :-1]  # All columns except the last one

print("Training size: ", Xtrain.shape[0])
print("Test size", Xtest.shape[0])

# Standardize the data
scaler = preprocessing.StandardScaler()
Xtrain_scaled = scaler.fit_transform(Xtrain)
Xtest_scaled = scaler.transform(Xtest)

# Train the Poly SVM with specified hyperparameters
print("\nTraining Poly SVM with C=10 and degree=3")
model_svm = SVC(kernel="poly", C=10, degree=3)
model_svm.fit(Xtrain_scaled, Ytrain)

# Evaluate training score
train_score = model_svm.score(Xtrain_scaled, Ytrain)
print("Training score: ", train_score)

# Estimate generalization score on the test set
test_score = model_svm.score(Xtest_scaled, Ytest)
print("\nGeneralization (Test) score: ", test_score)

# Print classification report for the test set
y_pred = model_svm.predict(Xtest_scaled)
print("\nClassification Report:")
report = classification_report(Ytest, y_pred)
print(report)

# Save the classification report to a file
with open(f'./report/svm_{file_type}_report_without_ranking.txt', 'w') as f:
    f.write("SVM Classification Report without Ranking Data:\n")
    f.write(f"Kernel: Polynomial (C=10, degree=3)\n")
    f.write(report)
