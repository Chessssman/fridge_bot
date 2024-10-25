import requests

class RecipeGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_recipe(self, ingredients):
        url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={self.api_key}&includeIngredients={",".join(ingredients)}&language=ru'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return data['results'][0]['title']
        return "Не удалось найти рецепт."
