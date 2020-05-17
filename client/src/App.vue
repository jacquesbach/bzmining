/* eslint-disable */

<template>
  <body>
    <div class="logo"></div>
      <p>Der Verwaltungswissenschaftler Klaus Simon äußerte sich 1987 in einem Beitrag
      zur Politikvermittlung durch die Lokalpresse wie folgt:</p>
      <blockquote cite="Simon, Klaus (1987): Kommunale Demokratie — eine
      Politikvermittlungs-Idylle?, in: Sarcinelli, Ulrich (Hg.): Politikvermittlung.
      Beiträge zur politischen Kommunikationskultur. Bonn, S. 232—247.">
      <p>Qualitativ ist die geringe Politikvermittlungsleistung der Lokalpresse
      [&#8230;] unzureichend. Sie enthält sich weitgehend der Kritik an der lokalen
      politischen Elite. Nur ca. zwei bis fünf Prozent ihrer Artikel weisen
      kritische Bemerkungen auf. Kommentare sind selten; es überwiegt der
      Verlautbarungsstil, indem Mitteilungen von Verwaltungen, anderen
      Organisationen, meist deren Führungen, berichtet, häufig sogar die dazu eingesandten Texte
      einfach abgedruckt werden. [&#8230;] Die Inhaber von Führungspositionen und die lokalen
      Organisationen erfreuen sich einer »lobhudlerischen Form der Darstellung«. Nur selten
      werden Probleme sozial schwacher Gruppen zur Sprache gebracht und damit
      »non-decision«-Barrieren überwunden, die solche Probleme normalerweise
      von der politischen Kommunikation in der Gemeinde fernhalten.
      Politikvermittlung in der Lokalpresse geschieht demnach höchst einseitig, im
      Interesse des Status quo und der lokalen Eliten »von oben nach unten«.</p></blockquote>
      <p>Als Klaus Simon diese Zeilen schrieb, erschienen Zeitungen ausschließlich im Print-Format,
      war die Auswertung der Zeitungsberichterstattung aufwändig und entsprechend waren die
      Stichproben in den von Klaus Simon rezipierten Untersuchungen zur Politikvermittlungsfunktion
      der Lokalpresse verhältnismäßig klein.</p>
      <p>Heute, in Zeiten von Big Data, ist das anders. Immer weniger Menschen lesen Zeitungen im
      Print-Format. Die Onlineauftritte der Zeitungen – auch solche der Lokalpresse – werden größer
      und dienen immer öfter als Ersatz für ein Zeitungsabonnement. Zugleich wurde mit der
      fortschreitenden Digitalisierung von Textinhalten auch Software entwickelt, die es
      ermöglicht, große Text- und Datenmengen auszulesen, aufzubereiten und zu analysieren.
      Das verspricht ein erhebliches Forschungspotential.</p>
      <p>Eine Analyse der Onlineberichterstattung eines deutschen Nachrichtenmagazins mittels
      Text- und Data-Mining führte David Kriesel vor einigen Jahren in seinem Projekt
      <a href="http://www.dkriesel.com/spiegelmining">„Spiegel Mining“</a> durch. Er analysierte
      das Publikationsverhalten von Spiegel Online, des vielleicht größten Meinungsmachers
      Deutschlands.</p>
      <p>Ähnliches soll hier mit der Website einer lokalen Tageszeitung aus Freiburg
      (<a href="https://www.badische-zeitung.de/">„Badische Zeitung“</a>) geschehen,
      um die Thesen, die Klaus Simon 1987 zur Funktion der Lokalpresse aufstellte, mittels
      moderner Methoden erneut zu überprüfen.</p>
      <p>Seit dem 8. Februar überwachen wir die Website der Badischen Zeitung und sammeln
      Daten über die veröffentlichten Artikel für eine ergebnisoffene Analyse. Nach und nach
      stellen wir hier die Auswertung zur Verfügung.</p>
      <div id="app">
        <form action="#" @submit.prevent="getArticles">
          <div class="form-group">
            <input
              type="text"
              placeholder="Gib hier einen Suchbegriff für den Artikelinhalt ein!"
              v-model="searchterm"
              class=""
            ><br/>
            <!--<input
              type="text"
              placeholder="Gib hier einen Autor ein!"
              v-model="authorterm"
              class="col-md-2 col-md-offset-5"
            ><br/>
            <input
              type="text"
              placeholder="Gib hier einen Titel ein!"
              v-model="titleterm"
              class="col-md-2 col-md-offset-5"
            >-->
          </div>
        </form>
        <div class="alert alert-info" v-show="loading">Lade...</div>
        <div class="alert alert-danger" v-show="errored">Es trat ein Fehler auf.</div>
        <!--<d3timeserieschart :articlesattribute="articlesnew"></d3timeserieschart>-->
        <amchartstimeserieschart :articlesattribute="articlesnew"></amchartstimeserieschart>
      </div>
  </body>
</template>

<script>

import axios from 'axios';

import moment from 'moment';

import d3timeserieschart from './components/d3timeserieschart.vue';
import amchartstimeserieschart from './components/amchartstimeserieschart.vue';

export default {
  name: 'app',
  components: {
    d3timeserieschart,
    amchartstimeserieschart,
  },
  data() {
    return {
      loading: false,
      errored: false,
      articlesnew: [],
      searchterm: '',
      authorterm: '',
      titleterm: '',
      startDate: null,
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
          countall: 0,
          countdpa: 0,
        });
        startDate.add(1, 'days');
      }
      return dates;
    },
    getArticles() {
      this.loading = true;
      const path = `http://localhost:5000/articles?dpa&s=${this.searchterm}&author=${this.authorterm}&title=${this.titleterm}`;
      this.startDate = moment('2020-02-08').format('YYYY-MM-DD');
      axios
        .get(path)
        .then((response) => {
          const payload = this.getDateRange();
          response.data.forEach((element) => {
            const key = moment(element.date).format('YYYY-MM-DD');
            const obj = payload.filter((o) => o.date === key)[0];
            if ((typeof obj !== 'undefined') && (obj !== null)) {
              obj.countall = element.countall;
              obj.countdpa = element.countdpa;
            }
          });
          this.articlesnew = payload;
        })
        .catch((error) => {
          this.errored = true;
          console.error(error);
        })
        .finally(this.loading = false);
    },
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
  margin-top: 60px;
}
input {
  width:100%;
  text-align:center;
}
.bar {
  fill: #626d79;
  }
.logo {
  line-height: 0px;
  font-size:0px;
  color:transparent;
  background-image:url(../public/logo-text.svg);
  background-position: left bottom;
  background-repeat: no-repeat;
  background-size: 250px auto;
  height:63px;
  width:255px;
  display:block;
  margin-bottom:20px;
}
blockquote {
  display: block;
  border-width: 2px 0;
  border-style: solid;
  border-color: #eee;
  padding: 1.5em 0 0.5em;
  margin: 1.5em 0;
  position: relative;
  font-family: 'Sanchez',serif;
}
blockquote:before {
  content: '\201C';
  position: absolute;
  top: -0.15em;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #fff;
  width: 3rem;
  height: 2rem;
  font: 6em/1.08em 'Arimo';
  color: #666;
  text-align: center;
}
blockquote:after {
  content: attr(cite);
  display: block;
  text-align: right;
  font-family: 'Roboto';
  font-size: 0.875em;
  font-style: italic;
}
</style>

/* eslint-disable camelcase */
