function makeFig02() {
    d3.csv("population-and-demography.csv")
        .then( function( data ) {

            const marginBig = 100;
            const marginSmall = 30;
            const width = 460 - marginBig;
            const height = 400 - marginSmall;

            var x = d3.scaleLinear()
                .domain(d3.extent(data, d => d.Year))
                .nice()
                .range([marginBig, width + marginBig - marginSmall]);

            // We format the dates so that they do not put a comma in the year
            // which looks weird.
            var xAxis = d3.axisBottom(x)
                .tickFormat(d3.format("d"));

            var y = d3.scaleLinear()
                .domain(d3.extent(data, d => d.Population))
                .nice()
                .range([height, marginSmall]);

            // We call the ticks method so that a sensible number of points are
            // used in the figure.
            var yAxis = d3.axisLeft(y).ticks(4);

            var fig = d3.select("#fig02");

            fig.append("g")
                .attr("transform", "translate(" + 0 + "," + (height + 10) + ")")
                .call(xAxis);

            fig.append("g")
                .attr("transform", "translate(" + (marginBig - 10) + "," + 0 + ")")
                .call(yAxis);

            var lineMaker = d3.line()
                .x(d => x(d.Year))
                .y(d => y(d.Population));

            fig.append("g")
                .append("path")
                .attr("fill", "none")
                .attr("stroke", "green")
                .attr("d", lineMaker(data));

            fig.append("g")
                .selectAll("circle")
                .data(data)
                .enter()
                .append("circle")
                .attr("r", 5)
                .attr("fill", "red")
                .attr("cx", d => x(d.Year))
                .attr("cy", d => y(d.Population));
        });
}
