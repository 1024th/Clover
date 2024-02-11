Grammar_tutorial = "Dafny Grammar tutorial: Map Comprehension Expression (grammar)\
Examples:\
map x : int | 0 <= x <= 10 :: x * x;\
map x : int | 0 <= x <= 10 :: -x := x * x;\
function square(x : int) : int { x * x }\
method test()\
{\
  var m := map x : int | 0 <= x <= 10 :: x * x;\
  ghost var im := imap x : int :: x * x;]\
  ghost var im2 := imap x : int :: square(x);}\
    Iterating over the contents of a map uses the component sets: Keys, Values, and Items. The iteration loop follows the same patterns as for sets:\
method m<T(==),U(==)> (m: map<T,U>) {\
  var items := m.Items;\
  while items != {}\
    decreases |items|\
  {\
    var item :| item in items;\
    items := items - { item };\
    print item.0, " ", item.1, "";}\
}"

SYS_DAFNY = "You are an expert in Dafny. \
You will be given tasks dealing with Dafny programs including precise docstrings and annotations.\n"

GEN_BODY_FROM_SPEC = Grammar_tutorial + "Given an empty Dafny program with function head and specifications.\
You are asked to generate the full Dafny code so that it can be verified by Dafny with the given specification. \
Please return the whole program.\
If loop is needed, use while instead of for. \
Do not use helper functions. \
Do not modify the function signature and specifications. Do not explain.\
Below is the function head with specifications:\n"

GEN_DOC_FROM_BODY = "Given a Dafny program. \
Please return an detailed docstring of the given dafny code's complete functional behavior. \
Do not mention implementation details. Mention 'assert' as preconditions in the docstring. Deduce postconditions. \
Describe every detail. Please only return the docstring. Do not explain.\
Below is the Dafny program:\n"

GEN_BODY_FROM_DOC = Grammar_tutorial + "Given a docstring and the function signature for a Dafny program. \
Please return a Dafny program that implements the functionality described in the docstring. \
If loop is needed, use while instead of for. \
Please only return the Dafny program. Do not explain.\
Below is the docstring and the function signature:\n"

GEN_DOC_FROM_SPEC = "Given the function signature and its specifications for a Dafny program. \
Please return a short and concise docstring of the functional behavior implied by the specifications. \
Do not mention implementation details. \
Please only return the docstring. Do not explain.\
Below is the Dafny signature and its specifications:\n"

GEN_SPEC_FROM_DOC = "Given the function signature and its docstring for a Dafny program. \
Please return the function signature along with specifications include pre- and post- conditions. \
Put one condition in one line. \
Do not return the docstring and the function implementation. Do not use helper functions. Use abs for absolute value. Do not explain.\
Below is the docstring and function signature:\n"

DOC_EQUIV = "Determine if two docstrings can describe the same functional behavior of a dafny program. return YES or NO, and then explain.\n"


if __name__ == "__main__":
    print(SYS_GEN_BODY)
    print(GEN_BODY_FROM_SPEC)
