function makeFig01() {
    var margin = { top: 10, right: 30, bottom: 50, left: 60 };
    var width = 460 - margin.left - margin.right;
    var height = 400 - margin.top - margin.bottom;

    var fig = d3.select("#fig01")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    d3.csv("iris.csv").then((data) => {

        var x = d3.scaleLinear()
            .domain(d3.extent(data, d => Number(d.sepalLength)))
            .range([ 0, width ]);

        var y = d3.scaleLinear()
            .domain(d3.extent(data, d => Number(d.petalLength)))
            .range([ height, 0]);

        var colourScale = d3.scaleOrdinal()
            .domain(data.map(d => d.species))
            .range(d3.schemeCategory10);

        fig.append("g")
            .attr("transform", "translate(" + 0 + "," + height + ")")
            .call(d3.axisBottom(x));

        fig.append("g")
            .call(d3.axisLeft(y));

        fig.selectAll("circle")
            .data(data)
            .enter().append("circle")
            .attr("cx", d => x(Number(d.sepalLength)))
            .attr("cy", d => y(Number(d.petalLength)))
            .attr("r", 2)
            .style("fill", d => colourScale(d.species));

        fig.append("text")
            .attr("text-anchor", "end")
            .attr("transform", "rotate(-90)")
            .attr("x", -height/2 + margin.bottom)
            .attr("y", -margin.left/2)
            .text("Petal Length");

        fig.append("text")
            .attr("text-anchor", "end")
            .attr("x", width/2 + margin.left)
            .attr("y", height + margin.top + margin.bottom/2)
            .text("Sepal Length");

        // The following annotation code needs to be done in here to prevent the
        // function returning too early.

        // We set up an object to compute a natural curve connecting the
        // specified points and then append this as a path element so it is
        // drawn.
        const curve = d3.line().curve(d3.curveNatural);
        const points = [
            [x(5.0), y(2.0)],
            [x(0.5*(6.5+5.0)-0.2), y(2.5+0.6)],
            [x(6.5), y(3.0)]
        ];
        fig.append("path")
            .attr("d", curve(points))
            .attr("stroke", "darkgreen")
            .style("stroke-width", "2px")
            .attr("fill", "none");

        // The text annotation is a bit boring, but this demonstrates how you
        // might go about making it a bit more interesting and tweaking the
        // appearance.
        var yRect = 3.5;

        fig.append("a")
            .attr("xlink:href", "https://en.wikipedia.org/wiki/Doge_(meme)")
            .append("rect")
            .attr("x", x(6.5))
            .attr("y", y(yRect))
            .attr("width", x(8.1) - x(6.5))
            .attr("height", y(yRect) - y(yRect + 1.0))
            .style("fill", "lightgreen")
            .attr("rx", 10)
            .attr("ry", 10)
            .attr("stroke", "darkgreen")
            .attr("stroke-width", "2px");

        fig.append("text")
            .attr("text-anchor", "start")
            .attr("x", x(6.5 + 0.1))
            .attr("y", y(3.0 - 0.1))
            .style("fill", "darkgreen")
            .style("font-size", "18px")
            .style("font-style", "italic")
            .text("Wow! Click Me!");

    });
};
