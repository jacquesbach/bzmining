<template>

  <div style="height: 500px; width: 100%">
    <p>Center is at {{ currentCenter }} and the zoom is: {{ currentZoom }}</p>
    <l-map
      style="height: 100%"
      :options="mapOptions"
      :center="center"
      :zoom="zoom"
      @update:center="centerUpdate"
      @update:zoom="zoomUpdate"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
      />
    </l-map>
  </div>
</template>

<script>
import {
  LMap,
  LTileLayer,
} from 'vue2-leaflet';
import { latLng } from 'leaflet';

export default {
  name: 'KeywordsCommentsMap',
  components: {
    LMap,
    LTileLayer,
  },
  data() {
    return {
      url: 'http://bz-mining.zapto.org/wp-content/uploads/tiles/keywords-comments/{z}/{x}/{y}.png',
      zoom: 2,
      center: latLng(47.41322, -1.219482),
      currentCenter: latLng(47.41322, -1.219482),
      currentZoom: 2,
      attribution:
        '&copy; <a href="https://github.com/jacquesbach/">Jakob Bach</a>',
      mapOptions: {
        zoomSnap: 1,
        zoom: 2,
        minZoom: 0,
        maxZoom: 6,
      },
    };
  },
  methods: {
    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },
    centerUpdate(center) {
      this.currentCenter = center;
    },
  },
};
</script>
