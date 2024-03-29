"""serializers for recipe api"""

from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
    Ingredient
)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'title',
            'time_minutes',
            'price',
            'link',
            'tags',
            'ingredients'

        )
        read_only_fields = ('id',)

    def _get_or_create_tags(self, recipe, tags):
        """Handle getting or creating tags"""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, recipe, ingredients):
        """Handle getting or creating ingredients"""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """Create and return a new recipe"""
        tags = validated_data.pop('tags', [])
        ingredient = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(recipe, tags)
        self._get_or_create_ingredients(recipe, ingredient)

        return recipe

    def update(self, instance, validated_data):
        """Update a recipe, adding tags if provided"""
        tags = validated_data.pop('tags', None)
        ingredient = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(instance, tags)

        if ingredient is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(instance, ingredient)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail objects"""
    # ingredients = IngredientSerializer(many=True, read_only=True)
    # tags = TagSerializer(many=True, read_only=True)

    class Meta(RecipeSerializer.Meta):

        fields = RecipeSerializer.Meta.fields + ('description', 'image')


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes"""

    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
        extra_kwargs = {'image': {'required': True}}
