// Define dimensions
const width = 900, height = 600;
const linkLength = 200;

// Default opacity
const defaultOpacity = 0.3;

// Create an SVG element and a group for the visualization content.
const svg = d3.select("body")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .style("border", "1px solid black")
      .call(d3.zoom().on("zoom", zoomed));

const g = svg.append("g");

// Load JSON data
d3.json("data.json").then(data => {
    const simulation = d3.forceSimulation(data.nodes)
          .force("link", d3.forceLink(data.links).id(d => d.id).distance(linkLength))
          .force("charge", d3.forceManyBody().strength(-800))
          .force("center", d3.forceCenter(width / 2, height / 2));

    const link = g.append("g")
          .attr("class", "links")
          .selectAll("line")
          .data(data.links)
          .enter().append("line")
          .attr("class", "link")
          .style("stroke-opacity", defaultOpacity);

    const node = g.append("g")
          .attr("class", "nodes")
          .selectAll("circle")
          .data(data.nodes)
          .enter().append("circle")
          .attr("class", "node")
          .attr("r", 10)
          .style("fill", "grey")
          .style("opacity", defaultOpacity)
          .on("mouseover", function(event, d) {
              const neighbors = new Set(data.links.filter(l => l.source.id === d.id || l.target.id === d.id)
                                        .flatMap(l => [l.source.id, l.target.id]));
              neighbors.add(d.id);

              node.style("opacity", n => neighbors.has(n.id) ? 1 : defaultOpacity);
              link.style("stroke-opacity", l => neighbors.has(l.source.id) && neighbors.has(l.target.id) ? 1 : defaultOpacity);

              const xPosition = event.pageX + 5;
              const yPosition = event.pageY + 5;

              d3.select("#tooltip")
                  .style("left", xPosition + "px")
                  .style("top", yPosition + "px")
                  .style("opacity", 1);

              d3.select("#tooltip-title").text(d.title);
              d3.select("#tooltip-year").text(d.year);
              d3.select("#tooltip-first-author").text(d.first_author);
              d3.select("#tooltip-doi")
                  .attr("href", "https://doi.org/" + d.doi)
                  .text(d.doi);
          })
          .on("mouseout", function() {
              node.style("opacity", defaultOpacity);
              link.style("stroke-opacity", defaultOpacity);

              setTimeout(() => {
                  if (!d3.select("#tooltip").classed("hovered")) {
                      d3.select("#tooltip")
                          .style("opacity", 0)
                          .style("left", "-9999px");  // Move off-screen
                  }
              }, 1000);  // 1 second delay
          })
          .on("click", function(event, d) {
              addToTooltipList(d);
          });

    d3.select("#tooltip")
        .on("mouseover", function() {
            d3.select(this).classed("hovered", true);
        })
        .on("mouseout", function() {
            d3.select(this).classed("hovered", false);
            setTimeout(() => {
                if (!d3.select(this).classed("hovered")) {
                    d3.select(this)
                        .style("opacity", 0)
                        .style("left", "-9999px");  // Move off-screen
                }
            }, 1000);  // 1 second delay
        });

    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
    });
});

// Zoom function
function zoomed(event) {
    g.attr("transform", event.transform);
}

function addToTooltipList(nodeData) {
    var tooltipItems = document.getElementById("tooltipItems");
    var listItem = document.createElement("li");
    listItem.innerHTML = `
        <strong>Title:</strong> ${nodeData.title}<br>
        <strong>Year:</strong> ${nodeData.year}<br>
        <strong>First Author:</strong> ${nodeData.first_author}<br>
        <strong>DOI:</strong> <a href="https://doi.org/${nodeData.doi}" target="_blank">${nodeData.doi}</a><br>
        <strong>Keywords:</strong> ${nodeData.keywords}
    `;
    tooltipItems.appendChild(listItem);
}
