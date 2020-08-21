const weatherCsv = "http://localhost:8000/misc/seattle-weather.csv"

const weatherHeatmap = vl
      .markRect()
      .data(weatherCsv)
      .encode(
          vl.x().timeUnit("date").fieldO("date").title("Day").axis({"format": "%e"}),
          vl.y().timeUnit("month").fieldO("date").title("Month"),
          vl.color().max("temp_max").fieldQ("temp_max").legend({"title": null})
      )
      .width(500)
      .height(400)
      .title("Daily Max Temperatures (C) in Seattle, WA")
      .toJSON();

vegaEmbed("#vis08", weatherHeatmap);
