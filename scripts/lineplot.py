# Generated using paraview version 5.4.1-1307-gb15223f

# This script saves out line plot for velocity magnitude
# The options below can be used to change defaults.
#--------------------------------------------------------------

# Path to directory where all output files are dumped.
output_dir = "/tmp/output/lineplots"

# To write every N'th timestep, change this to `N`, where `N` is a +'ve integer.
write_frequency = 1

from paraview.simple import *
from paraview import coprocessing

# ensure output directory exits
import os
try:
    os.makedirs(output_dir)
except OSError:
    pass

#--------------------------------------------------------------
# Code generated from cpstate.py to create the CoProcessor.
# paraview version 5.4.1-1307-gb15223f

#--------------------------------------------------------------
# Global screenshot output options
imageFileNamePadding=0
rescale_lookuptable=False

# ----------------------- CoProcessor definition -----------------------

def CreateCoProcessor():
  global output_dir, write_frequency
  def _CreatePipeline(coprocessor, datadescription):
    class Pipeline:
      # state file generated using paraview version 5.4.1-1307-gb15223f

      # ----------------------------------------------------------------
      # setup views used in the visualization
      # ----------------------------------------------------------------

      # trace generated using paraview version 5.4.1-1307-gb15223f

      #### disable automatic camera reset on 'Show'
      paraview.simple._DisableFirstRenderCameraReset()

      # Create a new 'Line Chart View'
      lineChartView1 = CreateView('XYChartView')
      lineChartView1.ViewSize = [800, 600]
      lineChartView1.ChartTitle = 'Plot Over Line (time=${TIME})'
      lineChartView1.ChartTitleFontFile = ''
      lineChartView1.LeftAxisTitle = 'velocity magnitude'
      lineChartView1.LeftAxisTitleFontFile = ''
      lineChartView1.LeftAxisUseCustomRange = 1
      lineChartView1.LeftAxisRangeMaximum = 1500.0
      lineChartView1.LeftAxisLabelFontFile = ''
      lineChartView1.BottomAxisTitleFontFile = ''
      lineChartView1.BottomAxisRangeMaximum = 2.0
      lineChartView1.BottomAxisLabelFontFile = ''
      lineChartView1.RightAxisRangeMaximum = 6.66
      lineChartView1.RightAxisLabelFontFile = ''
      lineChartView1.TopAxisTitleFontFile = ''
      lineChartView1.TopAxisRangeMaximum = 6.66
      lineChartView1.TopAxisLabelFontFile = ''

      # register the view with coprocessor
      # and provide it with information such as the filename to use,
      # how frequently to write the images, etc.
      fname = output_dir + "/lineplot_%t.png"
      coprocessor.RegisterView(lineChartView1,
          filename=fname, freq=write_frequency, fittoscreen=0, magnification=1, width=800, height=600, cinema={})
      lineChartView1.ViewTime = datadescription.GetTime()

      # ----------------------------------------------------------------
      # restore active view
      SetActiveView(lineChartView1)
      # ----------------------------------------------------------------

      # ----------------------------------------------------------------
      # setup the data processing pipelines
      # ----------------------------------------------------------------

      # create a new 'XML Partitioned Unstructured Grid Reader'
      # create a producer from a simulation input
      data = coprocessor.CreateProducer(datadescription, 'input')

      # create a new 'Plot Over Line'
      plotOverLine1 = PlotOverLine(Input=data,
          Source='High Resolution Line Source')

      # init the 'High Resolution Line Source' selected for 'Source'
      plotOverLine1.Source.Point2 = [1.125, 1.125, 1.125]

      # ----------------------------------------------------------------
      # setup the visualization in view 'lineChartView1'
      # ----------------------------------------------------------------

      # show data from plotOverLine1
      plotOverLine1Display = Show(plotOverLine1, lineChartView1)

      # trace defaults for the display properties.
      plotOverLine1Display.CompositeDataSetIndex = [0]
      plotOverLine1Display.UseIndexForXAxis = 0
      plotOverLine1Display.XArrayName = 'arc_length'
      plotOverLine1Display.SeriesVisibility = ['velocity_Magnitude']
      plotOverLine1Display.SeriesLabel = ['acceleration_X', 'acceleration_X', 'acceleration_Y', 'acceleration_Y', 'acceleration_Z', 'acceleration_Z', 'acceleration_Magnitude', 'acceleration_Magnitude', 'arc_length', 'arc_length', 'artificial-viscosity', 'artificial-viscosity', 'element-mass', 'element-mass', 'energy', 'energy', 'force_X', 'force_X', 'force_Y', 'force_Y', 'force_Z', 'force_Z', 'force_Magnitude', 'force_Magnitude', 'nodal-mass', 'nodal-mass', 'pressure', 'pressure', 'relative-volume', 'relative-volume', 'sound-speed', 'sound-speed', 'velocity_X', 'velocity_X', 'velocity_Y', 'velocity_Y', 'velocity_Z', 'velocity_Z', 'velocity_Magnitude', 'velocity_Magnitude', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']
      plotOverLine1Display.SeriesColor = ['acceleration_X', '0', '0', '0', 'acceleration_Y', '0.889998', '0.100008', '0.110002', 'acceleration_Z', '0.220005', '0.489998', '0.719997', 'acceleration_Magnitude', '0.300008', '0.689998', '0.289998', 'arc_length', '0.6', '0.310002', '0.639994', 'artificial-viscosity', '1', '0.500008', '0', 'element-mass', '0.650004', '0.340002', '0.160006', 'energy', '0', '0', '0', 'force_X', '0.889998', '0.100008', '0.110002', 'force_Y', '0.220005', '0.489998', '0.719997', 'force_Z', '0.300008', '0.689998', '0.289998', 'force_Magnitude', '0.6', '0.310002', '0.639994', 'nodal-mass', '1', '0.500008', '0', 'pressure', '0.650004', '0.340002', '0.160006', 'relative-volume', '0', '0', '0', 'sound-speed', '0.889998', '0.100008', '0.110002', 'velocity_X', '0.220005', '0.489998', '0.719997', 'velocity_Y', '0.300008', '0.689998', '0.289998', 'velocity_Z', '0.6', '0.310002', '0.639994', 'velocity_Magnitude', '1', '0.500008', '0', 'vtkValidPointMask', '0.650004', '0.340002', '0.160006', 'Points_X', '0', '0', '0', 'Points_Y', '0.889998', '0.100008', '0.110002', 'Points_Z', '0.220005', '0.489998', '0.719997', 'Points_Magnitude', '0.300008', '0.689998', '0.289998']
      plotOverLine1Display.SeriesPlotCorner = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'acceleration_Magnitude', '0', 'acceleration_X', '0', 'acceleration_Y', '0', 'acceleration_Z', '0', 'arc_length', '0', 'artificial-viscosity', '0', 'element-mass', '0', 'energy', '0', 'force_Magnitude', '0', 'force_X', '0', 'force_Y', '0', 'force_Z', '0', 'nodal-mass', '0', 'pressure', '0', 'relative-volume', '0', 'sound-speed', '0', 'velocity_Magnitude', '0', 'velocity_X', '0', 'velocity_Y', '0', 'velocity_Z', '0', 'vtkValidPointMask', '0']
      plotOverLine1Display.SeriesLabelPrefix = ''
      plotOverLine1Display.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'acceleration_Magnitude', '1', 'acceleration_X', '1', 'acceleration_Y', '1', 'acceleration_Z', '1', 'arc_length', '1', 'artificial-viscosity', '1', 'element-mass', '1', 'energy', '1', 'force_Magnitude', '1', 'force_X', '1', 'force_Y', '1', 'force_Z', '1', 'nodal-mass', '1', 'pressure', '1', 'relative-volume', '1', 'sound-speed', '1', 'velocity_Magnitude', '1', 'velocity_X', '1', 'velocity_Y', '1', 'velocity_Z', '1', 'vtkValidPointMask', '1']
      plotOverLine1Display.SeriesLineThickness = ['Points_Magnitude', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'acceleration_Magnitude', '2', 'acceleration_X', '2', 'acceleration_Y', '2', 'acceleration_Z', '2', 'arc_length', '2', 'artificial-viscosity', '2', 'element-mass', '2', 'energy', '2', 'force_Magnitude', '2', 'force_X', '2', 'force_Y', '2', 'force_Z', '2', 'nodal-mass', '2', 'pressure', '2', 'relative-volume', '2', 'sound-speed', '2', 'velocity_Magnitude', '2', 'velocity_X', '2', 'velocity_Y', '2', 'velocity_Z', '2', 'vtkValidPointMask', '2']
      plotOverLine1Display.SeriesMarkerStyle = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'acceleration_Magnitude', '0', 'acceleration_X', '0', 'acceleration_Y', '0', 'acceleration_Z', '0', 'arc_length', '0', 'artificial-viscosity', '0', 'element-mass', '0', 'energy', '0', 'force_Magnitude', '0', 'force_X', '0', 'force_Y', '0', 'force_Z', '0', 'nodal-mass', '0', 'pressure', '0', 'relative-volume', '0', 'sound-speed', '0', 'velocity_Magnitude', '0', 'velocity_X', '0', 'velocity_Y', '0', 'velocity_Z', '0', 'vtkValidPointMask', '0']

      # ----------------------------------------------------------------
      # finally, restore active source
      SetActiveSource(plotOverLine1)
      # ----------------------------------------------------------------
    return Pipeline()

  class CoProcessor(coprocessing.CoProcessor):
    def CreatePipeline(self, datadescription):
      self.Pipeline = _CreatePipeline(self, datadescription)

  coprocessor = CoProcessor()
  # these are the frequencies at which the coprocessor updates.
  freqs = {'input': [write_frequency]}
  coprocessor.SetUpdateFrequencies(freqs)
  return coprocessor


#--------------------------------------------------------------
# Global variable that will hold the pipeline for each timestep
# Creating the CoProcessor object, doesn't actually create the ParaView pipeline.
# It will be automatically setup when coprocessor.UpdateProducers() is called the
# first time.
coprocessor = CreateCoProcessor()

#--------------------------------------------------------------
# Enable Live-Visualizaton with ParaView and the update frequency
coprocessor.EnableLiveVisualization(False, 1)

# ---------------------- Data Selection method ----------------------

def RequestDataDescription(datadescription):
    "Callback to populate the request for current timestep"
    global coprocessor
    if datadescription.GetForceOutput() == True:
        # We are just going to request all fields and meshes from the simulation
        # code/adaptor.
        for i in range(datadescription.GetNumberOfInputDescriptions()):
            datadescription.GetInputDescription(i).AllFieldsOn()
            datadescription.GetInputDescription(i).GenerateMeshOn()
        return

    # setup requests for all inputs based on the requirements of the
    # pipeline.
    coprocessor.LoadRequestedData(datadescription)

# ------------------------ Processing method ------------------------

def DoCoProcessing(datadescription):
    "Callback to do co-processing for current timestep"
    global coprocessor

    # Update the coprocessor by providing it the newly generated simulation data.
    # If the pipeline hasn't been setup yet, this will setup the pipeline.
    coprocessor.UpdateProducers(datadescription)

    # Write output data, if appropriate.
    coprocessor.WriteData(datadescription);

    # Write image capture (Last arg: rescale lookup table), if appropriate.
    coprocessor.WriteImages(datadescription, rescale_lookuptable=rescale_lookuptable,
        image_quality=0, padding_amount=imageFileNamePadding)

    # Live Visualization, if enabled.
    coprocessor.DoLiveVisualization(datadescription, "localhost", 22222)
