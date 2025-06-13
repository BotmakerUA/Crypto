# Machine learning module for NapalmProBotV2
# Provides simple logistic regression model to predict trade outcome

from dataclasses import dataclass
from typing import List
import numpy as np
from sklearn.linear_model import LogisticRegression

@dataclass
class TradeRecord:
    features: List[float]
    result: int  # 1 for win, 0 for loss

class MachineLearningAgent:
    def __init__(self):
        self.records: List[TradeRecord] = []
        self.model = LogisticRegression()
        self.trained = False

    def add_record(self, features: List[float], result: int):
        """Store trade outcome for training later."""
        self.records.append(TradeRecord(features, result))

    def train(self):
        """Train the logistic regression model on collected records."""
        if len(self.records) < 10:
            return
        X = np.array([r.features for r in self.records])
        y = np.array([r.result for r in self.records])
        self.model.fit(X, y)
        self.trained = True

    def predict(self, features: List[float]) -> float:
        """Return probability of a winning trade."""
        if not self.trained:
            return 0.5
        prob = self.model.predict_proba([features])[0][1]
        return float(prob)
