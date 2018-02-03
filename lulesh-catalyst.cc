#include "lulesh.h"

#include <vtkAOSDataArrayTemplate.h>
#include <vtkCellArray.h>
#include <vtkCellData.h>
#include <vtkCPDataDescription.h>
#include <vtkCPInputDataDescription.h>
#include <vtkCPProcessor.h>
#include <vtkCPPythonScriptPipeline.h>
#include <vtkNew.h>
#include <vtkNew.h>
#include <vtkPointData.h>
#include <vtkPoints.h>
#include <vtkSmartPointer.h>
#include <vtkSOADataArrayTemplate.h>
#include <vtkUnstructuredGrid.h>
#if USE_MPI
#include <vtkMPI.h>
#endif

namespace detail
{
  static vtkSmartPointer<vtkUnstructuredGrid> Mesh;

  template <typename T>
  vtkDataArray* _addField(vtkDataSetAttributes* dsa, const char* name, T* x, T* y, T* z, Index_t numItems)
  {
    vtkNew<vtkSOADataArrayTemplate<T> > array;
    array->SetName(name);
    array->SetNumberOfComponents(3);
    array->SetArray(0, x, numItems, true, true);
    array->SetArray(1, y, numItems, true, true);
    array->SetArray(2, z, numItems, true, true);
    dsa->AddArray(array);
    return array;
  }

  template <typename T>
  vtkDataArray* _addField(vtkDataSetAttributes* dsa, const char* name, T* x, Index_t numItems)
  {
    vtkNew<vtkSOADataArrayTemplate<T> > array;
    array->SetName(name);
    array->SetNumberOfComponents(1);
    array->SetArray(0, x, numItems, true, true);
    dsa->AddArray(array);
    return array;
  }

  vtkSmartPointer<vtkUnstructuredGrid> getMesh(Domain& domain)
  {
    // since mesh doesn't change over time, we create it the first time
    // this method is called.
    if (Mesh == nullptr)
    {
      vtkNew<vtkUnstructuredGrid> ug;

      // Add points (zero-copy)
      vtkNew<vtkSOADataArrayTemplate<Real_t> > pointsArray;
      pointsArray->SetNumberOfComponents(3);
      pointsArray->SetArray(0, domain.x(), domain.numNode(), true, true);
      pointsArray->SetArray(1, domain.y(), domain.numNode(), true, true);
      pointsArray->SetArray(2, domain.z(), domain.numNode(), true, true);

      vtkNew<vtkPoints> pts;
      pts->SetData(pointsArray);
      ug->SetPoints(pts);

      // Add connectivity (deep copy)
      vtkNew<vtkCellArray> cellArray;
      cellArray->Allocate(domain.numElem()*8);
      for (Index_t elem=0; elem < domain.numElem(); ++elem)
      {
        const Index_t *nodeIds = domain.nodelist(elem);
        cellArray->InsertNextCell(8);
        for (int cc=0; cc < 8; ++cc)
        {
          cellArray->InsertCellPoint(nodeIds[cc]);
        }
      }
      ug->SetCells(VTK_HEXAHEDRON, cellArray);

      // add node-centered fields.
      auto pd = ug->GetPointData();
      _addField(pd, "velocity", domain.xd(), domain.yd(), domain.zd(), domain.numNode());
      _addField(pd, "acceleration", domain.xdd(), domain.ydd(), domain.zdd(), domain.numNode());
      _addField(pd, "force", domain.fx(), domain.fy(), domain.fz(), domain.numNode());
      _addField(pd, "nodal-mass", domain.nodalMass(), domain.numNode());

      auto cd = ug->GetCellData();
      _addField(cd, "energy", domain.e(), domain.numElem());
      _addField(cd, "pressure", domain.p(), domain.numElem());
      _addField(cd, "artificial-viscosity", domain.q(), domain.numElem());
      _addField(cd, "relative-volume", domain.v(), domain.numElem());
      _addField(cd, "sound-speed", domain.ss(), domain.numElem());
      _addField(cd, "element-mass", domain.elemMass(), domain.numElem());


      Mesh = ug;
    }
    // since mesh geometry changes every timestep, ensure we let VTK know.
    Mesh->GetPoints()->GetData()->Modified();
    return Mesh;
  }

  void update(Domain& domain, vtkUnstructuredGrid* mesh)
  {
    // since the zero-copied array could have been modified, we simply call
    // `Modified` on all VTK-array so things like ranges etc are recomputed.
    mesh->GetPoints()->GetData()->Modified();
    mesh->GetPoints()->Modified();
    for (int cc=0; cc < mesh->GetPointData()->GetNumberOfArrays(); ++cc)
    {
      mesh->GetPointData()->GetArray(cc)->Modified();
    }
    for (int cc=0; cc < mesh->GetCellData()->GetNumberOfArrays(); ++cc)
    {
      mesh->GetCellData()->GetArray(cc)->Modified();
    }

    // add field data for cycle and time.
    vtkNew<vtkAOSDataArrayTemplate<Int_t>> cycleArray;
    cycleArray->SetName("cycle");
    cycleArray->SetNumberOfComponents(1);
    cycleArray->SetNumberOfTuples(1);
    cycleArray->SetTypedComponent(0, 0, domain.cycle());

    vtkNew<vtkAOSDataArrayTemplate<Real_t>> timeArray;
    timeArray->SetName("time");
    timeArray->SetNumberOfComponents(1);
    timeArray->SetNumberOfTuples(1);
    timeArray->SetTypedComponent(0, 0, domain.time());

    mesh->GetFieldData()->AddArray(cycleArray);
    mesh->GetFieldData()->AddArray(timeArray);
  }

  void initialize()
  {
    Mesh = nullptr;
  }

  void finalize()
  {
    Mesh = nullptr;
  }
}


namespace adaptor
{
static vtkSmartPointer<vtkCPProcessor> Processor;

void initialize(int rank, int numranks, const std::vector<std::string>& scripts)
{
  detail::initialize();
  if (scripts.size() == 0)
  {
    cout << "no catalyst scripts specified. skipping catalyst." << endl;
  }
  else
  {
    if (Processor == nullptr)
    {
      Processor = vtkSmartPointer<vtkCPProcessor>::New();
#if USE_MPI
      MPI_Comm world = MPI_COMM_WORLD;
      vtkMPICommunicatorOpaqueComm comm(&world);
      Processor->Initialize(comm);
#else
      Processor->Initialize();
#endif
    }
    for (const std::string& ascript: scripts)
    {
      vtkNew<vtkCPPythonScriptPipeline> apipeline;
      apipeline->Initialize(ascript.c_str());
      Processor->AddPipeline(apipeline);
    }
  }
}

void process(Domain& domain)
{
  if (Processor)
  {
    vtkNew<vtkCPDataDescription> dataDescription;
    dataDescription->AddInput("input");
    dataDescription->SetTimeData(domain.time(), domain.cycle());
    if (Processor->RequestDataDescription(dataDescription) != 0)
    {
      auto mesh = detail::getMesh(domain);
      detail::update(domain, mesh);
      dataDescription->GetInputDescriptionByName("input")->SetGrid(mesh);
      Processor->CoProcess(dataDescription);
    }
  }
}

void finalize()
{
  detail::finalize();
  if (Processor)
  {
    Processor->Finalize();
    Processor = nullptr;
  }
}

}
