import os

from main import Result, Results


def print_result(id: str, result: Result):
    print("=" * 80)
    print(f"ID={id}")
    print(f"verify_success={result.verify_success}, reconstruct_success={result.reconstruct_success}")
    for trace in result.trace:
        print(f"{trace['role']}: {trace['content']}")
    print()


def print_reconstruct_result(id: str, result: Result):
    print("=" * 80)
    print()
    print(f"ID={id}")
    print(result.code)
    print(f"reconstruct_success={result.reconstruct_success}")
    start = False
    for trace in result.trace:
        if "method foo" in trace["content"]:
            start = True
        if not start:
            continue
        print(f"{trace['role']}: {trace['content']}")
        print()
    print()


if __name__ == "__main__":
    file = "../output/clover_mbpp_dfy50_results.json"
    file = "../output/clover_mbpp_dfy50_feedback10_grammarTutorial.json"
    file = "../output/clover_mbpp_dfy50_reconstruct3.json"
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(file, "r") as f:
        data = f.read()
    res = Results.model_validate_json(data)
    for id, r in res.root.items():
        # if not r.verify_success or not r.reconstruct_success:
        #     print_result(id, r)
        # if r.verify_success and not r.reconstruct_success:
        #     print_reconstruct_result(id, r)
        print_reconstruct_result(id, r)
