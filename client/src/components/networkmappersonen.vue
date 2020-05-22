<template>

  <div style="height: 500px; width: 100%">
    <!--<p>Center is at {{ currentCenter }} and the zoom is: {{ currentZoom }}</p>-->
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
// import { latLng } from 'leaflet';

export default {
  name: 'PersonenMap',
  components: {
    LMap,
    LTileLayer,
  },
  data() {
    return {
      url: '/map_tiles/person-names/{z}/{x}/{y}.png',
      zoom: 2,
      center: [56.559482, -66.796875],
      currentCenter: [56.559482, -66.796875],
      currentZoom: 2,
      attribution:
        '&copy; <a href="https://github.com/jacquesbach/">Jakob Bach</a>',
      mapOptions: {
        maxZoom: 6,
        minZoom: 2,
        zoomControl: 1,
        scrollWheelZoom: 0,
        doubleClickZoom: 1,
        attributionControl: false,
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
