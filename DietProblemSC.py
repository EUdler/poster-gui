import scipy.optimize as sopt
import numpy as np

food_names = ["broccoli", "apple", "oatmeal coockie", "milk", "chicken", "omelette"]

# List of nutritional parameters - see more on Excel spreadsheet/NutritionFacts
parameters = ["cost", "fat", "vitA", "vitC", "protein", "calories", "carbohidrates", "calcium"]

foods = {'fat': [0.80, 0.50, 3.3, 4.7, 10.8, 7.3],
         'vitA': [70.0, 73.10, 2.9, 100, 77.4, 409.2],
         'vitC': [160.20, 7.90, 0.1, 2.3, 2.0, 0.1],
         'cost': [0.16, 0.24, 0.09, 0.23, 0.84, 0.11],
         'protein': [8.00, 0.30, 1.1, 8.1, 42.2, 6.7],
         'calories': [74.00, 81.40, 81.0, 121.2, 227.2, 99.6],
         'carbohydrates': [13.6, 21.00, 12.4, 11.7, 0.02, 1.3],
         'calcium': [159.00, 9.7, 6.7, 302.3, 21.9, 42.6]

         }


def re_solve(a, b, bounds, is_smaller, is_min, new_demand=None, new_constraint=None, new_objective=None):
    # is_max=1 if objective is to maximize  otherwise -1
    if new_demand:
        v = float(is_smaller) * new_demand
        b = np.append(b, v)
    if new_constraint:
        new_constraint = float(is_smaller) * (np.array(new_constraint)).flatten()
        a = np.vstack((a, new_constraint))
    new_objective = np.array(new_objective)
    new_objective = int(is_min) * new_objective.flatten()
    res = sopt.linprog(c=new_objective, A_ub=a, b_ub=b, bounds=bounds)

    return res


# A matrix A - nutrient in one unit of each food
# first solve with only 3 core nutients - fat, protein and VitC
A = np.vstack((foods['fat'], foods['protein']))
A = np.vstack((A, foods['vitC']))
A = -1 * np.array(A)
b = [20.1, 50.0, 50.1]
b = np.array(b)
b = -1 * b.flatten()
bounds = (0, 8)
bounds = (bounds, bounds, bounds, bounds, bounds, bounds)

yesno = 1
# first objective - cost of the diet
newObj = foods['cost']

res = re_solve(A, b, bounds, -1, 1, new_objective=newObj)

while True:
    print('current solution: x=', res.x, 'y=', res.fun)
    yesno = input('would you like to re solve with new objective? 1 for"yes",0 for "no"')
    if int(yesno) == 1:
        prevObj = newObj
        concession = input('enter a concession for  current solution')
        f_value = res.fun
        newDemand = f_value + float(concession)
        newConstr = prevObj
        inp = input('enter new objective')
        newObj = foods[inp]
        is_smaller = input('enter 1 for constraint < or -1 for >')
        is_min = input('enter 1 for min and -1 for max')
        re_solve(A, b, bounds, is_smaller, is_min, newDemand, newConstr, newObj)
    else:
        break
