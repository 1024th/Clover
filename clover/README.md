# Quick Start
Clover APIs in `clover.py`. Run single example:
```
python clover.py  --test-name array_append
```

Run CloverBench Experiments:
```
python exps.py --dafny-path [DAFNY_PATH]
```

# Documentation
## Naming convention:

| Name | Explanation |
| --- | --- |
| spec | specifications right after the function head |
| annotation | specification + all annotations in the code |
| code | implementation only (no annotations) |
| body | implementation + annotation in the code (no specification) |
| doc | doc string |
