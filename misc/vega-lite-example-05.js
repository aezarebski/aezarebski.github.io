const dataCsv = "https://aezarebski.github.io/misc/vega-lite-data-02.csv"

const chartSpec = vl
      .markPoint()
      .data(dataCsv)
      .encode(
          vl.x().fieldQ("demoX"),
          vl.y().fieldQ("demoY"),
          vl.color().fieldN("demoColour")
      ).toJSON();

vegaEmbed('#vis', chartSpec);
