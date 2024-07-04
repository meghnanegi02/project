import json
from datetime import datetime
import matplotlib.pyplot as plt

# User class
class User:
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.workouts = []
        self.goals = []

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "height": self.height,
            "workouts": [w.to_dict() for w in self.workouts],
            "goals": [g.to_dict() for g in self.goals]
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data['name'], data['age'], data['weight'], data['height'])
        user.workouts = [Workout.from_dict(w) for w in data['workouts']]
        user.goals = [Goal.from_dict(g) for g in data['goals']]
        return user

# Workout class
class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def to_dict(self):
        return {
            "date": self.date,
            "exercise_type": self.exercise_type,
            "duration": self.duration,
            "calories_burned": self.calories_burned
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['date'], data['exercise_type'], data['duration'], data['calories_burned'])

# Goal class
class Goal:
    def __init__(self, description, target):
        self.description = description
        self.target = target
        self.progress = 0

    def to_dict(self):
        return {
            "description": self.description,
            "target": self.target,
            "progress": self.progress
        }

    @classmethod
    def from_dict(cls, data):
        goal = cls(data['description'], data['target'])
        goal.progress = data['progress']
        return goal

# FitnessApp class
class FitnessApp:
    def __init__(self, data_file='fitness_data.json'):
        self.data_file = data_file
        self.users = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.users = [User.from_dict(u) for u in data]
        except FileNotFoundError:
            self.users = []

    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump([u.to_dict() for u in self.users], file)

    def register_user(self, name, age, weight, height):
        user = User(name, age, weight, height)
        self.users.append(user)
        self.save_data()

    def find_user(self, name):
        for user in self.users:
            if user.name == name:
                return user
        return None

    def add_workout(self, user_name, date, exercise_type, duration, calories_burned):
        user = self.find_user(user_name)
        if user:
            workout = Workout(date, exercise_type, duration, calories_burned)
            user.workouts.append(workout)
            self.save_data()

    def update_workout(self, user_name, workout_index, date=None, exercise_type=None, duration=None, calories_burned=None):
        user = self.find_user(user_name)
        if user and 0 <= workout_index < len(user.workouts):
            workout = user.workouts[workout_index]
            workout.date = date if date else workout.date
            workout.exercise_type = exercise_type if exercise_type else workout.exercise_type
            workout.duration = duration if duration else workout.duration
            workout.calories_burned = calories_burned if calories_burned else workout.calories_burned
            self.save_data()

    def delete_workout(self, user_name, workout_index):
        user = self.find_user(user_name)
        if user and 0 <= workout_index < len(user.workouts):
            user.workouts.pop(workout_index)
            self.save_data()

    def set_goal(self, user_name, description, target):
        user = self.find_user(user_name)
        if user:
            goal = Goal(description, target)
            user.goals.append(goal)
            self.save_data()

    def update_goal(self, user_name, goal_index, description=None, target=None, progress=None):
        user = self.find_user(user_name)
        if user and 0 <= goal_index < len(user.goals):
            goal = user.goals[goal_index]
            goal.description = description if description else goal.description
            goal.target = target if target else goal.target
            goal.progress = progress if progress else goal.progress
            self.save_data()

    def delete_goal(self, user_name, goal_index):
        user = self.find_user(user_name)
        if user and 0 <= goal_index < len(user.goals):
            user.goals.pop(goal_index)
            self.save_data()

    def generate_report(self, user_name):
        user = self.find_user(user_name)
        if user:
            total_calories = sum(w.calories_burned for w in user.workouts)
            total_duration = sum(w.duration for w in user.workouts)
            report = {
                "total_calories": total_calories,
                "total_duration": total_duration,
                "goals": [g.to_dict() for g in user.goals]
            }
            return report
        return None

    def generate_summary(self, user_name, period='weekly'):
        user = self.find_user(user_name)
        if user:
            if period == 'weekly':
                date_range = datetime.now() - timedelta(days=7)
            elif period == 'monthly':
                date_range = datetime.now() - timedelta(days=30)
            elif period == 'yearly':
                date_range = datetime.now() - timedelta(days=365)
            else:
                return None

            workouts = [w for w in user.workouts if datetime.strptime(w.date, "%Y-%m-%d") >= date_range]
            total_calories = sum(w.calories_burned for w in workouts)
            total_duration = sum(w.duration for w in workouts)
            summary = {
                "total_calories": total_calories,
                "total_duration": total_duration,
                "workouts": [w.to_dict() for w in workouts]
            }
            return summary
        return None

    def plot_progress(self, user_name):
        user = self.find_user(user_name)
        if user:
            dates = [datetime.strptime(w.date, "%Y-%m-%d") for w in user.workouts]
            calories = [w.calories_burned for w in user.workouts]

            plt.figure(figsize=(10, 5))
            plt.plot(dates, calories, marker='o')
            plt.xlabel('Date')
            plt.ylabel('Calories Burned')
            plt.title('Workout Progress Over Time')
            plt.grid(True)
            plt.show()

# Example usage
if __name__ == "__main__":
    app = FitnessApp()

    # Register a user
    app.register_user("Alice", 30, 70, 165)

    # Log workouts
    app.add_workout("Alice", "2023-07-01", "running", 30, 300)
    app.add_workout("Alice", "2023-07-02", "cycling", 45, 400)

    # Update a workout
    app.update_workout("Alice", 0, duration=35, calories_burned=350)

    # Delete a workout
    app.delete_workout("Alice", 1)

    # Set goals
    app.set_goal("Alice", "Lose 5kg", 5)
    app.set_goal("Alice", "Run 20km a week", 20)

    # Update a goal
    app.update_goal("Alice", 0, progress=2)

    # Delete a goal
    app.delete_goal("Alice", 1)

    # Generate report
    report = app.generate_report("Alice")
    print(report)

    # Generate summary
    summary = app.generate_summary("Alice", 'weekly')
    print(summary)

    # Plot progress
    app.plot_progress("Alice")
