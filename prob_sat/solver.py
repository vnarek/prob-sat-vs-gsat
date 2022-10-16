from .inst import Inst
import numpy as np


class ProbSat(object):
    _max_tries = 100
    _max_flips = 100

    _cm = 0.0
    _cb = 2.3

    def __init__(self, max_tries: int = 100, max_flips: int = 100, cm=0, cb=2.3):
        self._max_tries = max_tries
        self._max_flips = max_flips
        self._cm = cm
        self._cb = cb

    def solve(self, inst: Inst) -> np.array:
        for _ in range(1, self._max_tries + 1):
            rnd_tt = np.round(np.random.uniform(0, 1, size=inst.var_num + 1))
            for _ in range(1, self._max_flips + 1):
                sat, unsat = inst.sat_unsat(rnd_tt)
                if unsat == 0:
                    return rnd_tt[1:]
                unsat_clause = inst.pick_rnd_unsat(unsat, rnd_tt)
                var = self._pick_variable(unsat_clause, unsat, sat, rnd_tt, inst)
                rnd_tt[int(np.abs(var))] = not rnd_tt[int(np.abs(var))]
        raise "No satisfying assignment found"

    def _pick_variable(
        self, unsat_clause: np.array, unsat: int, sat: int, tt: np.array, inst: Inst
    ):
        probs = []
        for lit in unsat_clause:
            if lit == 0:
                probs.append(0)
            tt[int(np.abs(lit))] = not tt[int(np.abs(lit))]
            new_su = inst.sat_unsat(tt)
            probs.append(self._f((sat, unsat), new_su))
            tt[int(np.abs(lit))] = not tt[int(np.abs(lit))]
        prob_arr = np.array(probs)
        return np.random.choice(unsat_clause, p=prob_arr / np.sum(prob_arr))

    def _f(self, old_su, new_su) -> np.float64:
        old_sat, old_unsat = old_su
        new_sat, new_unsat = new_su
        make = np.abs(old_unsat - new_sat)
        shatter = np.abs(old_sat - new_unsat)
        return make**self._cm / (0.001 + shatter) ** self._cb
