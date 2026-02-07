import re
import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from itertools import accumulate
from IPython.display import clear_output
from sklearn.metrics import mean_squared_error, r2_score

DEFAULT_SIZE = 200

class Tester:
    """
    Evaluates a predictor function against a dataset and visualizes the results.
    Refactored from Week 7 util.py
    """
    def __init__(self, predictor, data, title=None, size=DEFAULT_SIZE):
        self.predictor = predictor
        self.data = data
        self.title = title or self.make_title(predictor)
        self.size = size
        self.titles = []
        self.guesses = []
        self.truths = []
        self.errors = []
        self.colors = []

    @staticmethod
    def make_title(predictor) -> str:
        if hasattr(predictor, "__name__"):
            return predictor.__name__.replace("__", ".").replace("_", " ").title().replace("Gpt", "GPT")
        return "Model Prediction"

    @staticmethod
    def post_process(value):
        if isinstance(value, str):
            value = value.replace("$", "").replace(",", "")
            match = re.search(r"[-+]?\d*\.\d+|\d+", value)
            return float(match.group()) if match else 0
        else:
            return value

    def color_for(self, error, truth):
        if truth == 0: return "red"
        if error < 40 or error / truth < 0.2:
            return "green"
        elif error < 80 or error / truth < 0.4:
            return "orange"
        else:
            return "red"

    def run_datapoint(self, i):
        datapoint = self.data[i]
        # Handle different data formats (Week 6/7 items vs general dicts)
        if hasattr(datapoint, "summary"):
            input_text = datapoint.summary
            truth = float(datapoint.price) if hasattr(datapoint, "price") else 0.0
            title_text = f"Item {i}"
        else:
            # Assuming fine-tuning dataset format
            input_text = datapoint.get("prompt", "")
            truth = float(datapoint.get("completion", 0))
            title_text = input_text[:40]

        value = self.predictor(datapoint) # Predictor takes the raw item
        guess = self.post_process(value)
        
        error = abs(guess - truth)
        color = self.color_for(error, truth)
        
        return title_text, guess, truth, error, color

    def chart(self, title):
        df = pd.DataFrame({
            "truth": self.truths,
            "guess": self.guesses,
            "title": self.titles,
            "error": self.errors,
            "color": self.colors,
        })
        
        max_val = float(max(df["truth"].max(), df["guess"].max())) if not df.empty else 100

        fig = px.scatter(
            df, x="truth", y="guess", color="color",
            color_discrete_map={"green": "green", "orange": "orange", "red": "red"},
            title=title, labels={"truth": "Actual Price", "guess": "Predicted Price"},
            width=800, height=600,
        )
        
        # Add y=x line
        fig.add_trace(go.Scatter(
            x=[0, max_val], y=[0, max_val], mode="lines",
            line=dict(width=2, dash="dash", color="deepskyblue"),
            name="Perfect Prediction"
        ))
        fig.show()

    def run(self):
        print(f"Running evaluation on {min(len(self.data), self.size)} items...")
        for i in range(min(len(self.data), self.size)):
            title, guess, truth, error, color = self.run_datapoint(i)
            self.titles.append(title)
            self.guesses.append(guess)
            self.truths.append(truth)
            self.errors.append(error)
            self.colors.append(color)
        
        self.chart(self.title)

def evaluate(function, data, size=DEFAULT_SIZE):
    Tester(function, data, size=size).run()
