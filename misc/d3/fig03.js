function makeFig03() {
    d3.json("network.json")
        .then(res => {
            var svg = d3.select("#fig03");
            var colScale = d3.scaleOrdinal(d3.schemePastel1);

            // Randomly permuting the data means that each time a different
            // layout is achieved.
            d3.shuffle(res.ps);
            d3.shuffle(res.ln);

            // The names associated with the forces do not seem to matter.
            // Understanding the API for the forces is a bit tricky, but there
            // is documentation on GitHub.
            d3.forceSimulation( res.ps )
                .force("centering", d3.forceCenter(230, 200))
                .force("links", d3.forceLink(res.ln).distance(50).id(d => d.id))
                .force("collision", d3.forceCollide(10))
                .force("many", d3.forceManyBody().strength(-500))
                .on("end", function () {

                    svg.selectAll("line")
                        .data(res.ln)
                        .enter()
                        .append("line")
                        .attr("stroke", "black")
                        .attr("x1", d=>d.source.x)
                        .attr("y1", d=>d.source.y)
                        .attr("x2", d => d.target.x)
                        .attr("y2", d => d.target.y);

                    svg.selectAll("circle")
                        .data(res.ps)
                        .enter()
                        .append("circle")
                        .attr("r", 10)
                        .attr("fill", (d, i) => colScale(i % 3))
                        .attr("cx", d => d.x)
                        .attr("cy", d => d.y);

                    svg.selectAll("text")
                        .data(res.ps)
                        .enter()
                        .append("text")
                        .attr("x", d => d.x)
                        .attr("y", d => d.y + 4)
                        .attr("text-anchor", "middle")
                        .attr("font-size", 10)
                        .text(d => d.id);
                });
        });
}
