
#define a function to calculate the predictions for a specific belt
def linreg(center, belt):
    chute = xdf[(xdf['sorting_center_name'] == center) & (xdf['output_belt'] == belt)]
    lags = 7 
    X = create_lag_features(chute['no_of_events'], lags)

    # Create day_of_week feature
    X['day_of_week'] = chute['scanning_date'].dt.day_of_week + 1

    # Create cyclic features for day_of_week
    X['cos_day_of_week'] = np.cos(2 * np.pi * X['day_of_week'] / 7)
    X['sin_day_of_week'] = np.sin(2 * np.pi * X['day_of_week'] / 7)
    X.dropna(inplace=True)

    y = chute['no_of_events'][lags:]  # Target variable is the actual series shifted by the number of lags
    dates = chute['scanning_date'][lags:]  # Corresponding dates for the target

    # Split the data into train and test sets
    X_train, X_rest, y_train, y_rest, dates_train, dates_rest = train_test_split(
        X, y, dates, test_size=0.25, shuffle=False
    )
    X_test, X_drop, y_test, y_drop, dates_test, dates_drop = train_test_split(
        X_rest, y_rest, dates_rest, test_size=0.8, shuffle=False
    )
    # Train the model
    model = LinearRegression()
    model.fit(X_train[features], y_train)

    test_data = X_test.copy()  # Make a copy of the test data
    predictions = []

    # Recursive forecasting loop
    for i in range(len(X_test)):
        # Select the current row of features (including lags)
        row_data = X_test[features].iloc[i].to_frame().T 
        # Make the prediction for the current step
        pred = model.predict(row_data)[0]

        # Append the prediction to the predictions list
        predictions.append(pred)

        # Now, update lag_1 with this prediction for the next step
        for lag in range(1, 8):  # Loop over the 7 lags
            if i + lag < len(X_test):
                X_test.loc[X_test.index[i + lag], f'lag_{lag}'] = pred   

    # Convert predictions list to a NumPy array or DataFrame for analysis
    predictions = np.array(predictions)
    return np.array(y_test), predictions, dates_test


####
#calculate model performance for the linear regression model
days = 14
sorting_centers = xdf["sorting_center_name"].unique()
daily_errors = {}
daily_mse = {}
daily_mae = {}


for sorting_center in sorting_centers:
    output_belts = xdf[(xdf['sorting_center_name'] == sorting_center)]['output_belt'].unique()
    number_of_output_belts = len(output_belts)

    # For each output belt make forecasts
    for output_belt in output_belts:
        # Train and test the model for the given belt
        test = linreg(sorting_center, output_belt)[0]
        forecast = linreg(sorting_center, output_belt)[1]

        # For each day, calculate the squared deviation
        for day in range(len(forecast)):
            actual = test[day]
            forecast_value = forecast[day]

            squared_deviation = (actual - forecast_value) ** 2
            absolute_deviation = np.abs(actual-forecast_value)

            # If day not in dictionary, add empty list
            if day not in daily_errors:
                daily_errors[day] = {}
                daily_errors[day]['mse'] = []
                daily_errors[day]['mae'] = []
                

            daily_errors[day]['mse'].append(squared_deviation)
            daily_errors[day]['mae'].append(absolute_deviation)
            

    # Calculate for each day the average squared deviation
    for day in range(days):
        if day in daily_errors and len(daily_errors[day]) > 0:  # Check if there are errors recorded
            mse = sum(daily_errors[day]['mse']) / number_of_output_belts
            mae = sum(daily_errors[day]['mae']) / number_of_output_belts
            daily_mse[day] = mse
            daily_mae[day] = mae
        else:
            daily_mse[day] = 0 

    MSE = sum(daily_mse.values()) / days
    MAE = sum(daily_mae.values()) / days
    VSE = np.var(list(daily_mse.values()), ddof=1)

    print(f"MSE for {sorting_center}: {MSE}, MAE: {MAE}, VSE: {VSE}")

####
#plot a specific output belt using the linear regression

def plotlinreg(sorting_center, output_belt):
    # Plot the actual vs predicted values
    plt.figure(figsize=(10, 6))

    # Plot actual values
    plt.plot(linreg(sorting_center, output_belt)[2], linreg(sorting_center, output_belt)[0], label='Actual Values', color='blue', marker='o')

    # Plot predicted values
    plt.plot(linreg(sorting_center, output_belt)[2], linreg(sorting_center, output_belt)[1], label='Predicted Values', color='red', linestyle='--', marker='x')

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Actual vs Predicted Values Over Time')
    plt.xticks(rotation=45)
    plt.legend()

    # Show plot
    plt.tight_layout()
    plt.show()
    
plotlinreg('VANTAA',16)