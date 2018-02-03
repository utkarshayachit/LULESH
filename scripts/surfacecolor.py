# Generated using paraview version 5.4.1-1307-gb15223f

# This script saves out rendering with surface colored by velocity magnitude
# The options below can be used to change defaults.
#--------------------------------------------------------------

# Path to directory where all output files are dumped.
output_dir = "/tmp/output/surfaceplots"

# To write every N'th timestep, change this to `N`, where `N` is a +'ve integer.
write_frequency = 5

#--------------------------------------------------------------
from paraview.simple import *
from paraview import coprocessing

# ensure output directory exits
import os
try:
    os.makedirs(output_dir)
except OSError:
    pass

# This is used to avoid data conversion warnings.
# Presently, scalar coloring filter needs to be converted to avoid
# required data conversion from SOA to AOS arrays.
os.environ["VTK_SILENCE_GET_VOID_POINTER_WARNINGS"] = "1"

#--------------------------------------------------------------
# Code generated from cpstate.py to create the CoProcessor.

#--------------------------------------------------------------
# Global screenshot output options
imageFileNamePadding=0
rescale_lookuptable=True


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

      # Create a new 'Render View'
      renderView1 = CreateView('RenderView')
      renderView1.ViewSize = [800, 600]
      renderView1.AxesGrid = 'GridAxes3DActor'
      renderView1.CenterOfRotation = [0.5625, 0.5625, 0.5625]
      renderView1.CameraPosition = [-2.0629262355442965, -2.0796735752002924, -1.138800264456351]
      renderView1.CameraFocalPoint = [0.2788758743398502, 0.3354912810455095, 0.5503036415498939]
      renderView1.CameraViewUp = [0.3257081428618759, 0.3090901367960047, -0.8935197216675718]
      renderView1.CameraParallelScale = 0.9742785792574935
      renderView1.Background = [0.32, 0.34, 0.43]
      renderView1.UseGradientBackground = 1

      # register the view with coprocessor
      # and provide it with information such as the filename to use,
      # how frequently to write the images, etc.
      fname = output_dir + '/surface_velocity_%t.png'
      coprocessor.RegisterView(renderView1,
          filename=fname, freq=write_frequency, fittoscreen=0, magnification=1, width=800, height=600, cinema={})
      renderView1.ViewTime = datadescription.GetTime()

      # ----------------------------------------------------------------
      # restore active view
      SetActiveView(renderView1)
      # ----------------------------------------------------------------

      # ----------------------------------------------------------------
      # setup the data processing pipelines
      # ----------------------------------------------------------------

      # create a new 'XML Partitioned Unstructured Grid Reader'
      # create a producer from a simulation input
      data = coprocessor.CreateProducer(datadescription, 'input')

      # create a new 'Annotate Attribute Data'
      annotateAttributeData1 = AnnotateAttributeData(Input=data)
      annotateAttributeData1.ArrayName = 'cycle'
      annotateAttributeData1.Prefix = 'cycle: '

      # create a new 'Annotate Attribute Data'
      annotateAttributeData2 = AnnotateAttributeData(Input=data)
      annotateAttributeData2.ArrayName = 'time'
      annotateAttributeData2.Prefix = 'time: '

      # ----------------------------------------------------------------
      # setup the visualization in view 'renderView1'
      # ----------------------------------------------------------------

      # show data from data
      dataDisplay = Show(data, renderView1)

      # get color transfer function/color map for 'velocity'
      velocityLUT = GetColorTransferFunction('velocity')
      velocityLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 375.46432803263104, 0.865003, 0.865003, 0.865003, 750.9286560652621, 0.705882, 0.0156863, 0.14902]
      velocityLUT.ScalarRangeInitialized = 1.0

      # trace defaults for the display properties.
      dataDisplay.Representation = 'Surface With Edges'
      dataDisplay.ColorArrayName = ['POINTS', 'velocity']
      dataDisplay.LookupTable = velocityLUT

      # show data from annotateAttributeData1
      annotateAttributeData1Display = Show(annotateAttributeData1, renderView1)

      # trace defaults for the display properties.
      annotateAttributeData1Display.FontSize = 10
      annotateAttributeData1Display.Position = [0.01, 0.965]

      # show data from annotateAttributeData2
      annotateAttributeData2Display = Show(annotateAttributeData2, renderView1)

      # trace defaults for the display properties.
      annotateAttributeData2Display.FontSize = 10
      annotateAttributeData2Display.WindowLocation = 'UpperRightCorner'
      annotateAttributeData2Display.Position = [0.0125, 0.931667]

      # setup the color legend parameters for each legend in this view

      # get color legend/bar for velocityLUT in view renderView1
      velocityLUTColorBar = GetScalarBar(velocityLUT, renderView1)
      velocityLUTColorBar.Orientation = 'Horizontal'
      velocityLUTColorBar.WindowLocation = 'AnyLocation'
      velocityLUTColorBar.Position = [0.3377449168207022, 0.09479289940828395]
      velocityLUTColorBar.Title = 'velocity'
      velocityLUTColorBar.ComponentTitle = 'Magnitude'
      velocityLUTColorBar.TitleFontFile = ''
      velocityLUTColorBar.LabelFontFile = ''
      velocityLUTColorBar.ScalarBarLength = 0.3299999999999996

      # set color bar visibility
      velocityLUTColorBar.Visibility = 1

      # show color legend
      dataDisplay.SetScalarBarVisibility(renderView1, True)

      # ----------------------------------------------------------------
      # setup color maps and opacity mapes used in the visualization
      # note: the Get..() functions create a new object, if needed
      # ----------------------------------------------------------------

      # ----------------------------------------------------------------
      # finally, restore active source
      SetActiveSource(annotateAttributeData1)
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
