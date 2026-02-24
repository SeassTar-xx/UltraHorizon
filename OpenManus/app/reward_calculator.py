# Reward Calculation Module
# This module handles the calculation of rewards for the agentic RL project.

import requests
import yaml

class RewardCalculator:
    def __init__(self, weights=None):
        """
        Initialize the reward calculator with default weights.
        :param weights: A dictionary containing weights for each reward dimension (C, N, L, P).
        """
        self.weights = weights or {'C': 0.25, 'N': 0.25, 'L': 0.25, 'P': 0.25}
        self.step_penalty = -0.05
        self.end_penalty = -25

    def calculate_step_reward(self, scores):
        """
        Calculate the reward for a single step.
        :param scores: A dictionary containing scores for each reward dimension (C, N, L, P).
        :return: The calculated reward for the step.
        """
        reward = sum(self.weights[dim] * scores.get(dim, 0) for dim in self.weights)
        reward += self.step_penalty
        return reward

    def calculate_total_reward(self, trajectory_rewards, submitted):
        """
        Calculate the total reward for a trajectory.
        :param trajectory_rewards: A list of rewards for each step in the trajectory.
        :param submitted: A boolean indicating whether the result was submitted.
        :return: The total reward for the trajectory.
        """
        total_reward = sum(trajectory_rewards)
        if not submitted:
            total_reward += self.end_penalty
        return total_reward

    def set_weights(self, new_weights):
        """
        Update the weights for the reward dimensions.
        :param new_weights: A dictionary containing new weights for each reward dimension (C, N, L, P).
        """
        self.weights.update(new_weights)

    def fetch_scores_from_judge(self, step_data):
        """
        Fetch scores for a step from the LLM-judge API.
        :param step_data: A dictionary containing the step data to be evaluated.
        :return: A dictionary with scores for each reward dimension (C, N, L, P).
        """
        with open("judge_config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)

        api_key = config.get("api_key")
        base_url = config.get("base_url")
        model = config.get("model")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "input": step_data
        }

        response = requests.post(f"{base_url}/score", headers=headers, json=payload)

        if response.status_code == 200:
            return response.json().get("scores", {})
        else:
            raise Exception(f"Failed to fetch scores: {response.status_code}, {response.text}")

    def calculate_step_reward_with_judge(self, step_data):
        """
        Calculate the reward for a single step using LLM-judge scores.
        :param step_data: A dictionary containing the step data to be evaluated.
        :return: The calculated reward for the step.
        """
        scores = self.fetch_scores_from_judge(step_data)
        return self.calculate_step_reward(scores)

# Future GRPO interface can be added here.