<template>
  <div>
    <div id="chartcategorylength" style="width: 100%; height: 500px;"></div>
  </div>
</template>

<script>
import * as am4core from '@amcharts/amcharts4/core';
import * as am4charts from '@amcharts/amcharts4/charts';
import am4themesAnimated from '@amcharts/amcharts4/themes/animated';

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
      am4core.useTheme(am4themesAnimated);

      // Create chart instance
      const chart = am4core.create('chartcategorylength', am4charts.XYChart);
      chart.maskBullets = false;

      chart.data = issuesVal;
      console.log(issuesVal);

      // Create axes
      const categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
      categoryAxis.dataFields.category = 'category';
      categoryAxis.renderer.grid.template.location = 0;
      categoryAxis.renderer.minGridDistance = 30;
      categoryAxis.renderer.labels.template.rotation = 270;

      /* eslint-disable no-unused-vars */
      const valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
      /* eslint-enable no-unused-vars */

      // Create series
      const series = chart.series.push(new am4charts.ColumnSeries());
      series.dataFields.valueY = 'length';
      series.dataFields.categoryX = 'category';
      series.name = 'Textlänge';
      series.columns.template.tooltipText = '{categoryX}: [bold]{valueY}[/]';
      series.columns.template.fillOpacity = 0.8;

      const columnTemplate = series.columns.template;
      columnTemplate.strokeWidth = 2;
      columnTemplate.strokeOpacity = 1;
    },
  },
};
</script>

/* eslint-disable camelcase */
