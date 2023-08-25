import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import plotly.graph_objs as go

# Read the data from the file
with open('flappy_bird_data_processed.txt', 'r') as file:
    lines = file.readlines()

# Initialize lists to store features and labels
X = []  # Features for the current line
y = []  # Labels for the next line

# Initialize variables to track the previous line's data and label
prev_data = None
label_count = 0  # Count of 1's before pipe_height changes
for line in lines:
    data, label = eval(line)  # Convert the line to a Python dictionary and label

    # If we have previous data, use it as features for the current line
    if prev_data is not None:
        X.append([prev_data['bird_velocity'], prev_data['bird_y'], prev_data['pipe_x'], prev_data['pipe_height']])
        y.append(label_count)  # Predict the number of 1's before pipe_height changes

    # Update previous data and label count for the next iteration
    prev_data = data

    # Check if pipe_height has changed (label changes from 1 to 0)
    if label == 0:
        label_count = 0
    else:
        label_count += label

# Convert lists to NumPy arrays
X = np.array(X)
y = np.array(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train a Logistic Regression model
model = DecisionTreeClassifier()  # Use DecisionTreeClassifier
model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Count the number of label=1 data points in testing data and predicted data
num_label_1_testing = np.sum(y_test == 1)
num_label_1_predicted = np.sum(y_pred == 1)
print(f"Number of label=1 data points in testing data: {num_label_1_testing}")
print(f"Number of label=1 data points in predicted data: {num_label_1_predicted}")

test_label_1_indices = np.where(y_test == 1)[0]
predicted_label_1_indices = np.where(y_pred == 1)[0]

# Check if the positions of label 1 data points are equal
if np.array_equal(test_label_1_indices, predicted_label_1_indices):
    print("Label 1 positions in testing data and predicted data are equal.")
else:
    print("Label 1 positions in testing data and predicted data are not equal.")

# Create a list of coordinates for the plot
coordinates = list(zip(test_label_1_indices, predicted_label_1_indices))

# Create a Plotly figure
fig = go.Figure()

# Add a scatter plot
fig.add_trace(go.Scatter(x=[coord[0] for coord in coordinates],
                         y=[coord[1] for coord in coordinates],
                         mode='markers',
                         text=["Point " + str(i+1) for i in range(len(coordinates))],
                         name='Positions of Label 1'))

# Set plot labels and title
fig.update_layout(title="Positions of Label 1 in Testing Data vs. Predicted Data",
                  xaxis_title="Testing Data Index",
                  yaxis_title="Predicted Data Index")

# Show the plot
fig.show()