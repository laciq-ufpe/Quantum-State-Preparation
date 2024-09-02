from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import UnitaryGate
from math import sqrt
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qiskit import transpile

#Function definition
def createCircuit(nSize):
  x = QuantumRegister(nSize,name='x')
  g = QuantumRegister(nSize-1,name='g')
  c = QuantumRegister(2,name='c')
  meas = ClassicalRegister(nSize)

  qc = QuantumCircuit(x,g,c,meas)
  return qc, x, g, c, meas

def createSgate(states_left):
  matrix = [[1,0,0,0],
            [0,1,0,0],
            [0,0,(sqrt((states_left-1)/states_left)),(-1/sqrt(states_left))],
            [0,0,(1/sqrt(states_left)),(sqrt((states_left-1)/states_left))]]
  gate = UnitaryGate(matrix)
  return gate

def flipStage(qc,x,g,c,currBinaryString,nextBinaryString):
  counter = 0
  qc.x(c[1])
  while(counter < len(currBinaryString)):
    if(currBinaryString[counter] != nextBinaryString[counter]):
      qc.cx(c[1],x[counter])
    counter = counter+1
  qc.cx(c[1],c[0])
  qc.x(c[1])

def saveStage(qc,x,g,c,currBinaryString):
  counterControl = 0
  sizeString = len(currBinaryString)
  while(counterControl < sizeString):
    if(int(currBinaryString[counterControl]) == 0):
      qc.x(x[counterControl])
    counterControl = counterControl + 1


  qc.ccx(x[0],x[1],g[0])

  counterSaveStage = 2

  while(counterSaveStage <= sizeString-1):
    qc.ccx(x[counterSaveStage],g[counterSaveStage - 2],g[counterSaveStage - 1])
    counterSaveStage = counterSaveStage + 1

  qc.cx(g[sizeString-2],c[0])

  counterSaveStage = sizeString - 1

  while(counterSaveStage >= 2):
    qc.ccx(x[counterSaveStage],g[counterSaveStage - 2],g[counterSaveStage - 1])
    counterSaveStage = counterSaveStage - 1

  qc.ccx(x[0],x[1],g[0])

  counterControl = 0
  while(counterControl < sizeString):
    if(int(currBinaryString[counterControl]) == 0):
      qc.x(x[counterControl])
    counterControl = counterControl + 1

#THE FUNCTION
def basisEncoding(qc,x,g,c,binaryString):
  nSize = qc.num_qubits -1
  counter = len(binaryString) - 2
  while(counter >= 0):
    #flipStageGen2
    flipStage(qc,x,g,c,binaryString[counter],binaryString[counter+1])
    qc.barrier()
    #sGateStageGen2
    gate = createSgate(counter+1)
    qc.append(gate,[nSize,nSize-1])
    qc.barrier()
    #saveStageGen2
    saveStage(qc,x,g,c,binaryString[counter])
    qc.barrier()

    counter = counter - 1

#Test phase
"""
binaryString = ['00','11']
startString = ''
for char in binaryString[0]:
  startString = startString + '0'

qc, x, g, c, meas = createCircuit(len(binaryString[0]))

binaryString = binaryString + [startString]
basisEncoding(qc,x,g,c,binaryString)

counter = 0
while(counter < len(binaryString[0])):
  qc.measure(x[counter],meas[counter])
  counter = counter + 1

qc.draw('mpl')

sim = Aer.get_backend('aer_simulator')

qc_t = transpile(qc, basis_gates=['u', 'cx'])

qc_t.draw('mpl')

counts = sim.run(qc_t,shots = 100000).result().get_counts()
plot_histogram(counts)

"""