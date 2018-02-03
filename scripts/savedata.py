# Generated using paraview version `5.4.1-1307-gb15223f`

# This script simply saves out pvtu files from the
# simulation dataset for chosen timesteps. The options below
# can be used to change the defaults.
#--------------------------------------------------------------

# Path to directory where all output files are dumped.
output_dir = "/tmp/output/rawdata"

# To write every N'th timestep, change this to `N`, where `N` is a +'ve integer.
write_frequency = 1

#--------------------------------------------------------------
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
      # setup the data processing pipelines
      # ----------------------------------------------------------------

      # trace generated using paraview version 5.4.1-1307-gb15223f

      #### disable automatic camera reset on 'Show'
      paraview.simple._DisableFirstRenderCameraReset()

      # create a new 'XML Unstructured Grid Reader'
      # create a producer from a simulation input
      sPH_Pointsvtu = coprocessor.CreateProducer(datadescription, 'input')

      # create a new 'Parallel UnstructuredGrid Writer'
      parallelUnstructuredGridWriter1 = servermanager.writers.XMLPUnstructuredGridWriter(Input=sPH_Pointsvtu)

      # register the writer with coprocessor
      # and provide it with information such as the filename to use,
      # how frequently to write the data, etc.
      fname = output_dir + "/data-%t.pvtu"
      coprocessor.RegisterWriter(parallelUnstructuredGridWriter1, filename=fname, freq=write_frequency, paddingamount=0)

      # ----------------------------------------------------------------
      # finally, restore active source
      SetActiveSource(parallelUnstructuredGridWriter1)
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
