<template>
  <div>
    <svg></svg>
  </div>
</template>

<script>
import * as d3 from 'd3';
import _ from 'lodash';

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
      const margin = 60;
      const svgWidth = 800;
      const svgHeight = 500;
      const chartWidth = 800 - 2 * margin;
      const chartHeight = 500 - 2 * margin;
      const svg = d3
        .select('svg')
        .attr('width', svgWidth)
        .attr('height', svgHeight);
      this.chart = svg
        .append('g')
        .attr('transform', `translate(${margin}, ${margin})`);
      const yScale = d3
        .scaleLinear()
        .range([chartHeight, 0])
        .domain([0, _.maxBy(issuesVal, 'count').count]);
      this.chart
        .append('g')
        .call(d3.axisLeft(yScale).ticks(10));
      const xScale = d3
        .scaleBand()
        .range([0, chartWidth])
        .domain(issuesVal.map((s) => s.date))
        .padding(0.2);
      this.chart
        .append('g')
        .attr('transform', `translate(0, ${chartHeight})`)
        .call(d3.axisBottom(xScale));
      const barGroups = this.chart
        .selectAll('rect')
        .data(issuesVal)
        .enter();
      barGroups
        .append('rect')
        .attr('class', 'bar')
        .attr('x', (g) => xScale(g.date))
        .attr('y', (g) => yScale(g.count))
        .attr('height', (g) => chartHeight - yScale(g.count))
        .attr('width', xScale.bandwidth())
        .on('mouseenter', function (actual, i) {
          d3.select(this)
            .transition()
            .duration(300)
            .attr('opacity', 0.6)
            .attr('x', (a) => xScale(a.date) - 5)
            .attr('width', xScale.bandwidth() + 10);
          barGroups
            .append('text')
            .attr('class', 'value')
            .attr('x', (a) => xScale(a.date) + xScale.bandwidth() / 4)
            .attr('y', (a) => yScale(a.count) - 20)
            .attr('text-anchor', 'middle')
            .text((a, idx) => (idx !== i ? '' : `${a.count} Artikel am ${a.date}`));
        })
        .on('mouseleave', function () {
          d3.selectAll('.count').attr('opacity', 1);
          d3.select(this)
            .transition()
            .duration(300)
            .attr('opacity', 1)
            .attr('x', (a) => xScale(a.date))
            .attr('width', xScale.bandwidth());
          svg.selectAll('.value').remove();
        });
      svg
        .append('text')
        .attr('class', 'label')
        .attr('x', -(chartHeight / 2) - margin)
        .attr('y', margin / 2.4)
        .attr('transform', 'rotate(-90)')
        .attr('text-anchor', 'middle')
        .text('Veröffentlichte Artikel');
      svg
        .append('text')
        .attr('class', 'label')
        .attr('x', chartWidth / 2 + margin)
        .attr('y', chartHeight + margin * 1.7)
        .attr('text-anchor', 'middle')
        .text('Datum');
      svg
        .append('text')
        .attr('class', 'title')
        .attr('x', chartWidth / 2 + margin)
        .attr('y', 40)
        .attr('text-anchor', 'middle')
        .text('Veröffentlichte Artikel seit dem 8.2.2020');
    },
  },
};
</script>

/* eslint-disable camelcase */
