import argparse
import os
import typing

import mbpp_dataset
import prompts
import pydantic
import sglang
from sglang import OpenAI, assistant, gen, set_default_backend, system, user
from sglang.lang.interpreter import ProgramState
from utils import (
    extract_code_from_llm_output,
    extract_spec,
    is_dafny_verified,
    no_compile_error,
    run_dafny,
    stream_print,
    mask_method_name,
    mask_comments,
    remove_empty_lines,
    extract_docstring_from_llm_output
)


@sglang.function
def gen_doc_from_spec(s: ProgramState, spec):
    s += system(prompts.SYS_DAFNY)
    s += user(prompts.GEN_DOC_FROM_SPEC + spec)
    s += assistant(gen("new_doc", max_tokens=512))
    s["new_doc"] = extract_docstring_from_llm_output(s["new_doc"])
    return s["new_doc"]


@sglang.function
def ask_llm_equiv_test_doc(s: ProgramState, doc, new_doc, head):
    with s.user():
        s += prompts.DOC_EQUIV
        s += "Below is the signature of the Dafny program:\n" + head + "\n"
        s += "Below is the first docstring:\n" + doc + "\n"
        s += "Below is the second docstring:\n" + new_doc + "\n"
    s += assistant(gen("doc_equiv", max_tokens=256))
    return "YES" in s["doc_equiv"]


@sglang.function
def gen_body_spec_from_doc(
    s: ProgramState, doc: str, method_signature: str, feedback_turn=3
):
    s += system(prompts.SYS_DAFNY)
    s += user(prompts.GEN_BODY_SPEC_FROM_DOC + doc + "\n" + method_signature)
    for i in range(feedback_turn):
        name = f"gen_body_spec_try{i}"
        s += assistant(gen(name, max_tokens=1024))
        code = extract_code_from_llm_output(s[name])
        out = run_dafny(code)
        if no_compile_error(out) and is_dafny_verified(out):
            return code
        with s.user():
            s += "This answer got Dafny compile error:\n" + out + "\n"
            s += "Please try again by taking the Dafny compiler feedback."
    return ""


class Result(pydantic.BaseModel):
    verify_success: bool
    reconstruct_success: bool
    code: str = ""
    trace: typing.List = []


class Results(pydantic.RootModel):
    root: typing.Dict[str, Result] = {}


def clover_mbpp(
    task: mbpp_dataset.Task,
    old_results: typing.Optional[Result] = None,
    feedback_turn=3,
    num_trial=1,
    run_generation=True,
    run_reconstruction=True,
    verbose=0,
) -> Result:
    docstring = task.task_description
    signature = task.specification.method_signature
    if old_results:
        res = old_results
    else:
        res = Result(verify_success=False, reconstruct_success=False)

    # Doc -> spec + code
    if run_generation:
        s = gen_body_spec_from_doc(
            docstring, signature, feedback_turn=feedback_turn,
            stream=(verbose >= 2)
        )
        if verbose >= 2:
            stream_print(s)
        res.code = str(s.ret_value)
        res.trace += s.messages()
        res.verify_success = bool(res.code)
        if not res.verify_success:
            return res

    # Spec -> doc reconstruction
    if run_reconstruction:
        spec = extract_spec(res.code)
        spec = remove_empty_lines(mask_method_name(mask_comments(spec)))
        if verbose >= 1:
            print(f"spec: {spec}")
        for k in range(num_trial):
            s = gen_doc_from_spec(spec, stream=(verbose >= 2))
            if verbose >= 2:
                stream_print(s)
            new_doc = str(s.ret_value)
            res.trace += s.messages()
            s = ask_llm_equiv_test_doc.run(
                docstring, new_doc, signature, stream=(verbose >= 2)
            )
            if verbose >= 2:
                stream_print(s)
            res.reconstruct_success = bool(s.ret_value)
            res.trace += s.messages()
            if res.reconstruct_success:
                break
            if verbose >= 1:
                print(f"Reconstruction failed for trial {k}")
        if not res.reconstruct_success:
            return res

    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", type=int, default=1)
    parser.add_argument("--load-path", type=str, default="",
                        help="Load the previous results json file")
    parser.add_argument("--save-path", type=str, default="",
                        help="Save the results json file")
    parser.add_argument("--early-quit", action="store_true")
    parser.add_argument("--dafny-path", type=str, default="dafny")
    parser.add_argument("--reconstruction-only", type=bool, default=False)
    parser.add_argument("--feedback-turn", type=int, default=3)
    parser.add_argument("--num-trial", type=int, default=1)
    args = parser.parse_args()

    if not args.save_path:
        args.save_path = "../output/clover_mbpp_dfy50_results.json"
        args.save_path = os.path.join(
            os.path.dirname(__file__), args.save_path)
    print(f"Save path: {args.save_path}")
    input()

    # backend = OpenAI("gpt-3.5-turbo")
    # backend = OpenAI("gpt-4")
    set_default_backend(OpenAI("gpt-4-1106-preview"))
    # set_default_backend(OpenAI("gpt-4"))

    dataset = mbpp_dataset.load_dataset()
    if args.load_path:
        with open(args.load_path, "r") as f:
            data = f.read()
        results = Results.model_validate_json(data)
    else:
        results = Results()

    sorted_dataset = sorted(dataset.root.items(), key=lambda x: int(x[0]))
    for id, task in sorted_dataset:
        if args.reconstruction_only:
            if id not in results.root or not results.root[id].verify_success:
                print(f"Skipping task: {id}")
                continue
        else:
            if id in results.root and results.root[id].verify_success:
                print(f"Skipping task: {id}")
                continue
        print(f"Processing task: {id}")
        res = clover_mbpp(
            task=task,
            old_results=results.root.get(id),
            feedback_turn=args.feedback_turn, num_trial=args.num_trial,
            run_generation=not args.reconstruction_only,
            verbose=args.verbose)
        results.root[id] = res
        with open(args.save_path, "w") as f:
            f.write(results.model_dump_json(indent=2))
