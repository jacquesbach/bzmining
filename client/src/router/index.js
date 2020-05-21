import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home.vue';
import Statistics from '@/views/Statistics.vue';
import Network from '@/views/Networkgraphs.vue';
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
      path: '/statistics',
      name: 'Statistics',
      component: Statistics,
    },
    {
      path: '/networkgraphs',
      name: 'Network',
      component: Network,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});

/* eslint-disable eol-last */
