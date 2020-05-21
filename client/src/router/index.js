import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home.vue';
import Statistics from '@/views/Statistics.vue';
import Ping from '@/components/ping.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    { path: '*', redirect: '/' }, // catch-all route
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/statistik',
      name: 'Statistics',
      component: Statistics,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});

/* eslint-disable eol-last */
