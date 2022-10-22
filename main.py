from typer import Typer, Option
import typer
from prob_sat import Inst
from prob_sat import ProbSat
import numpy as np

app = Typer()


def main(
    file: str,
    max_tries: int = Option(300, "-T"),
    max_flips: int = Option(5, "-i"),
):
    inst = Inst.from_dimacs(file)
    solver = ProbSat(max_tries, max_flips)
    sol = solver.solve(inst)
    print(solver.metadata["tries"], max_tries * max_flips)
    print_sol_as_cnfsol(sol)


def print_sol_as_cnfsol(sol: np.array):
    var_names = np.arange(sol.size + 1)[1:]
    var_names[sol == 0] *= -1
    print(" ".join(list(var_names.astype(str))) + " 0")


if __name__ == "__main__":
    typer.run(main)
