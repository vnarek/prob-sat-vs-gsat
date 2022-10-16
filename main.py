from prob_sat import Inst
from prob_sat import ProbSat

if __name__ == "__main__":
    inst = Inst.from_dimacs("sample_dimacs")
    solver = ProbSat()
    print(solver.solve(inst))
