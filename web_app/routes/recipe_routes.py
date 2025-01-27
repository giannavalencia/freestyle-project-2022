# web_app/routes/recipe_routes.py

from flask import Blueprint, request, render_template, flash, redirect

from pprint import pprint

from app.recipe_generator_new import display_category, display_area, display_name, display_random, display_ingredient, fetch_recipe_area, fetch_recipe_category
from app.email_service import send_email

recipe_routes = Blueprint("recipe_routes", __name__)

@recipe_routes.route("/")
@recipe_routes.route("/recipes")
def index():
    print("Recipe...")
    return render_template("recipes.html")

# @recipe_routes.route("/recipes/list", methods=["GET", "POST"])
@recipe_routes.route("/recipes/list", methods=["GET","POST"])
def recipe_list():
    print("Recipe List...")

    form_data = dict(request.form)
    #print(form_data)

    method = form_data["method"]
    selection = form_data["selection"]
    email = form_data["email"]
    print(method)
    print(selection)
    print(email)

    if method == "By Category":
        recipes = display_category(selection)
    elif method == "By Nationality/Country of Origin":
        recipes = display_area(selection)
    elif method == "By Ingredient":
        recipes = display_ingredient(selection)
    elif method == "Random Selection":
        recipes = display_random()
    #pprint(recipes)

    #creating the HTML template and sending email
    if email:
        subject = "Custom Recipe List - Recipe Generator App Search"
        
        
        html = ""
        html += f"<h>Recipe Generator Search Results</h>"
        html += "<br>"
        html += f"<p>Here is you individual recipe list based on your search: .</p>"
        html += "<br>"
        # html += "<ul>"
        
        for recipe in recipes:
            html += f"<h> {recipe['name']} </h>"
            html += "<br>"
            html += "<br>"
            html += f"<img src={recipe['picture_url']} alt='Picture' width='400' height= '233' >"
            html += "<ul>"
            html += "<li>Ingredients</li>"
            html += "<ul>"
            for ingredient in recipe["ingredients"]:
                html += f"<li>{ingredient['name']} ({ingredient['measure']})</li>" 
            html += "</ul>"
            html += f"<li>Instructions: {recipe['instructions']} </li>"
            html += f"<li>Video URL: {recipe['video_url']}</li>"
            html += "</ul>"
            html += "<br>"
            html += "<hr>"
        # html += "</ul>"

        send_email(subject, html, email)

    
    try:
        if recipes:
            flash(f"Recipe Search Successful!", "success")
            return render_template("recipes_list.html", recipes=recipes)
        else:
            flash(f"Oops, something went wrong. Please correctly enter your inputs based on your instructions. You can refer to the Help Page to see the valid inputs. If an ingredient or recipe is in the help page but is still is procuding errors, please contact the Admin at 'kms475@georgetown.edu':", "warning")
            return redirect("/home")

    except Exception as err:
        print(err)
        flash(f"Oops, something went wrong: {err}", "warning")
        return redirect("/home")