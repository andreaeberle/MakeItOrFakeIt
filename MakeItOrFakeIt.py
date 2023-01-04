"""
MAKE IT OR FAKE IT
A program that calculates whether it is cheaper to buy something from the store or to make
it yourself.

    Program reads information for conversions, prices, and recipes in three .txt files.

    Program currently operates based on pre-loaded values, but could be expanded to allow
    for user input.
"""

import os, sys

class Ingredient():
    """ Ingredient class for objects that store an ingredient's name and the
    amount used to create the item that they are an ingredient of. With this information,
    an ingredient object then calculates its own cost based on its per-liter price and
    the quantity used to create the item. """

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        self.price_per_liter = checkForPrice(self.name)

        # Calculating ingredient's cost based on quantity in the item's recipe
        quantity_in_liters = convertToLiters(self.amount)
        self.cost = quantity_in_liters * self.price_per_liter

    def __str__(self):
        return f"{self.amount} of {self.name}"

    def getCost(self):
        return self.cost

class Item():
    """ Item class is a container for Ingredient objects. Item class is passed its store
    price and a dictionary containing a recipe for the item (with each ingredient's name as
    the key and the amount of the ingredient used to create the item as the value) """

    def __init__(self, name, item_price, recipe_dict):
        self.name = name
        self.price = item_price
        
        self.ingredient_list = [Ingredient(x, recipe_dict.get(x)) for x in
                                recipe_dict.keys()]
            
    def calculateCostOfMaking(self):
        """ Method loops through each ingredient used to create the Item and adds up the
        cost of each ingredient to get the total cost of making the item from scratch """
        self.cost_of_making = 0
        for ingredient in self.ingredient_list:
            self.cost_of_making += ingredient.getCost()
        return self.cost_of_making

    def getDetermination(self):
        """ Determines whether an item is cheaper to make yourself or to buy at
        a store based on the item's price versus the total cost of making the item from
        scratch """
        if self.cost_of_making > self.price:
            print(f"It is cheaper to buy {self.name} than it is to make it... So fake it!")
        else:
            print(f"It is cheaper to make {self.name} than it is to buy it... So make it!")

    def printIngredientCosts(self):
        """ Displays the cost of each ingredient in an item's recipe """
        print(f"To make {self.name}, it costs: ")
        for ingredient in self.ingredient_list:
            print(f"    ${ingredient.getCost():.2f} for {ingredient}")


def checkForPrice(item):
    """ Searches the .txt file "prices" for relevant price information """
    file_name = os.path.join(__file__, "..", "saved_info", "prices.txt")

    try:
        with open(file_name) as open_file:
            for line in open_file:
                info = line.strip().split(": ")
                if info[0] == item:
                    price = float(info[1].strip("$"))
                    return price
            return f"No price information available for {item}"
        
    except IOError:
        sys.stderr.write(f"The file '{file_name}' cannot be read.\n")


def checkForRecipe(item):
    """ Searches the .txt file "recipes" for relevant recipe information """
    file_name = os.path.join(__file__, "..", "saved_info", "recipes.txt")

    try:
        with open(file_name) as open_file:
            #print(open_file.readlines())
            recipe_found = False
            for line in open_file:
                if line.strip() == f"|{item}|":
                    recipe_found = True
                    print(f"Saved recipe is available for {item}")
                    recipe_dict = {}
                    continue
                if recipe_found:
                    if "|" in line:
                        break
                    info = line.strip().split(": ")
                    recipe_dict[info[0]] = info[1]

            if recipe_found:
                return recipe_dict

            print(f"No saved recipes available for {item}")
            return None
     
    except IOError:
        sys.stderr.write(f"The file '{file_name}' cannot be read.\n")

def convertToLiters(amount):
    """ Converts a quantity to liters """
    
    quantity, unit = amount.split()
    quantity = float(quantity)
    
    if unit != "l":
        conversion_rate = getConversion(unit, "l")
        quantity_in_liters = quantity * conversion_rate
    else:
        quantity_in_liters = quantity
        
    return quantity_in_liters
    
def getConversion(from_unit, to_unit):
    """ Searches the .txt file "conversions" for relevant recipe information """
    file_name = os.path.join(__file__, "..", "saved_info", "conversions.txt")

    try:
        with open(file_name) as open_file:
            for line in open_file:
                if f"1 {from_unit}" in line:
                    conversion_info = line.split()
                    if conversion_info[-1] == to_unit:
                        conversion_rate = conversion_info[-2]
                        return float(conversion_rate)
                
            print(f"No saved conversations available for {from_unit} to {to_unit}")
            return None
     
    except IOError:
        sys.stderr.write(f"The file '{file_name}' cannot be read.\n")

def main():
    test_tuple = ("bread", "pico de gallo")

    for test in test_tuple:
        item = test

        # Checking to see if necessary item info is already contained in saved_info
        item_price = checkForPrice(item)
        print(f"The price of {item} is ${item_price}")
        recipe_dict = checkForRecipe(item)
        
        if not recipe_dict:
            pass # Can add functionality to allow user input

        oItem = Item(item, item_price, recipe_dict)
        final_cost = oItem.calculateCostOfMaking()
        
        oItem.printIngredientCosts()
        print(f"It would cost ${final_cost:.2f} to make {item} yourself")

        oItem.getDetermination()

        print("")

if __name__ == "__main__":
    main()
