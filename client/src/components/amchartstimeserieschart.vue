<template>
  <div>
    <div id="charttimeseries" style="width: 100%; height: 550px;"></div>
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
      am4core.useTheme(am4themes_animated);

      // Create chart instance
      const chart = am4core.create('charttimeseries', am4charts.XYChart);

      // Add data
      chart.data = issuesVal;

      // Set input format for the dates
      chart.dateFormatter.inputDateFormat = 'yyyy-MM-dd';

      // Create axes
      const dateAxis = chart.xAxes.push(new am4charts.DateAxis());
      const valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

      // Create series
      const series = chart.series.push(new am4charts.LineSeries());
      series.dataFields.valueY = 'countall';
      series.dataFields.dateX = 'date';
      series.name = 'Zahl aller veröffentlichten Artikel';
      series.tooltipText = '{countall}';
      series.stroke = am4core.color('#985757'); // red
      series.strokeWidth = 2;
      series.minBulletDistance = 15;
      series.tooltip.getFillFromObject = false;
      series.tooltip.background.fill = am4core.color('#985757');
      series.tooltip.label.fill = am4core.color('#fff');
      series.tooltip.background.cornerRadius = 20;
      series.tooltip.background.strokeOpacity = 0;
      series.tooltip.pointerOrientation = 'vertical';
      series.tooltip.label.minWidth = 40;
      series.tooltip.label.minHeight = 40;
      series.tooltip.label.textAlign = 'middle';
      series.tooltip.label.textValign = 'middle';

      // Create series2
      const series2 = chart.series.push(new am4charts.LineSeries());
      series2.dataFields.valueY = 'countdpa';
      series2.dataFields.dateX = 'date';
      series2.strokeWidth = 2;
      series2.minBulletDistance = 15;
      series2.tooltipText = '{countdpa}';
      series2.name = 'davon Artikel von dpa/mit dpa-Beteiligung';
      series2.stroke = am4core.color('#626d79'); // blue
      series2.tooltip.getFillFromObject = false;
      series2.tooltip.background.fill = am4core.color('#626d79');
      series2.tooltip.label.fill = am4core.color('#fff');
      series2.tooltip.background.cornerRadius = 20;
      series2.tooltip.background.strokeOpacity = 0;
      series2.tooltip.pointerOrientation = 'vertical';
      series2.tooltip.label.minWidth = 40;
      series2.tooltip.label.minHeight = 40;
      series2.tooltip.label.textAlign = 'middle';
      series2.tooltip.label.textValign = 'middle';

      // Make bullets grow on hover
      const bullet = series.bullets.push(new am4charts.CircleBullet());
      bullet.circle.strokeWidth = 2;
      bullet.circle.radius = 4;
      bullet.circle.fill = am4core.color('#fff');
      const bullethover = bullet.states.create('hover');
      bullethover.properties.scale = 1.3;

      // Make bullets grow on hover
      const bullet2 = series2.bullets.push(new am4charts.CircleBullet());
      bullet2.circle.strokeWidth = 2;
      bullet2.circle.radius = 4;
      bullet2.circle.fill = am4core.color('#fff');
      const bullethover2 = bullet2.states.create('hover');
      bullethover2.properties.scale = 1.3;

      // Make a panning cursor
      chart.cursor = new am4charts.XYCursor();
      chart.cursor.behavior = 'panXY';
      chart.cursor.xAxis = dateAxis;
      // chart.cursor.snapToSeries = series;

      // Create vertical scrollbar and place it before the value axis
      chart.scrollbarY = new am4core.Scrollbar();
      chart.scrollbarY.parent = chart.leftAxesContainer;
      chart.scrollbarY.toBack();

      // Create a horizontal scrollbar with previe and place it underneath the date axis
      chart.scrollbarX = new am4charts.XYChartScrollbar();
      chart.scrollbarX.series.push(series);
      chart.scrollbarX.parent = chart.bottomAxesContainer;

      chart.legend = new am4charts.Legend();

      dateAxis.start = 0;
      dateAxis.keepSelection = true;
    },
  },
};
</script>

/* eslint-disable camelcase */
