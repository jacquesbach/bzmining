<template>
  <body>
      <Navigation></Navigation>
      <div id="app">
        <Networkmap></Networkmap>
      </div>
  </body>
</template>

<script>
import Navigation from '@/components/navigation.vue';
import Networkmap from '@/components/networkmapcomments.vue';

export default {
  name: 'app',
  components: {
    Navigation,
    Networkmap,
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');
@import url('https://fonts.googleapis.com/css?family=Sanchez&display=swap');
@import url('https://fonts.googleapis.com/css?family=Arimo&display=swap');
body {
  display:block;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  margin-top:60px;
  color: #2f2f2f;
  font-family: "Roboto";
  font-size: 20px;
  line-height: 1.7;
  overflow-wrap: break-word;
}
#app {
  text-align: center;
  color: #2c3e50;
}
</style>

/* eslint-disable */
