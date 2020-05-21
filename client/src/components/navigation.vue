<template>
  <div>
    <div class="logo"></div>
    <nav>
      <router-link v-for="routes in links"
      v-bind:key="routes.id"
      :to="`${routes.page}`"  class="separator">{{routes.text}}</router-link>
    </nav>
    <div class="clearfix"></div>
  </div>
</template>

<script>
export default {
  name: 'Navigation',
  data() {
    return {
      links: [
        {
          id: 0,
          text: 'Home',
          page: '/',
        },
        {
          id: 1,
          text: 'Statistics',
          page: '/statistics',
        },
        {
          id: 2,
          text: 'Network Graphs',
          page: '/networkgraphs',
        },
      ],
    };
  },
};
</script>

<style>
a {
  color:#466DB2;
  transition: all .2s ease;
}
a:hover {
  color:#2f2f2f;
  text-decoration: none;
}
a.router-link-exact-active {
  font-weight: 700;
  color:#2f2f2f;
}
.logo {
  line-height: 0px;
  font-size:0px;
  color:transparent;
  background-image:url(../assets/logo-text.svg);
  background-position: left bottom;
  background-repeat: no-repeat;
  background-size: 250px auto;
  height:63px;
  width:255px;
  display:block;
  margin-bottom:50px;
  float:left;
}
nav {
  text-align: right;
  vertical-align: middle;
}
.separator {
  margin-right: 15px;
}
.separator:not(:last-child):after {
}
.clearfix:after {
  content: "";
  display: table;
  clear: both;
}
</style>
