from collections import defaultdict
import numpy as np


def _is_satisfied(clause: np.array, tt: np.array):
    for lit in clause:
        if lit == 0:
            continue
        assignment = tt[int(abs(lit))]
        if lit < 0 and assignment == 0 or lit > 0 and assignment == 1:
            return True
    return False


class Inst(object):
    def __init__(self, var_num: int, clause_num: int):
        self.clauses = np.empty((clause_num, 3), dtype=int)
        self.table_t = defaultdict()
        self.var_num = var_num

    def sat_unsat(self, tt: np.array) -> tuple[int, int]:
        sat = 0
        unsat = 0
        for cl in self.clauses:
            satisfied = _is_satisfied(cl, tt)
            if satisfied:
                sat += 1
            else:
                unsat += 1
        return (sat, unsat)

    def pick_rnd_unsat(self, unsat_count: int, tt: np.array) -> np.array:
        ind = np.round(np.random.uniform(1, unsat_count))
        count = 1
        for cl in self.clauses:
            if _is_satisfied(cl, tt):
                continue
            if ind == count:
                return cl
            count += 1

    @classmethod
    def from_dimacs(cls, filename: str):
        inst = None
        count = 0

        with open(filename) as dimacs_f:
            for line in dimacs_f:
                if line[0] == "c":
                    continue
                if line[0] == "p":
                    line = line[2:]
                    sat_format, var_num, clause_num = line.split(" ")
                    if sat_format != "cnf":
                        raise "invalid sat_format"
                    inst = cls(int(var_num), int(clause_num))
                    continue
                if inst is None:
                    raise "expected p row before first clause row"
                line = line.strip()
                if line[-1] == "0":
                    line = line[:-2]
                else:
                    continue
                clause = np.array([int(x) for x in line.split()])
                inst.clauses[count] = np.append(clause, np.zeros(3 - len(clause)))
                count += 1
        return inst
