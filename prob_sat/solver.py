from .inst import Inst
import numpy as np


class ProbSat(object):
    _max_tries = 300
    _max_flips = 35

    _cm = 0.0
    _cb = 2.3

    metadata = {
        "tries": 0,
    }

    def __init__(self, max_tries: int = 100, max_flips: int = 100, cm=0, cb=2.3):
        self._max_tries = max_tries
        self._max_flips = max_flips
        self._cm = cm
        self._cb = cb

    def solve(self, inst: Inst) -> np.array:
        tries_c = 0
        for _ in range(1, self._max_tries + 1):
            rnd_tt = np.round(np.random.uniform(0, 1, size=inst.var_num + 1))
            for i in range(1, self._max_flips + 1):
                tries_c += 1
                sat, unsat = inst.sat_unsat(rnd_tt)
                if unsat == 0:
                    self.metadata["tries"] = tries_c
                    return rnd_tt[1:]
                unsat_clause = inst.pick_rnd_unsat(unsat, rnd_tt)
                var = self._pick_variable(unsat_clause, unsat, sat, rnd_tt, inst)
                rnd_tt[np.abs(var)] = not rnd_tt[np.abs(var)]
        self.metadata["tries"] = self._max_tries

    def _pick_variable(
        self, unsat_clause: np.array, unsat: int, sat: int, tt: np.array, inst: Inst
    ):
        probs = []
        for lit in unsat_clause:
            if lit == 0:
                probs.append(0)
            tt[np.abs(lit)] = not tt[np.abs(lit)]
            new_su = inst.sat_unsat(tt)
            probs.append(self._f((sat, unsat), new_su))
            tt[np.abs(lit)] = not tt[np.abs(lit)]
        prob_arr = np.array(probs)
        prob_arr = prob_arr / sum(prob_arr)
        return np.random.choice(unsat_clause, p=prob_arr)

    def _f(self, old_su, new_su) -> np.float64:
        old_sat, old_unsat = old_su
        new_sat, new_unsat = new_su
        make = np.float64(np.max([new_sat - old_sat, 0]))
        shatter = np.float64(np.max([new_unsat - old_unsat, 0]))
        # make, shatter = new_su
        return make**self._cm / (0.01 + shatter) ** self._cb
