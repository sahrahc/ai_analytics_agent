from rapidfuzz import fuzz
from state import GraphState

# -----------------------------------
# Identify relevant metrics based on user query and available metric list
#
# TODO: use more advanced techniques like embedding similarity
# -----------------------------------


def identify_metrics(analysis_request: str, metrics: list):

    if metrics is None:
        raise Exception("Metrics not found in state.")

    scores = []

    for metric in metrics:

        score = fuzz.token_sort_ratio(analysis_request, metric["metric_name"])

        scores.append((score, metric))

    # TODO: could be returning more than one top scoring metric in the future based on similarity
    return {"target_metric": max(scores, key=lambda x: x[0])[1]}
