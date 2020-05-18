<template>
  <div>
    <div id="chartweekdayhour" style="width: 100%; height: 500px;"></div>
  </div>
</template>

<script>
import * as am4core from '@amcharts/amcharts4/core';
import * as am4charts from '@amcharts/amcharts4/charts';
import am4themes_animated from '@amcharts/amcharts4/themes/animated';

export default {
  props: ['articlesattribute'],
  data() {
    return {
      chart: null,
    };
  },
  watch: {
    articlesattribute(val) {
      if (this.chart != null) this.chart.remove();
      this.renderChart(val);
    },
  },
  methods: {
    renderChart(issuesVal) {
      // Create chart instance
      const chart = am4core.create('chartweekdayhour', am4charts.XYChart);
      chart.maskBullets = false;

      chart.data = issuesVal;
      console.log(issuesVal);

      const xAxis = chart.xAxes.push(new am4charts.CategoryAxis());
      const yAxis = chart.yAxes.push(new am4charts.CategoryAxis());

      yAxis.dataFields.category = 'weekday';
      xAxis.renderer.minGridDistance = 10;
      xAxis.dataFields.category = 'hour';

      xAxis.renderer.grid.template.disabled = true;
      yAxis.renderer.grid.template.disabled = true;
      xAxis.renderer.axisFills.template.disabled = true;
      yAxis.renderer.axisFills.template.disabled = true;
      yAxis.renderer.ticks.template.disabled = true;
      xAxis.renderer.ticks.template.disabled = true;

      yAxis.renderer.inversed = true;

      const series = chart.series.push(new am4charts.ColumnSeries());
      series.dataFields.categoryY = 'weekday';
      series.dataFields.categoryX = 'hour';
      series.dataFields.value = 'count';
      series.dataFields.valueY = 'length';
      series.name = 'Absolute Zahl der an diesem Wochentag zu dieser Zeit veröffentlichten Artikel';
      series.columns.template.disabled = true;
      series.sequencedInterpolation = true;
      // series.defaultState.transitionDuration = 3000;

      const bullet = series.bullets.push(new am4core.Circle());
      bullet.tooltipText = '{weekday}, {hour} Uhr: {count} Artikel';
      bullet.strokeWidth = 3;
      bullet.stroke = am4core.color('#ffffff');
      bullet.strokeOpacity = 0;

      bullet.adapter.add('tooltipY', (tooltipY, target) => -target.radius + 1);

      series.heatRules.push({
        property: 'radius',
        target: bullet,
        min: 1,
        max: 20,
      });

      series.heatRules.push({
        target: bullet,
        property: 'fill',
        min: am4core.color('#AEEEEE'),
        max: am4core.color('#FF0000'),
        dataField: 'valueY',
      });

      bullet.hiddenState.properties.scale = 0.01;
      bullet.hiddenState.properties.opacity = 1;

      const hoverState = bullet.states.create('hover');
      hoverState.properties.strokeOpacity = 1;

      chart.legend = new am4charts.Legend();
      const heatLegend = chart.bottomAxesContainer.createChild(am4charts.HeatLegend);
      heatLegend.width = am4core.percent(100);
      heatLegend.series = series;
      heatLegend.valueAxis.renderer.labels.template.fontSize = 0;
      heatLegend.valueAxis.renderer.minGridDistance = 30;
    },
  },
};
</script>

/* eslint-disable camelcase */
