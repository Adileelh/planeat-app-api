<template>
   <div class="mx-auto container flex flex-col">

       <h1 class="text-center text-8xl my-3">Recettes</h1>
    <div class="flex flex-wrap">



            <div class=" mx-auto m-1 flex" v-for="recipe in recipes" :key="recipe.id">
                <a href="#" class="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
                    <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{{ recipe.title }}</h5>
                    <p class="font-normal text-gray-700 dark:text-gray-400">{{ recipe.description }}.</p>
                    <p class="font-normal text-gray-700 dark:text-gray-400">{{ recipe.link }}.</p>
                </a>
            </div>



    </div>
   </div>
  </template>
  <script>

import axios from 'axios';

export default {
  // ...
  data() {
    return {
      recipes: [] // Tableau pour stocker les recettes
    };
  },
  mounted() {
    this.getRecipes();
  },
  methods: {
    async getRecipes() {
      try {
        const response = await axios.get('http://localhost:8000/api/recipe/recipes/');
        this.recipes = response.data;
        console.log(response.data);
      } catch (error) {
        console.log(error);
      }
    }
  }
}

</script>