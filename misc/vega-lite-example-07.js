const dataUrl07 = "https://aezarebski.github.io/misc/cars.json";

const chartSpec07 = vl
      .markBar()
      .data(dataUrl07)
      .encode(
          vl.x().fieldN("Origin").axis({"title": ""}),
          vl.y().aggregate("count").axis({"grid": false}).title("Frequency"),
          vl.column().fieldO("Cylinders"),
          vl.color().fieldN("Origin")
      )
      .config({})
      .toJSON();

vegaEmbed('#vis07', chartSpec07);
