# Libs: 
import random


# ----- Auxiliary functions 

# Function to perform the union operation
def union_listOflists_list(X, o_d):
    # Convert lists to tuples
    X_tuples = set(map(tuple, X))
    o_d_tuple = tuple(o_d)
    
    # Perform the union operation
    result_set = X_tuples | {o_d_tuple}
    
    # Convert the result back to a list of lists
    result = [list(item) for item in result_set]
    
    return result



def o_X(theta, X, g, u):
    """
    This function returns the element o in X that maximizes g(theta, o) 
    subject to the condition that u(theta, o) >= u(theta, o') for all o' in X.
    
    :param g: Function g(θ, o)
    :param X: List of elements
    :param u: Function u(θ, o)
    :param theta: Parameter θ
    
    :return: The element in X that maximizes g(θ, o) under the given condition
    """
    # Finding the element that satisfies the condition on u and maximizes g
    max_element = None
    max_value = float('-inf')
    
    for o in X:
        if all(u(theta, o) >= u(theta, o_prime) for o_prime in X):
            current_value = g(theta, o)
            if current_value > max_value:
                max_value = current_value
                max_element = o
    
    return max_element



def v_X(X, Theta, p, g, u):
    """
    This function computes the value of v(X) given by:
    sum_{theta in Theta} p(theta) * g(theta, o_X(theta))
    
    :param X: List of elements
    :param Theta: List of possible values for theta
    :param p: Probability distribution function over Theta
    :param g: Function g(theta, o)
    :param u: Function u(theta, o)
    
    :return: The computed value of v(X)
    """
    # Compute the sum
    v = sum(p(theta) * g(theta, o_X(theta, X, g, u)) for theta in Theta)
    
    return v



def o_XY(theta, X, Y, O, g, u):
    """
    This function returns the element o in X that maximizes g(theta, o) 
    subject to the condition that u(theta, o) >= u(theta, o') for all o' in X.
    
    :param g: Function g(θ, o)
    :param X: List of elements
    :param u: Function u(θ, o)
    :param theta: Parameter θ
    
    :return: The element in X that maximizes g(θ, o) under the given condition
    """
    # Finding the element that satisfies the condition on u and maximizes g
    max_element = None
    max_value = float('-inf')

    # Convert elements of O and Y to tuples for comparison
    O_tuples = [tuple(o) for o in O]
    Y_tuples = [tuple(y) for y in Y]
    # Compute the difference using list comprehension
    O_minus_Y = [list(o) for o in O_tuples if o not in Y_tuples]
    
    for o in O_minus_Y: 
        if all(u(theta, o) >= u(theta, o_prime) for o_prime in X):
            current_value = g(theta, o)
            if current_value > max_value:
                max_value = current_value
                max_element = o
    
    return max_element




def v_XY(X, Y, O, Theta, p, g, u):
    """
    This function computes the value of v(X) given by:
    sum_{theta in Theta} p(theta) * g(theta, o_X(theta))
    
    :param X: List of elements
    :param Theta: List of possible values for theta
    :param p: Probability distribution function over Theta
    :param g: Function g(theta, o)
    :param u: Function u(theta, o)
    
    :return: The computed value of v(X)
    """
    # Compute the sum
    v = sum(p(theta) * g(theta, o_XY(theta, X, Y, O,  g, u)) for theta in Theta)
    
    return v




# ----- classess for experiments 
class g_class:
    def __init__(self, Theta, O, minimum_value = 0, maximum_value = 100):
        self.Theta = Theta  # A list of elements in Theta
        self.O = O          # A list of lists
        self.values = {}
        for theta in Theta:
            for o in O:
                o_tuple = tuple(o)  # Convert the list o to a tuple for dictionary key
                self.values[(theta, o_tuple)] = random.randint(minimum_value, maximum_value)

    def g(self, theta, o):
        o_tuple = tuple(o)  # Convert the list o to a tuple for lookup
        if (theta, o_tuple) in self.values:
            return self.values[(theta, o_tuple)]
        else:
            raise ValueError("The given theta and o pair is not in the initialized set.")




class u_class:
    def __init__(self, Theta, O, minimum_value = 0, maximum_value = 100):
        self.Theta = Theta  # A list of elements in Theta
        self.O = O          # A list of lists
        self.values = {}
        for theta in Theta:
            for o in O:
                o_tuple = tuple(o)  # Convert the list o to a tuple for dictionary key
                self.values[(theta, o_tuple)] = random.randint(minimum_value, maximum_value)

    def u(self, theta, o):
        o_tuple = tuple(o)  # Convert the list o to a tuple for lookup
        if (theta, o_tuple) in self.values:
            return self.values[(theta, o_tuple)]
        else:
            raise ValueError("The given theta and o pair is not in the initialized set.")
        




# It checks if, for all theta in Theta, there is at least one o in O s.t. u(theta, o) >= 0
# If the above condition is true, it returns True, otherwise False
def check_IR(Theta, X, u):
    check_list = [False for _ in range(len(X))]
    for theta in Theta:
        i = 0
        for o in X:
            if u(theta, o) >= 0:
                check_list[i] = True
            i += 1
    return all(check_list)




# ------  Bartering 
class g_bartering_class:
    def __init__(self, Theta, O, minimum_value = 0, maximum_value = 10):
        self.Theta = Theta  # A list of elements in Theta
        self.O = O          # A list of lists
        self.values = {}
        self.outcome_size = len(O[0])
        for i in range(self.outcome_size):
            self.values[(i)] = random.randint(minimum_value, maximum_value)

    def g(self,theta, o): # in this specific case, g is indepenedent from theta
        if o is None:
            raise ValueError(f"The solution vector 's' must be a list of integers, but got {o}")
        return sum(self.values[i]*(1-o[i]) for i in range(self.outcome_size)) # o[i] = 0 if designer took the item i, 1 otherwise



class u_bartering_class:
    def __init__(self, Theta, O, minimum_value = 0, maximum_value = 10):
        self.Theta = Theta  # A list of elements in Theta
        self.O = O          # A list of lists
        self.values = {}
        self.outcome_size = len(O[0])
        for theta in Theta:
            for i in range(self.outcome_size):
                self.values[(theta, i)] = random.randint(minimum_value, maximum_value)

    def u(self, theta, o):
        return sum(self.values[(theta,i)]*(o[i]) for i in range(self.outcome_size)) # o[i] = 1 if agent took the item i, 0 otherwise



class g_bartering_class_difference:
    def __init__(self, Theta, O, minimum_value = 0, maximum_value = 10, initial_goods = None):
        self.Theta = Theta  # A list of elements in Theta
        self.O = O          # A list of lists
        self.values = {}
        self.outcome_size = len(O[0])
        self.initial_goods = initial_goods
        for i in range(self.outcome_size):
            self.values[i] = random.randint(minimum_value, maximum_value)
        self.initial_values = sum(self.values[i]*(1-self.initial_goods[i]) for i in range(self.outcome_size))
        
    def g(self,theta, o): # in this specific case, g is indepenedent from theta
        current_value = sum(self.values[i]*(1-o[i]) for i in range(self.outcome_size)) 
        return current_value - self.initial_values 


class u_bartering_class_difference:
    def __init__(self, Theta, O, minimum_value = 0, maximum_value = 10, initial_goods = None):
        self.Theta = Theta  # A list of elements in Theta
        self.O = O          # A list of lists
        self.values = {}
        self.initial_values = {}
        self.outcome_size = len(O[0])
        self.initial_goods = initial_goods  
        for theta in Theta:
            for i in range(self.outcome_size):
                self.values[(theta, i)] = random.randint(minimum_value, maximum_value)
        for theta in Theta:
            self.initial_values[theta] = sum(self.values[(theta,i)]*(self.initial_goods[i]) for i in range(self.outcome_size))

    def u(self, theta, o):
        current_value = sum(self.values[(theta,i)]*(o[i]) for i in range(self.outcome_size)) # o[i] = 1 if agent took the item i, 0 otherwise
        return current_value - self.initial_values[theta]
    




# ----- Functions to do the comparison of the three methods 

# -- Brench and bound functions
def find_X(O, Theta, p, o_XY, v_XY, g_instance, u_instance, algorithm = None):
    CB, elapsed_time = algorithm(O, Theta, p, o_XY, v_XY, g_instance.g, u_instance.u)
    model_vX_value = v_X(CB, Theta, p, g_instance.g, u_instance.u)

    semi_random_CB = random.sample(O, len(CB))
    semi_random_vX_value = v_X(semi_random_CB, Theta, p, g_instance.g, u_instance.u)
    if model_vX_value != 0:
        model_vs_rand = round((model_vX_value-semi_random_vX_value)/model_vX_value * 100,2)
    else:
        model_vs_rand = None

    return CB, round(model_vX_value,2), elapsed_time, semi_random_CB, round(semi_random_vX_value,2), model_vs_rand


def check_model_results(CB, g_instance, u_instance, Theta, semi_random_CB):
    outcomeForAllThetas_model = [o_X(theta = theta, X = CB, g = g_instance.g, u = u_instance.u) for theta in Theta]
    gForAllOutcomes_model = [g_instance.g(theta=theta, o=o_model) for theta, o_model in zip(Theta, outcomeForAllThetas_model)]
    uForAllOutcomes_model = [u_instance.u(theta=theta, o=o_model) for theta, o_model in zip(Theta, outcomeForAllThetas_model)]

    outcomeForAllThetas_semiRandom = [o_X(theta = theta, X = semi_random_CB, g = g_instance.g, u = u_instance.u) for theta in Theta]
    gForAllOutcomes_semiRandom = [g_instance.g(theta=theta, o=o_semiRandom) for theta, o_semiRandom in zip(Theta, outcomeForAllThetas_semiRandom)]
    uForAllOutcomes_semiRandom = [u_instance.u(theta=theta, o=o_semiRandom) for theta, o_semiRandom in zip(Theta, outcomeForAllThetas_semiRandom)]

    return gForAllOutcomes_model, uForAllOutcomes_model, gForAllOutcomes_semiRandom, uForAllOutcomes_semiRandom

# -- Ida functions 
def ida_find_X(O, Theta, p, o_XY, v_XY, g_instance, u_instance, L_initial_limit, L_reduction = 0.1, algorithm = None):
    CB, elapsed_time = algorithm(O, Theta, p, o_XY, v_XY, g_instance.g, u_instance.u, L_initial_limit=L_initial_limit, L_reduction = L_reduction)
    model_vX_value = v_X(CB, Theta, p, g_instance.g, u_instance.u)

    semi_random_CB = random.sample(O, len(CB))
    semi_random_vX_value = v_X(semi_random_CB, Theta, p, g_instance.g, u_instance.u)
    if model_vX_value != 0:
        model_vs_rand = round((model_vX_value-semi_random_vX_value)/model_vX_value * 100,2)
    else:
        model_vs_rand = None

    return CB, round(model_vX_value,2), elapsed_time, semi_random_CB, round(semi_random_vX_value,2), model_vs_rand

def ida_check_model_results(CB, g_instance, u_instance, Theta, semi_random_CB):
    outcomeForAllThetas_model = [o_X(theta = theta, X = CB, g = g_instance.g, u = u_instance.u) for theta in Theta]
    gForAllOutcomes_model = [g_instance.g(theta=theta, o=o_model) for theta, o_model in zip(Theta, outcomeForAllThetas_model)]
    uForAllOutcomes_model = [u_instance.u(theta=theta, o=o_model) for theta, o_model in zip(Theta, outcomeForAllThetas_model)]

    outcomeForAllThetas_semiRandom = [o_X(theta = theta, X = semi_random_CB, g = g_instance.g, u = u_instance.u) for theta in Theta]
    gForAllOutcomes_semiRandom = [g_instance.g(theta=theta, o=o_semiRandom) for theta, o_semiRandom in zip(Theta, outcomeForAllThetas_semiRandom)]
    uForAllOutcomes_semiRandom = [u_instance.u(theta=theta, o=o_semiRandom) for theta, o_semiRandom in zip(Theta, outcomeForAllThetas_semiRandom)]

    return gForAllOutcomes_model, uForAllOutcomes_model, gForAllOutcomes_semiRandom, uForAllOutcomes_semiRandom

# -- SLEA functions 

def tuples_to_lists(tuple_list):
    return [list(t) for t in tuple_list]

# Define how to decode a solution vector s into X
def decode_solution(s, O):
    #if not isinstance(s, list) or not all(isinstance(x, int) for x in s):
    #    raise ValueError(f"The solution vector 's' must be a list of integers, but got {s}")
    #if not isinstance(O, list) or not all(isinstance(x, list) for x in O):
    #    raise ValueError(f"The list 'O' must be a list of lists, but got {O}")
    O = tuples_to_lists(O)
    s = list(s)
    decoded = [O[i] for i in range(len(s)) if s[i] == 1]
    #print(f"Decoded solution: {decoded}")  # Debug print
    return decoded


def apply_SLEA(O,population_size, new_population_size,tournament_size,max_evaluations,mutation_rate,Theta,p, g_instance, u_instance, algorithm = None):
    best_solution, best_fitness, elapsed_time = algorithm(
        O=O,n=population_size, new_population_size=new_population_size,tournament_size = tournament_size,max_evaluations=max_evaluations,mutation_rate=mutation_rate,Theta=Theta,p=p, g=g_instance.g,u=u_instance.u
    )

    X = decode_solution(best_solution, O)

    outcomeForAllThetas_model = [o_X(theta = theta, X = X, g = g_instance.g, u = u_instance.u) for theta in Theta]
    gForAllOutcomes_model = [g_instance.g(theta=theta, o=o_model) for theta, o_model in zip(Theta, outcomeForAllThetas_model)]
    uForAllOutcomes_model = [u_instance.u(theta=theta, o=o_model) for theta, o_model in zip(Theta, outcomeForAllThetas_model)]

    return best_solution, best_fitness, elapsed_time, X, gForAllOutcomes_model, uForAllOutcomes_model

