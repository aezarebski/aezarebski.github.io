/**
 * The summary statistics needed to make a boxplot.
 *
 * @param {number[]} xs - The values to summarise.
 *
 * @todo Handle outliers properly.
 */
function boxPlotStats(xs) {
    var sortedXs = xs.sort(d3.ascending);
    var q1 = d3.quantile(sortedXs, 0.25);
    var q2 = d3.quantile(sortedXs, 0.50);
    var q3 = d3.quantile(sortedXs, 0.75);
    var iQR = q3 - q1;
    var min = q1 - 1.5 * iQR;
    var max = q1 + 1.5 * iQR;
    return {
        q1: q1,
        q2: q2,
        q3: q3,
        IQR: iQR,
        min: min,
        max: max
    };
}

function makeFig04() {
    d3.csv("iris.csv").then((xs) => {

        var margin = { top: 10, right: 30, bottom: 30, left: 60 };
        var width = 460 - margin.right - margin.left;
        var height = 400 - margin.top - margin.bottom;

        var svg = d3.select("#fig04");

        var centerX = width / 2;
        var boxWidth = 100;

        sepalLengths = xs.map(d => Number(d.sepalLength));

        xStats = boxPlotStats(sepalLengths);

        var yScl = d3.scaleLinear()
            .domain([xStats.min - 2, xStats.max + 2])
            .nice()
            .range([height, 0]);
        var yAxs = d3.axisLeft(yScl).ticks(6);

        svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .call(yAxs);

        svg.append("line")
            .attr("x1", centerX)
            .attr("x2", centerX)
            .attr("y1", yScl(xStats.min))
            .attr("y2", yScl(xStats.max))
            .attr("stroke", "black");

        svg.append("rect")
            .attr("x", centerX - boxWidth / 2)
            .attr("y", yScl(xStats.q3))
            .attr("height", (yScl(xStats.q1) - yScl(xStats.q3)))
            .attr("width", boxWidth)
            .attr("stroke", "black")
            .style("fill", "white");

        svg.selectAll("toto")
            .data([xStats.q2])
            .enter()
            .append("line")
            .attr("x1", centerX - boxWidth / 2)
            .attr("x2", centerX + boxWidth / 2)
            .attr("y1", d => yScl(d))
            .attr("y2", d => yScl(d))
            .attr("stroke", "black");

        svg.selectAll("toto")
            .data([xStats.min, xStats.max])
            .enter()
            .append("line")
            .attr("x1", centerX - boxWidth / 5)
            .attr("x2", centerX + boxWidth / 5)
            .attr("y1", d => yScl(d))
            .attr("y2", d => yScl(d))
            .attr("stroke", "black");

        svg.append("text")
            .attr("text-anchor", "middle")
            .attr("transform", "rotate(-90)")
            .attr("x", -height/2)
            .attr("y", margin.left/2)
            .text("Sepal Length");
    });
}
