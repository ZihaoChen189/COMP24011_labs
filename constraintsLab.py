#!/usr/bin/env python3
from constraint import Problem, AllDifferentConstraint, ExactSumConstraint


# Task 1    
def Travellers(List):
    # According to the coursework instruction, the specific precondition was provided.
    problem = Problem()
    people = ["claude", "olga", "pablo", "scott"]
    times = ["2:30", "3:30", "4:30", "5:30"]
    destinations = ["peru", "romania", "taiwan", "yemen"]
    t_variables = list(map(lambda x: "t_" + x, people))
    d_variables = list(map(lambda x: "d_" + x, people))
    problem.addVariables(t_variables, times)
    problem.addVariables(d_variables, destinations)
    problem.addConstraint(AllDifferentConstraint(), t_variables)
    problem.addConstraint(AllDifferentConstraint(), d_variables)
    # The first constraint was ignored.
    # 1. Olga is leaving 2 hours before the traveller from Yemen.
    # for person in people:
    #     problem.addConstraint(
    #         (lambda x, y, z: (y != "yemen") or
    #         ((x == "4:30") and (z == "2:30")) or
    #          ((x == "5:30") and (z == "3:30"))),
    #         ["t_" + person, "d_" + person, "t_olga"])
     
    # 2. Claude is either the person leaving at 2:30 pm or the traveller leaving at 3:30 pm.
    problem.addConstraint((lambda x: (x == "2:30") or (x == "3:30")), ["t_claude"])
    
    # 3. The person leaving at 2:30 pm is flying from Peru.
    for person in people:
        problem.addConstraint(
            (lambda x, y: (x != "2:30") or
             (y == "peru")),
            ["t_" + person, "d_" + person])

    # 4. The person flying from Yemen is leaving earlier than the person flying from Taiwan.
    for i in range(len(people)):
        for j in range(len(people)):
            problem.addConstraint(
                (lambda t1, t2, d1, d2:
                 (d1 != "yemen" or d2 != "taiwan") or
                  (d1 == "yemen" and d2 == "taiwan" and t1 < t2)),
                ["t_" + people[i], "t_" + people[j], "d_" + people[i], "d_" + people[j]])
        
    # 5. The four travellers are Pablo, the traveller flying from Yemen, the person leaving at 2:30 pm
    # and the person leaving at 3:30 pm.
    for person in people:
        problem.addConstraint(
            (lambda x, y, z1, z2:
              (z2 != "yemen" and z1 != "2:30" and z1 != "3:30") or
              ((x == "2:30" or x == "3:30") and y != "Yemen")),
            ["t_" + person, "d_" + person, "t_pablo", "d_pablo"])
    
    # Add the constraint from the parameter of List.
    for element in List:
        problem.addConstraint((lambda x: (x == element[1])), ["t_" + element[0]])
    
    solns = problem.getSolutions() 
    return solns


# Task 2
def CommonSum(n):
    sum = n**2*(n**2+1)/2/4
    return sum


# Task 3
def msqList(m, pairList):
    # According to the coursework instruction, the specific precondition was provided.
    problem = Problem()
    problem.addVariables(range(0, m*m), range(1, m*m+1))
    problem.addConstraint(AllDifferentConstraint(), range(0, m*m))
    for row in range(m):
        problem.addConstraint(ExactSumConstraint(CommonSum(m)),
                              [row*m+i for i in range(m)])
    # Following the style of the row constraint, other constraints were designed.
    for col in range(m):
        problem.addConstraint(ExactSumConstraint(CommonSum(m)),
                              [col+m*i for i in range(m)])
        
    problem.addConstraint(ExactSumConstraint(CommonSum(m)),
                          [i*m+i for i in range(m)])
    
    problem.addConstraint(ExactSumConstraint(CommonSum(m)),
                          [i*m-i for i in range(1, m+1)])

    # Add the constraint from the parameter of List.
    for element in pairList:
        problem.addConstraint((ExactSumConstraint(element[1])), [element[0]])
        
    solns = problem.getSolutions()  
    return solns


# Task 4
# These two functions helped to catch every broken diagonal together.
def get_diag1(m, k):
    L1 = []
    for i in range(k, m):
        L1.append(i*m+i-k)
    L2 = []
    k1 = m-k
    for i in range(m-k1):
        L2.append(i*m+i+k1)
    L = L1 + L2
    return L


def get_diag2(m, k):
    L1 = []
    for i in range(1, m+1-k):
        L1.append(i*m-i-k)
    L2 = []
    k1 = m-k
    for i in range(k1+1, m+1):
        L2.append(i*m-i+k1)
    L = L1 + L2
    return L


def pmsList(m, pairList):
    # The front part was same as the task3.
    problem = Problem()
    problem.addVariables(range(0, m*m), range(1, m*m+1))
    problem.addConstraint(AllDifferentConstraint(),range(0, m*m))
    for row in range(m):
        problem.addConstraint(ExactSumConstraint(CommonSum(m)),
                              [row*m+i for i in range(m)])
    for col in range(m):
        problem.addConstraint(ExactSumConstraint(CommonSum(m)),
                              [col+m*i for i in range(m)])
    problem.addConstraint(ExactSumConstraint(CommonSum(m)),
                          [i*m+i for i in range(m)])
    problem.addConstraint(ExactSumConstraint(CommonSum(m)),
                          [i*m-i for i in range(1, m+1)])

    # Add the constraint from the parameter of List.
    for element in pairList:
        problem.addConstraint((ExactSumConstraint(element[1])), [element[0]])
    
    # The key algorithm of this file was here, under the help of the specific library, the constraints with the broken diagonals were created.
    for k in range(1, m):
        diag1 = get_diag1(m, k)
        problem.addConstraint(ExactSumConstraint(CommonSum(m)), diag1)
        diag2 = get_diag2(m, k)
        problem.addConstraint(ExactSumConstraint(CommonSum(m)), diag2)

    solns = problem.getSolutions() 
    return solns


# Debug
if __name__ == '__main__':
    print("debug run...")
