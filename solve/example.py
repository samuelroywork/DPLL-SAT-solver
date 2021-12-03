import sys
import time
import random

# global Datastructures
trail=dict()
clauses = []


#parser function given already
def parse_dimacs():
    with open(sys.argv[1], 'r') as input_file:
        for line in input_file:
            if line[0] in ['c', 'p']:
                continue
            literals = list(map(int, line.split()))
            assert literals[-1] == 0
            literals = literals[:-1]
            clauses.append(literals)


# DPLL Algorithm
def dpll():
    #trail.clear()
    #if not bcp():
     #   return UNSAT()
    while True:
        if not decide():
            return SAT()
        while not bcp():
            if not backtrack():
                return UNSAT()

def decide():
    #print(clauses)
    for clause in clauses:
        for literal in clause:
            var = literal if literal > 0 else -literal
            if var not in trail:
                trail[var]= [False, False]
                return True
    return False

def bcp():
    new_clause = clauses.copy()
    unit_exists, new_clause = unit_prop(new_clause)
    while unit_exists:
        unit_exists, new_clause = unit_prop(new_clause)
        #print(new_clause)
    if unsatisfied(new_clause):
        return False
    return True


def is_unit_is_pos(clause):
    literal_count = 0
    unassigned = 0
    for literal in clause:
        literal_count += 1
        absliteral = abs(literal)
        try:
            var = trail[absliteral]
            if (literal > 0 and var[0]) or (literal < 0 and not var[0]):
                return True
            #else:
                #return False
        except KeyError:
            if unassigned != 0:
                return False
            else:
                unassigned = literal
    if unassigned == 0:
        return False
    variable = unassigned if unassigned > 0 else -unassigned
    value = True if unassigned > 0 else False
    #print(variable, value)
    trail[variable] = [value, True]
    return True


def unit_prop(prop_clauses):
     new_clauses= [clause for clause in prop_clauses if not is_unit_is_pos(clause)]
     #print(new_clauses)
     if len(prop_clauses) > len(new_clauses):
         return True, new_clauses
     return False, new_clauses

def unsatisfied(new_clause):
    for clause in new_clause:
        false_count = 0
        literal_count = 0
        for literal in clause:
            literal_count += 1
            absliteral = literal if literal > 0 else -literal
            try:
                var = trail[absliteral]
                if (literal > 0 and var[0]) or (literal < 0 and not var[0]):
                    break
                else:
                    false_count += 1

            except KeyError:
                break
        if false_count == literal_count:

            return True
    return False


def backtrack():
    while (True):
        if not trail:
            return False
        last=[*trail][-1]
        b=trail.pop(last)
        if not b[1]:
            trail[last] = [not b[0], True]
            return True


def UNSAT():
    print("unsat\n")

    sys.exit(20)

def SAT():
    print("sat\n")

    sys.exit(10)


def main():
	parse_dimacs()
	dpll()


if __name__== "__main__":
    main()
    print(time.process_time())


