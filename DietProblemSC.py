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


'''
#list of foods
foodnames=["broccoli","apple","oatmeal cookie","milk","chicken","omelette"]
#list of nutritional parametrs - see more on Excel spreadsheet/NutritionFacts
nutri=["cost","fat","vitA","vitC","protein","calories","carbohydrates", "calcium"]
foods={'fat':[0.80,0.50,3.3,4.7,10.8,7.3],
       'vitA':[70.0,73.10,2.9,100,77.4,409.2],
       'vitC':[160.20,7.90,0.1,2.3,2.0,0.1],
       'cost':[0.16,0.24,0.09,0.23,0.84,0.11],
       'protein':[8.00,0.30,1.1,8.1,42.2,6.7],
       'calories':[74.00,81.40,81.0,121.2,227.2,99.6],
       'cabohydrates':[13.6,21.00,12.4,11.7,0.02,1.3],
       'calcium':[159.00,9.7,6.7,302.3,21.9,42.6]
       #add more if you like
}
'''
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
    yesno=input('would you like to re-solve with new objective? 1 for"yes", 0 for "no": ')
    if int(yesno)==1:
        prevObj=newObj
        concession=input('enter a concession for current solution: ')
        f_value=res.fun
        newDemand=f_value+float(concession)
        newConstr=prevObj
        inp=input('enter new objective: ')
        newObj=foods[inp]
        is_newmin=input('enter 1 for min in new objective, and -1 for max: ')
        is_oldmin=input('enter 1 for min in old objective, and -1 for max: ')
        newObj=float(is_newmin)*np.array(newObj).flatten()
        v=float(is_oldmin)*newDemand  
        b=np.append(b,v)
        newConstr=float(is_oldmin)*(np.array(newConstr)).flatten() 
        A=np.vstack((A,newConstr)) 
        res= sopt.linprog(c=newObj,A_ub=A,b_ub=b,bounds=Bounds)
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
    







