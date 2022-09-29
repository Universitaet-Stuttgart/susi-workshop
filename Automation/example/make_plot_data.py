from paraview.simple import XMLImageDataReader, PlotOverLine, CreateWriter

function = XMLImageDataReader(FileName="result.vti")

plot = PlotOverLine(Input=function)
plot.Resolution = 2000
plot.Point1 = [0, 0, 0]
plot.Point2 = [250, 250, 0]

writer = CreateWriter("plot_data.csv", plot)
writer.UpdatePipeline()
