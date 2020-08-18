const carsUrl = "https://cdn.jsdelivr.net/npm/vega-datasets@1.31.1/data/cars.json"

const mpg = vl
      .markLine()
      .width(300)
      .data(carsUrl)
      .encode(vl.x().fieldT('Year'),
              vl.y().average('Miles_per_Gallon')
              .title("Average miles per gallon")
             );

const hp = vl
      .markPoint()
      .width(500)
      .data(carsUrl)
      .encode(vl.x().fieldT("Year"),
              vl.y().fieldQ('Horsepower'),
              vl.tooltip(["Name", "Origin"]));

const combSpec = vl.hconcat(vl.layer(mpg,
                                     mpg.markCircle()),
                            hp).toJSON();

vegaEmbed('#vis06', combSpec);
