# models/anomaly_engine.py
import numpy as np
from sklearn.ensemble import IsolationForest

class SpendingAnomalyEngine:
    """ML engine using Isolation Forest to detect abnormal spending spikes."""
    def __init__(self):
        # contamination=0.1 assumes roughly 10% of entries might be unusual spending spikes
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False

    def train_and_check(self, historical_amounts: list, current_amount: float) -> bool:
        """
        Trains on past amounts and predicts if the current amount is an anomaly.
        Returns True if it's an anomaly, False otherwise.
        """
        if len(historical_amounts) < 4:
            # Fallback rule if there isn't enough historical data yet
            if historical_amounts and current_amount > (np.mean(historical_amounts) * 2):
                return True
            return False

        # Reshape for scikit-learn (expects a 2D array: [[val1], [val2], ...])
        X = np.array(historical_amounts).reshape(-1, 1)
        self.model.fit(X)

        # Predict on the new amount
        prediction = self.model.predict([[current_amount]])
        
        # IsolationForest outputs -1 for anomalies and 1 for normal data points
        return prediction[0] == -1