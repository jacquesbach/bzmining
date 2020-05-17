import Vue from 'vue';
import Router from 'vue-router';
import Ping from '../components/ping.vue';
import exams from '../components/exams.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/exams',
      name: 'exams',
      component: exams,
    },
  ],
});

/* eslint-disable eol-last */
