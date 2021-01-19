## Decision Models 

## FCM and ARV implementation in Python and NumPy

Implement Fuzzy Consensus Model (FCM) and Average Rating Values (ARV) algorithm as a Python
program.

Requests:

1. The input for the program is represented by a set of text files (CSV format) containing fuzzy
    preference relation matrices of a given set of experts, a first additional file containing experts’
    names and experts’ weights and a second additional file containing alternatives.
2. Additional input is represented by FCM parameters like maximum number of rounds,
    consensus threshold, lambda1, lambda2, etc.
3. The output of the program is represented by all the results (final and intermediate) offered by
    FCM (consensus building) and ARV (ranking).
4. The program must be interactive for the end-user, thus it should ask for file names and input
    parameters, communicate the consistency of fuzzy preference relation matrices, ask to change
    such matrices along the consistency check or the feedback mechanism, provide results on the
    standard output, etc.
5. The program must work with any number of experts and alternatives.
6. The program must be organized in Python functions (you can reuse common functions written
    for the homework#1).
7. The program must use NumPy (Pandas is not required for this homework).

## Test cases

Provide also two sets of input (files and other info) to test your program:

1. A first example that does not require the feedback mechanism
2. A second example that requires the feedback mechanism

In at least one of the above test cases, please demonstrate that the consistency check works well.
Provide also a text document in which all the steps to execute your code are described in details and
the test cases are explained and documented.

## Python tools

- Use NumPy to handle all vector-based structures and operations.
- Use Spyder (in the Anaconda package) to write the program. You must create a Spyder
    Project.

## Submission

- Send the solution files (in the Spyder Project – including the text document) to the teacher by
    using Microsoft Teams (Activity).

# Happy coding!
