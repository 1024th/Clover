Sequence_tutorial = r"""## Dafny sequences

```dafny
method SequenceExample() {
  // Constructing sequences
  var intSeq := [1, 2, 3, 4, 5]; // Sequence of integers
  var boolSeq := [true, false, true]; // Sequence of booleans

  // Accessing elements
  assert intSeq[0] == 1; // Access first element
  assert intSeq[|intSeq|-1] == 5; // Access last element

  // Slicing
  assert intSeq[1..] == [2, 3, 4, 5]; // Slice from index 1 to end
  assert intSeq[..|intSeq|-1] == [1, 2, 3, 4]; // Slice from start to second-last element

  // Concatenation
  var concatSeq := [1, 2] + [3, 4, 5];
  assert concatSeq == [1, 2, 3, 4, 5];

  // Containment
  assert 3 in intSeq; // Check if 3 is in intSeq
  assert 6 !in intSeq; // Check if 6 is not in intSeq

  // Updating (creating a new sequence)
  var updatedSeq := intSeq[2 := 10]; // Create a new sequence with the third element updated to 10
  assert updatedSeq == [1, 2, 10, 4, 5];

  // Converting arrays to sequences
  var arr := new int[5]; // Create an array of 5 integers
  arr[0], arr[1], arr[2], arr[3], arr[4] := 10, 20, 30, 40, 50; // Assign values to the array
  var seqFromArr := arr[..]; // Convert the entire array to a sequence
  assert seqFromArr == [10, 20, 30, 40, 50];

  // Slicing arrays to sequences
  assert arr[1..4] == [20, 30, 40]; // Convert a slice of the array to a sequence
}
```
"""

Array_tutorial = r"""## Dafny arrays

```dafny
type T(0)
function Square(x: int): int { x * x }
method OneDimensionalArrays() {
  // Creating a one-dimensional array
  var a := new T[5]; // Array of type T with length 5
  var b: array<int> := new int[8]; // Array of integers with length 8
  var c: array := new T[9]; // Array of type T with length 9

  // Initializing with values
  b := new int[][1, 2, 3, 4]; // Initialize with ordered list of expressions
  b := new int[5](i => i * i); // Initialize with a function
  b := new int[5](Square); // Initialize with a function name

  // Array length
  assert a.Length == 5; // Length of the array

  // Accessing and updating elements
  var elem := b[2]; // Access element at index 2
  b[3] := 9; // Update element at index 3
}

method MultiDimensionalArrays(m: int, n: int, i: int, j: int, x: int, y: int)
  requires 0 <= i < m && 0 <= j < n && 0 <= x < m && 0 <= y < n
{
  // Creating a two-dimensional array
  var matrix := new T[m, n]; // Array of type T with dimensions m x n

  // Swapping elements
  matrix[i, j], matrix[x, y] := matrix[x, y], matrix[i, j]; // Swap elements

  // Array dimensions
  assert matrix.Length0 == m; // Length of the first dimension
  assert matrix.Length1 == n; // Length of the second dimension

  // Bounds checking
  if 0 <= i < matrix.Length0 && 0 <= j < matrix.Length1 &&
     0 <= x < matrix.Length0 && 0 <= y < matrix.Length1 {
    // Swap is well-formed
  }
}

method ArrayToSequence(a: array<T>, lo: int, hi: int)
  requires a.Length > 0
  requires 0 <= lo <= hi <= a.Length
  ensures a[..] == old(a[..]) // Array is unchanged
{
  // Converting to sequence
  var seq1 := a[lo..hi]; // Subarray conversion to sequence
  var seq2 := a[lo..]; // Drop elements before lo
  var seq3 := a[..hi]; // Take elements up to hi
  var seq4 := a[..]; // Convert entire array to sequence

  // Check if an array contains an element
  var elem := a[0];
  assert elem in a[..]; // Check if elem is in the array
  assume elem in a[..hi]; // Assume elem is in the subarray
}
```
"""

Map_tutorial = r"""## Dafny maps

### Map Comprehension Expression

Examples:

```dafny
map x : int | 0 <= x <= 10 :: x * x;
map x : int | 0 <= x <= 10 :: -x := x * x;
function square(x : int) : int { x * x }
method test()
{
  var m := map x : int | 0 <= x <= 10 :: x * x;
  ghost var im := imap x : int :: x * x;
  ghost var im2 := imap x : int :: square(x);
}
```

### Map Operations

Iterating over the contents of a map uses the component sets: Keys, Values, and Items.
The iteration loop follows the same patterns as for sets:

```dafny
method m<T(==),U(==)> (m: map<T,U>) {
  var items := m.Items;
  while items != {}
    decreases |items|
  {
    var item :| item in items;
    items := items - { item };
    print item.0, " ", item.1, "\n";
  }
}
```
"""

Grammar_tutorial = (
    "# Dafny Grammar tutorial\n\n" +
    Sequence_tutorial + "\n" +
    Array_tutorial + "\n" +
    # Map_tutorial + "\n" +
    "\n\nDafny Grammar tutorial ends here."
)

SYS_DAFNY = "You are an expert in Dafny. \
You will be given tasks dealing with Dafny programs including precise docstrings and specifications.\n"

GEN_BODY_SPEC_FROM_DOC = Grammar_tutorial + "Given a docstring and the function signature for a Dafny program. \
Please return the whole function, including the function signature, specifications, \
and the body that implements the functionality described in the docstring. \
If loop is needed, use while instead of for. \
Exclude 'requires true', 'requires array!=null', 'requires natural number >= 0'. \
Do not modify the function signature. Directly return the Dafny program without any explanation. \
Below is the docstring and the function signature:\n"

GEN_BODY_FROM_SPEC = Grammar_tutorial + "Given an empty Dafny program with function head and specifications, \
you are asked to generate the full Dafny code so that it can be verified by Dafny with the given specification. \
Please return the whole program. \
If loop is needed, use while instead of for. \
Do not use helper functions. \
Do not modify the function signature and specifications. Directly return the Dafny program without any explanation. \
Below is the function head with specifications:\n"

GEN_DOC_FROM_BODY = "Given a Dafny program. \
Please return an detailed docstring of the given dafny code's complete functional behavior. \
Do not mention implementation details. Mention 'assert' as preconditions in the docstring. Deduce postconditions. \
Describe every detail. Please only return the docstring. Do not explain. \
Below is the Dafny program:\n"

GEN_BODY_FROM_DOC = Grammar_tutorial + "Given a docstring and the function signature for a Dafny program. \
Please return a Dafny program that implements the functionality described in the docstring. \
If loop is needed, use while instead of for. \
Please only return the Dafny program. Do not explain. \
Below is the docstring and the function signature:\n"

GEN_DOC_FROM_SPEC = "Given the function signature and its specifications for a Dafny program. \
Please return a short and concise docstring of the functional behavior implied by the specifications. \
The specifications are the 'requires', 'ensures', and 'modifies' clauses. \
The hints from method name and variable names should not be considered as part of the specification. \
Return 'No specifications' if no specifications are found. \
Do not add any additional information that is not in the specifications. \
Do not mention implementation details. \
Please only return the docstring. Do not explain. \
Below is the Dafny signature and its specifications:\n"

GEN_SPEC_FROM_DOC = "Given the function signature and its docstring for a Dafny program. \
Please return the function signature along with specifications include pre- and post- conditions. \
Put one condition in one line. \
Do not return the docstring and the function implementation. Do not use helper functions. Use abs for absolute value. \
Do not explain. \
Below is the docstring and function signature:\n"

DOC_EQUIV = "Determine if two docstrings describe the same functional behavior of a dafny program \
and the second docstring contains all the information in the first docstring. \
Leaving out any information from the first docstring is considered a mismatch. \
Return YES or NO, and then explain the reason.\n"


if __name__ == "__main__":
    print(Grammar_tutorial)
    print(GEN_BODY_FROM_SPEC)
