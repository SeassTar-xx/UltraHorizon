import json

SEQ_JUDGE_PROMPT = """
You are an expert evaluator tasked with scoring agent actions in the Sequence Exploration Environment. Your role is to assess the agent's performance based on four reward dimensions: Complementarity (C), Negation (N), Consistency (L), and Progress (P). Follow the scoring criteria strictly and provide detailed feedback.

Your job is:
1. Analyze the agent's actions, outputs, and historical trajectory for each step.
2. Evaluate the actions based on the following reward dimensions:
   - Complementarity (C): Did the agent introduce new information or constraints?
     - -5: Completely repetitive
     - 0: Minimal or no change
     - 0.3: Noticeable but weak change
     - 0.6: Clear addition of intermediate conclusions or constraints
     - 1: Strong new constraints
   - Negation (N): Did the agent negate previous steps?
     - 0: No negation
     - 0.3: Weak or ambiguous negation
     - 0.6: Clear negation of one reasonable hypothesis
     - 1: Clear negation of multiple reasonable hypotheses
   - Consistency (L): Did the agent avoid contradictions?
     - -5: Clear errors or contradictions
     - 0: Weak or inconsistent logic
     - 0.3: Basic reasoning
     - 0.6: Reasonable logic
     - 1: Clear and consistent reasoning
   - Progress (P): Did the agent make progress toward solving the task?
     - -5: Off-topic or irrelevant
     - 0: No progress
     - 1: Weak progress
     - 2: Clear progress
     - 3: Strong progress or near solution
3. Provide scores for each dimension in the following format:
{
  "step_number": <step_number>,
  "scores": {
    "C": <score>,
    "N": <score>,
    "L": <score>,
    "P": <score>
  },
  "feedback": "<detailed_feedback>"
}

Be precise and consistent in your evaluations. Ensure that your feedback helps the agent understand its performance and areas for improvement. Include references to the agent's historical trajectory, current state, and actions to justify your scores.

Historical Trajectory: {history}
Current State: {current_state}
Current Action: {action}
"""

def replace_placeholders(seq_env, step_number):
    """
    Replace placeholders in the SEQ_JUDGE_PROMPT with actual values from the SequenceExploreEnvironment.

    :param seq_env: An instance of SequenceExploreEnvironment.
    :param step_number: The step number to extract the current state and action.
    :return: The formatted prompt with placeholders replaced.
    """
    # Extract historical trajectory
    historical_trajectory = json.dumps(seq_env.history, indent=2)

    # Extract current state
    if step_number <= len(seq_env.history):
        current_state = json.dumps(seq_env.history[step_number - 1], indent=2)
    else:
        current_state = "{}"  # Empty state if step_number is out of range

    # Extract current action
    if step_number <= len(seq_env.history):
        current_action = (
            f"Main Input: {seq_env.history[step_number - 1]['main_input']}, "
            f"Vice Input: {seq_env.history[step_number - 1]['vice_input']}"
        )
    else:
        current_action = "No action available"

    # Replace placeholders in the prompt
    formatted_prompt = SEQ_JUDGE_PROMPT.replace("{history}", historical_trajectory)
    formatted_prompt = formatted_prompt.replace("{current_state}", current_state)
    formatted_prompt = formatted_prompt.replace("{action}", current_action)

    return formatted_prompt

# Example usage
# Assuming `env` is an instance of SequenceExploreEnvironment and step_number is the current step
# formatted_prompt = replace_placeholders(env, step_number)
# print(formatted_prompt)