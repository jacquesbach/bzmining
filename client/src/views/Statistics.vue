<template>
  <body>
      <Navigation></Navigation>
      <div id="app">
        <form action="#" @submit.prevent="getArticles">
          <div class="form-group">
            <input
              type="text"
              placeholder="Gib hier einen Suchbegriff für den Artikelinhalt ein!"
              v-model="searchterm"
              class=""
            ><br/>
            <input
              type="text"
              placeholder="Gib hier einen Autor ein!"
              v-model="authorterm"
              class=""
            ><br/>
            <input
              type="text"
              placeholder="Gib hier einen Titel ein!"
              v-model="titleterm"
              class=""
            ><br/>
            <div class="form-check">
            <label class="form-check-label">
              <input type="checkbox" id="checkbox" class="form-check-input"
              v-model="showdpa" @change="getArticles">
              Zeige dpa-Artikel an?
            </label>
            </div>
            <p>
            <input type="submit" value="Absenden">
            </p>
          </div>
        </form>
        <div class="alert alert-info" v-show="loading">Lade...</div>
        <div class="alert alert-danger" v-show="errored">Es trat ein Fehler auf.</div>
        <amchartstimeserieschart :articlesattribute="articlesnew"></amchartstimeserieschart>
        <amchartsweekdayhour :articlesattribute="weekdayhour"></amchartsweekdayhour>
        <amchartscategorylength :articlesattribute="categorylength"></amchartscategorylength>
      </div>
  </body>
</template>

<script>

import axios from 'axios';
import moment from 'moment';
import amchartsweekdayhour from '@/components/amchartsweekdayhour.vue';
import amchartstimeserieschart from '@/components/amchartstimeserieschart.vue';
import amchartscategorylength from '@/components/amchartscategorylength.vue';
import Navigation from '@/components/navigation.vue';

export default {
  name: 'app',
  components: {
    amchartstimeserieschart,
    amchartsweekdayhour,
    amchartscategorylength,
    Navigation,
  },
  data() {
    return {
      loading: false,
      errored: false,
      articlesnew: [],
      weekdayhour: [],
      searchterm: '',
      authorterm: '',
      titleterm: '',
      startDate: null,
      showdpa: true,
      apiurl: null,
    };
  },
  methods: {
    getDateRange() {
      const startDate = moment('2020-02-08');
      const endDate = moment();
      const dates = [];
      while (startDate.isSameOrBefore(endDate)) {
        dates.push({
          date: startDate.format('YYYY-MM-DD'),
          count: 0,
          countdpa: 0,
        });
        startDate.add(1, 'days');
      }
      return dates;
    },
    getArticles() {
      const apiurl = process.env.VUE_APP_API;
      this.loading = true;
      const path = `${apiurl}/articles?s=${this.searchterm}&author=${this.authorterm}&title=${this.titleterm}`;
      this.startDate = moment('2020-02-08').format('YYYY-MM-DD');
      axios
        .get(path)
        .then((response) => {
          const payload = this.getDateRange();
          response.data.forEach((element) => {
            const key = moment(element.date).format('YYYY-MM-DD');
            const obj = payload.filter((o) => o.date === key)[0];
            if ((typeof obj !== 'undefined') && (obj !== null)) {
              obj.count = element.count;
              if (this.showdpa) {
                obj.countdpa = element.countdpa;
              }
            }
          });
          payload.searchterm = this.searchterm;
          this.articlesnew = payload;
        })
        // .catch((error) => { console.error(error); });
        .finally(this.loading = false);
    },
    getWeekdayHourLength() {
      const apiurl = process.env.VUE_APP_API;
      const path = `${apiurl}/articles/hour/length`;
      axios
        .get(path)
        .then((response) => {
          this.weekdayhour = response.data;
        });
    // .catch((error) => { console.error(error); });
    },
    getCategoryLength() {
      const apiurl = process.env.VUE_APP_API;
      const path = `${apiurl}/articles/category/length`;
      axios
        .get(path)
        .then((response) => {
          this.categorylength = response.data;
        });
    // .catch((error) => { console.error(error); });
    },
  },
  mounted() {
    this.getArticles();
    this.getWeekdayHourLength();
    this.getCategoryLength();
  },
};
</script>
<!--@import '../public/new.min.css';-->
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
input {
  width:100%;
  text-align:center;
}
</style>

/* eslint-disable */
