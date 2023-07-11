import random
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from core.models import Recipe, Tag, Ingredient

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with random recipes'

    TAGS = ['Breakfast', 'Lunch', 'Dinner', 'Dessert',
            'Vegetarian', 'Vegan', 'Gluten-Free']
    INGREDIENTS = ['Salt', 'Pepper', 'Sugar', 'Flour',
                   'Butter', 'Eggs', 'Milk', 'Cheese', 'Tomatoes']

    def add_arguments(self, parser):
        parser.add_argument('num_recipes', type=int,
                            help='Number of recipes to create')

    def handle(self, *args, **options):
        if Recipe.objects.count() >= 100:
            self.stdout.write(self.style.WARNING(
                'already 100 or more items in db. Skipping population.'))
            return

        num_recipes = options['num_recipes']

        for i in range(num_recipes):
            user = random.choice(User.objects.all())
            title = f"Recipe {i + 1}"
            time_minutes = random.randint(10, 60)
            price = Decimal(random.uniform(5, 20))
            description = "Sample description"
            link = "https://www.example.com"

            recipe = Recipe.objects.create(
                user=user,
                title=title,
                time_minutes=time_minutes,
                price=price,
                description=description,
                link=link
            )

            self.stdout.write(self.style.SUCCESS(
                f"Recipe created: {recipe.title}"))

            # Add random tags to the recipe
            num_tags = random.randint(1, 3)
            tags = random.sample(self.TAGS, num_tags)
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name, user=user)
                recipe.tags.add(tag)

            # Add random ingredients to the recipe
            num_ingredients = random.randint(3, 6)
            ingredients = random.sample(self.INGREDIENTS, num_ingredients)
            for ingredient_name in ingredients:
                ingredient, _ = Ingredient.objects.get_or_create(
                    name=ingredient_name, user=user)
                recipe.ingredients.add(ingredient)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Tags and ingredients added to the recipe: {recipe.title}"
                )
            )
