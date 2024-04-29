from typing import List
from agents import MessageHistory
from langchain_core.messages import AIMessage, HumanMessage
import tabulate
import concurrent.futures

def build_message_history_for_test(messages: List[str]) -> MessageHistory:
    """
    Builds a message history in the same form as agents expect.
    This is a list of BaseMessage objects, starting with the first
    message from the user and alternating between user and agent.
    """
    rtn = []
    for i, message in enumerate(messages):
        if i % 2 == 0:
            rtn.append(HumanMessage(message))
        else:
            rtn.append(AIMessage(message))
    return rtn


def run_in_parallel(evaluator, times):
        # Create a list to store the results
        results = []
        responses = []

        # Create a ThreadPoolExecutor with 10 threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=times) as executor:
            for _ in range(times):
                future = executor.submit(evaluator)
                results.append(future)
        # Wait for all the results to complete
        concurrent.futures.wait(results)
        return results


def tabulate_evaluator_results(responses, results):
    table = []
    passed = 0
    for i, result in enumerate(responses):
        score = results[i]["score"]
        reasoning = results[i]["reasoning"]
        if (score < 1.0):
            table.append([result, score, reasoning])
        else:
            passed += 1
        
    print(f"Passed: {passed} out of {len(responses)}")
    print(tabulate.tabulate(table, headers=["Response", "Score", "Rationale"]))
