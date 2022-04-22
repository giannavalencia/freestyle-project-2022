# app/recipe_generator.py

import requests, json, os
from pprint import pprint
from IPython.display import Image, display 

# FUNCTION TO CONVERT API DATA TO A MORE ACCESSIBLE FORMAT
def read_data(url):
  response = requests.get(url)
  data = json.loads(response.text)
  return data

# FUNCTION TO PRINT THE RECIPE'S NAME AND PICTURE
def display_name_pics(data):
  print(data["strMeal"])
  display(Image(url=data["strMealThumb"], height=100))

# FUNCTION TO MORE EFFICIENTLY DISPLAY OUTPUT
def display_recipe(recipe):
  
  # PRINT LIST OF INGREDIENTS
  print("---------------------")   
  print("List of Ingredients")
  print("---------------------")
  for x in range (1,19):
      #define variables
      ingredientString = f'strIngredient{x}'
      measureString = f'strMeasure{x}'
      ingredient = recipe["meals"][0][ingredientString] 
      measure = recipe["meals"][0][measureString]

      # PRINT INGREDIENT IF IT EXISTS
      if ingredient:
        print(ingredient, "(" + measure + ")")
  print("---------------------")  

  # PRINT THE RECIPE INSTRUCTIONS
  print("Instructions")
  print("---------------------")
  print(recipe["meals"][0]["strInstructions"])
  print("---------------------")

  # PRINT CORRESPONDING VIDEO IF IT EXISTS
  video = recipe["meals"][0]["strYoutube"]
  if video:
    print("Video Link:", video)
  print("---------------------")

def convert_to_dict(recipe):
  ingredients = []
  for x in range (1,19):
    #define variables
    ingredientString = f'strIngredient{x}'
    measureString = f'strMeasure{x}'
    ingredient = recipe["meals"][0][ingredientString] 
    measure = recipe["meals"][0][measureString]

    # APPEND INGREDIENT AND MEASURE IF THEY BOTH EXIST
    if ingredient and measure:
      ingredients.append({
                          "name": ingredient.strip(),
                          "measure": measure.strip()
                         })
  title = recipe["meals"][0]["strMeal"]
  picture_url = recipe["meals"][0]["strMealThumb"]
  instructions = recipe["meals"][0]["strInstructions"]
  video_url = recipe["meals"][0]["strYoutube"]
  
  recipes = []
  recipes.append({
        "name": title.strip(),
        "picture_url": picture_url.strip(),
        "ingredients": ingredients,
        "instructions": instructions.strip(),
        "video_url": video_url.strip()
       })
  pprint(recipes)
  return recipes

# PRINT RECIPES BY NAME
def display_name(name):
  recipe_url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={name}'
  recipe = read_data(recipe_url)
  recipes = convert_to_dict(recipe)
  #pprint(recipes)
  return recipes

# PRINTING OUT RECIPES BY FOOD CATEGORY
def display_category(category): 
  category_url = f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}'
  category = read_data(category_url)

  #print(category)
  #meals = []
  for meal in category["meals"]:

    #meals.append(meal["strMeal"])

    display_name_pics(meal)
    name = meal["strMeal"]

    # Find the instructions and ingredients for each 
    recipe1_url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={name}'
    current = read_data(recipe1_url)

    # Display ingredients, intstruction, and video
    display_recipe(current)

# PRINT RECIPES BASED ON NATIONALITY/AREA
def display_area(area):
  area_url = f'https://www.themealdb.com/api/json/v1/1/filter.php?a={area}'
  area = read_data(area_url)

  for meal in area["meals"]:
    
    # Display the recipe's name and picture
    display_name_pics(meal)
    name = meal["strMeal"]

    # Find the instructions and ingredients for each 
    recipe1_url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={name}'
    current = read_data(recipe1_url)

    # Display ingredients, intstruction, and video
    display_recipe(current)

# PRINT 10 RECIPES RANDOMLY 
def display_random():
  for x in range (1,10):
    random_url = "https://www.themealdb.com/api/json/v1/1/random.php"
    random = read_data(random_url)
    
    # Display the recipe's name and picture
    display_name_pics(random["meals"][0])

    # Display ingredients, intstruction, and video
    display_recipe(random)

if __name__ == "__main__":
    name = "orange"
    selection =  "Seafood"
    area = "Canadian"


    # display_name(name)
    # display_category(category)
    # display_area(area)

    # recipes = display_category(selection)
    recipes = display_name(name)
    pprint(recipes)