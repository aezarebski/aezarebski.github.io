function makeFig01() {
    d3.csv("iris.csv").then((data) => {

        var margin = { top: 10, right: 30, bottom: 50, left: 60 };
        var width = 460 - margin.left - margin.right;
        var height = 400 - margin.top - margin.bottom;

        var x = d3.scaleLinear()
            .domain(d3.extent(data, d => Number(d.sepalLength)))
            .range([ 0, width ]);

        var y = d3.scaleLinear()
            .domain(d3.extent(data, d => Number(d.petalLength)))
            .range([ height, 0]);

        var colourScale = d3.scaleOrdinal()
            .domain(data.map(d => d.species))
            .range(d3.schemeCategory10);

        var fig = d3.select("#fig01")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");

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
    });
};
