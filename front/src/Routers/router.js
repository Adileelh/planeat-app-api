import { createRouter, createWebHistory } from 'vue-router';
import Homepage from '../components/Homepage.vue';
import Register from '../components/Register.vue';
import Login from '../components/Login.vue';
import Recipes from '../components/Recipes.vue';

const routes = [
  { path: '/', component: Homepage },
  { path: '/register', component: Register },
  { path: '/login', component: Login },
  { path: '/recipes', component: Recipes },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
