from paraview.simple import LoadState, Render, SaveScreenshot

LoadState("pvstate.pvsm")
Render()
SaveScreenshot(
    filename="function.png",
    ImageResolution=(2426, 1660),
    TransparentBackground=1
)
