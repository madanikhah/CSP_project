# from ast import List
# from ast import List
# import os
# import subprocess
import time
# from collections import deque
# from copy import deepcopy
from typing import Optional

from CSP.Problem import Problem
from CSP.Variable import  Variable
from SecretSanta.SecretSantaConstraint import NotEqualConstraint
# from CSP.Constraint import NotEqualConstraint
from typing import List, TypeVar
T = TypeVar('T')


class Solver:

    def __init__(self, problem: Problem, use_mrv=False, use_lcv=False, use_forward_check=False):
        self.problem = problem
        self.use_lcv = use_lcv
        self.use_mrv = use_mrv
        self.use_forward_check = use_forward_check

    def is_finished(self) -> bool:
        return all([x.is_satisfied() for x in self.problem.constraints]) and len(
            self.problem.get_unassigned_variables()) == 0

    def solve(self):
        self.problem.calculate_neighbors()
        start = time.time()
        for var in self.problem.variables:
            if not self.forward_check(var):
                print("Problem Unsolvable")
                return
        result = self.backtracking()
        end = time.time()
        time_elapsed = (end - start) * 1000
        if result:
            print(f'Solved after {time_elapsed} ms')
        else:
            print(f'Failed to solve after {time_elapsed} ms')


    def backtracking(self):
        # pass
        # Write your code here
        if self.is_finished():
            return True

        var = self.select_unassigned_variable()
        if var is None:
            return False

        ordered_values = self.order_domain_values(var)
        for value in ordered_values:
            if self.is_consistent_value(var, value):
                var.value = value
                if self.use_forward_check:
                    inferences = self.forward_check(var)
                    if inferences is not None:
                        result = self.backtracking()
                        if result:
                            return True
                        self.undo_forward_check(inferences)
                else:
                    result = self.backtracking()
                    if result:
                        return True
                var.value = None
        return False


    def forward_check(self, var):
        # pass
        # Write your code here
        inferences = []
        for constraint in self.problem.get_neighbor_constraints(var):
            for neighbor in constraint.variables:
                if not neighbor.has_value:
                    for value in neighbor.domain:
                        if not self.is_consistent_value(neighbor, value):
                            neighbor.domain.remove(value)
                            inferences.append((neighbor, value))
                    if len(neighbor.domain) == 0:
                        return None
        return inferences
    
    def undo_forward_check(self, inferences):
        for var, value in inferences:
            var.domain.append(value)


    def select_unassigned_variable(self) -> Optional[Variable]:
        if self.use_mrv:
            return self.mrv()
        unassigned_variables = self.problem.get_unassigned_variables()
        return unassigned_variables[0] if unassigned_variables else None

    def order_domain_values(self, var: Variable):
        if self.use_lcv:
            return self.lcv(var)
        return var.domain

    def mrv(self) -> Optional[Variable]:
        pass
        # Write your code here

    # def is_consistent(self, var: Variable):
        # pass
        # Write your code here
    def is_consistent_value(self, var: Variable, value: T) -> bool:
        for constraint in self.problem.get_neighbor_constraints(var):
            # new_var = NotEqualConstraint
            if isinstance(constraint, NotEqualConstraint):
                other_var = constraint.variables[0] if constraint.variables[1] is var else constraint.variables[1]
                if other_var.has_value and other_var.value == value:
                    return False
        return True




    # def lcv(self, var: Variable):
        # pass
        # Write your code here
    
def lcv(self, var: Variable)-> List:
    value_counts = {value: 0 for value in var.domain}
    for constraint in self.problem.get_neighbor_constraints(var):
        for neighbor in constraint.variables:
            if neighbor.has_value:
                for value in var.domain:
                    if not self.is_consistent_value(var, value):
                        value_counts[value] += 1

        sorted_values = sorted(var.domain, key=lambda value: value_counts[value])
    return sorted_values
    # def lcv(self, var: Variable):
        # pass


