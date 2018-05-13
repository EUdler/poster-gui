#If too many nutrient values are zero, it may return "null." If res.x returns 
#nan, just tell the user that there exists no diet within their constraints.

#If you get a negative y, apparently that's typical and means you were maximizing 
#rather than minimizing a value.

#The first input is not via the tuple, or it would run forever

#Note that the concession is the current bound PLUS what you enter as the concession

#Instead of cost, the initial value being optimized is 'Energ_Kcal', energy in kilocalories. Then you can select a new nutrient as the target, enter the name given in ABBREV.xlsx



import scipy.optimize as sopt
import numpy as np
from xlrd import open_workbook,XL_CELL_TEXT

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#STUFF THAT ISN'T BY ELI'S MOM

#Here's how we import data from Excel. Just change the program to use these.
book = open_workbook('ABBREV.xlsx')
sheet = book.sheet_by_index(0)
foodnames = [sheet.cell(i, 1).value for i in range(1, 8791)] #List of all available food items
nutrients = [sheet.cell(0, i).value for i in range(2, 49)] #List of all nutrients

#Here is where we store the input we would get from a user
UserFoods = [2, 4, 12, 19] #the user inputs the index of each food item they are willing to eat, these are dummy values for testing
isEdible = [True if i in UserFoods else False for i in range(1, 8791)] #A list of boolean values, indicating whether the user will eat this food


#You may want these if you want to run the program with all possible foods
nutrientArrays = [[sheet.cell(j, i).value for j in range(1, 8791)] for i in range (2, 49)] #An array of arrays containing the quantity of this nutrient that each food has, in order
foodsDict = {nutrients[i] : nutrientArrays[i] for i in range(len(nutrients))} #A dictionary where each key is a nutrient and each value is a list containing the quantity of this nutrient that each food has, in order


#here are the array and dictionary for when we are allowed to select the foods we will eat
edibleFoodNutrientArrays = [[sheet.cell(j, i).value for j in range(1, 8791) if j in UserFoods] for i in range (2, 49)]
edibleFoodsDict = {nutrients[i] : edibleFoodNutrientArrays[i] for i in range(len(nutrients))}

print(edibleFoodsDict)

#Eli's notes:
# The initial objective is cost. Array x contains the number of servings of each
#food item and float y contains the target value.
#When it asks for a concession, you enter a new maximum value for your current
#objective (initially, this is cost). You're essentially saying "I'm willing to
#pay x dollars for food today"
#When it asks to enter a new objective, you may enter another nutrient, such as
#fat or VitC. When it asks whether you want min or max in new objective, you are
#being asked whether you want to minimize or maximize the value of this nutrient.
#For example, you may want to minimize calories, or to maximize protein. 
#Similarly, you are asked whether you want to minimize or maximize the old
#objective function. Your answer is evaluated and printed. Then the program loops.

#so your input is as follows:
#a. 1 or 0
#b. float/int
#c. string (should be in list "nutri")
#d. -1 or 1
#e. -1 or 1
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


#Here's a replacement for the sequential input
userInput = (1, 4, 'Ash_(g)', 1, 1)

foods = edibleFoodsDict

#Amatrix A - nutrient in one unit of each food
#first solve with only 3 core nutients - fat, protein and VitC


A=np.vstack((foods['Lipid_Tot_(g)'],foods['Protein_(g)']))
A=np.vstack((A,foods['Carbohydrt_(g)']))
A=-1*np.array(A)
b=[20.1,50.0,50.1] #Demands: maximum nutritional requirements
b=-1*np.array(b).flatten()
bound = (0, 8)
Bounds = [(bound)] * len(UserFoods) #Don't allow more than 8 servings of something
Bounds=tuple(Bounds)




yesno=1
#first objective - cost of the diet
newObj=foods['Energ_Kcal']
newObj=np.array(newObj).flatten()
res = sopt.linprog(c=newObj, A_ub=A, b_ub=b, bounds=Bounds)

print(res)

while True:
    print('current solution: x=', res.x, 'y=', res.fun)
    yesno=input("Resolve with new concession? 1 for Yes, 0 for No: ") #Do you want to re-solve?
    if int(yesno) == 1:
        prevObj = newObj
        concession = userInput[1] #This is the concession
        f_value=res.fun
        newDemand = f_value + float(concession)
        newConstr = prevObj
        inp = userInput[2] #this is the objective
        newObj = foods[inp]
        is_newmin = userInput[3]
        is_oldmin = userInput[4]
        newObj = float(is_newmin)*np.array(newObj).flatten()
        v = float(is_oldmin)*newDemand  
        b = np.append(b,v)
        newConstr = float(is_oldmin)*(np.array(newConstr)).flatten() 
        A = np.vstack((A,newConstr)) 
        res = sopt.linprog(c=newObj,A_ub=A,b_ub=b,bounds=Bounds)
        #///////////////////////////////////////////////////////////////////////////////////
        #After our first re-solve, we can output this dictionary
        solution =  {inp: #The key of this dict is the objective, extremely intuitively named "inp"
            (concession, #concession 
            res.x, #List of servings of each food
            res.fun,#target function
            "min" if is_newmin == "1" else "max", #was the new objective min or max
            "min" if is_oldmin == "1" else "max")} #was the old objective min or max
        
        print(solution)
        #///////////////////////////////////////////////////////////////////////////////////
    else:
        break
    







