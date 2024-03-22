import os

from main import Result, Results


def print_result(id: str, result: Result):
    print("=" * 80)
    print(f"ID={id}")
    print(f"verify_success={result.verify_success}, reconstruct_success={result.reconstruct_success}")
    for trace in result.trace:
        print(f"{trace['role']}: {trace['content']}")
    print()


if __name__ == "__main__":
    file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../output/clover_mbpp_dfy50_results.json")
    with open(file, "r") as f:
        data = f.read()
    res = Results.model_validate_json(data)
    for id, r in res.root.items():
        if not r.verify_success or not r.reconstruct_success:
            print_result(id, r)
