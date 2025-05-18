"""
I had most of my data saved in this mobile app called "Strong"
and I want to to be able to add this to my database of informations    
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def filter_and_visualize_progress(df, exercise_name):
    # Filter for Bench Press (Barbell) exercise
    bench_press_df = df[df["Exercise Name"] == exercise_name]

    # Calculate estimated 1RM using the Epley formula: 1RM = Weight * (1 + Reps/30)
    bench_press_df["Estimated 1RM"] = bench_press_df["Weight"] * (
        1 + bench_press_df["Reps"] / 30
    )

    # Convert 'Date' to datetime
    bench_press_df["Date"] = pd.to_datetime(bench_press_df["Date"])

    # Get the maximum 1RM per workout session
    max_1rm_per_day = (
        bench_press_df.groupby(bench_press_df["Date"].dt.date)["Estimated 1RM"]
        .max()
        .reset_index()
    )

    # Plotting the progress over time
    plt.figure(figsize=(10, 6))
    plt.plot(
        max_1rm_per_day["Date"],
        max_1rm_per_day["Estimated 1RM"],
        marker="o",
        linestyle="-",
        color="b",
    )
    plt.title(f"{exercise_name} 1RM Progress Over Time")
    plt.xlabel("Date")
    plt.ylabel("Estimated 1RM (lbs)")
    plt.grid(True)

    # Improve date formatting on x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()

    plt.tight_layout()
    plt.show()


# Load the CSV file to inspect its structure
file_path = "strong.csv"
df = pd.read_csv(file_path)

# Display the first few rows and column names to understand the data
df.head(), df.columns
filter_and_visualize_progress(df, "Bench Press (Barbell)")
filter_and_visualize_progress(df, "Triceps Extension (Cable)")
filter_and_visualize_progress(df, "Squat (Barbell)")
filter_and_visualize_progress(df, "Incline Curl (Dumbbell)")
