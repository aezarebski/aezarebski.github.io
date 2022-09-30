function makeFig05() {
    d3.csv("iris.csv").then((data) => {

        var margin = { top: 10, right: 30, bottom: 30, left: 60 };
        var width = 460 - margin.right - margin.left;
        var height = 400 - margin.top - margin.bottom;

        // There is a bit of fuss here to simplify subsequent axis placement.
        var svg = d3.select("#fig05")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");

        var variableNames = [
            "Petal Length",
            "Petal Width",
            "Sepal Length",
            "Sepal Width"
        ];
        var speciesNames = ["setosa", "versicolor", "virginica"];

        var x = d3.scaleBand()
            .range([ 0, width ])
            .domain(variableNames)
            .padding(0.01);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        var y = d3.scaleBand()
            .range([ height, 0 ])
            .domain(speciesNames)
            .padding(0.01);
        svg.append("g")
            .call(d3.axisLeft(y));

        var myColor = d3.scaleLinear()
            .range(["white", "#67a9cf"])
            .domain([0,7]);

        var summary = Array.from(d3.group(data, d => d.species),
                                 ([species, values]) => (
                                     [{species: species,
                                       variable: "Petal Length",
                                       value: d3.mean(values.map(x => Number(x["petalLength"])))},
                                      {species: species,
                                       variable: "Petal Width",
                                       value: d3.mean(values.map(x => Number(x["petalWidth"])))},
                                      {species: species,
                                       variable: "Sepal Length",
                                       value: d3.mean(values.map(x => Number(x["sepalLength"])))},
                                      {species: species,
                                       variable: "Sepal Width",
                                       value: d3.mean(values.map(x => Number(x["sepalWidth"])))},
                                     ])
                                ).flat(1);

        svg.selectAll()
            .data(summary)
            .enter()
            .append("rect")
            .attr("x", d => x(d.variable))
            .attr("y", d => y(d.species))
            .attr("width", x.bandwidth() )
            .attr("height", y.bandwidth() )
            .style("fill", d => myColor(d.value));
    });
}
