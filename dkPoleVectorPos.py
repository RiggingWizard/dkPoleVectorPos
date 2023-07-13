import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import sys
from maya.OpenMaya import MVector

nodeName = 'dkPoleVecPos'
nodeId = OpenMaya.MTypeId (0x110fff)

class dkPoleVecPos(OpenMayaMPx.MPxNode):
    
    pointA = OpenMaya.MObject()
    pointB = OpenMaya.MObject()
    pointC = OpenMaya.MObject()
    outPos = OpenMaya.MObject()
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        
    def compute(self, plug, dataBlock):
        if plug == dkPoleVecPos.outPos:
            
            # GRABBING THE VALUES FROM DATA BLOCK #
            
            pointAVal = dataBlock.inputValue(dkPoleVecPos.pointA).asFloat3()
            pointBVal = dataBlock.inputValue(dkPoleVecPos.pointB).asFloat3()
            pointCVal = dataBlock.inputValue(dkPoleVecPos.pointC).asFloat3()
            
            # CREATING VECTORS #
        
            A = MVector(pointAVal[0], pointAVal[1], pointAVal[2])
            B = MVector(pointBVal[0], pointBVal[1], pointBVal[2])
            C = MVector(pointCVal[0], pointCVal[1], pointCVal[2])
            
            # CALCULATION #

            D = (C-A)*0.5
            E = A+D
            F = (B-E)*3      
            G = E+F       
            
            # PROVIDING VALUE TO THE OUTPUT # 

            dataBlock.outputValue(dkPoleVecPos.outPos).set3Float(G.x, G.y, G.z)
            dataBlock.setClean(plug)           
    
def nodeCreator():
    return OpenMayaMPx.asMPxPtr(dkPoleVecPos())

def nodeInitializer():
    mFnAttr = OpenMaya.MFnNumericAttribute()
    
    # CREATING ATTRIBUTES #
    
    dkPoleVecPos.pointA = mFnAttr.create('pointA', 'a', OpenMaya.MFnNumericData.k3Float, 1.0)
    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    mFnAttr.setKeyable(1)
    
    dkPoleVecPos.pointB = mFnAttr.create('pointB', 'b', OpenMaya.MFnNumericData.k3Float, 1.0)
    mFnAttr.setKeyable(1)
    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    
    dkPoleVecPos.pointC = mFnAttr.create('pointC', 'c', OpenMaya.MFnNumericData.k3Float, 1.0)
    mFnAttr.setKeyable(1)
    mFnAttr.setReadable(1)
    mFnAttr.setWritable(1)
    mFnAttr.setStorable(1)
    
    dkPoleVecPos.outPos = mFnAttr.create('outPosition', 'op', OpenMaya.MFnNumericData.k3Float)
    mFnAttr.setReadable(1)
    mFnAttr.setWritable(0)
    mFnAttr.setStorable(0)
    mFnAttr.setKeyable(0)
    
    # ATTACHING ATTRIBUTES #
    
    dkPoleVecPos.addAttribute(dkPoleVecPos.pointA)
    dkPoleVecPos.addAttribute(dkPoleVecPos.pointB)
    dkPoleVecPos.addAttribute(dkPoleVecPos.pointC)
    dkPoleVecPos.addAttribute(dkPoleVecPos.outPos)
    
    # DESIGN CIRCUITRY #
    
    dkPoleVecPos.attributeAffects(dkPoleVecPos.pointA, dkPoleVecPos.outPos)
    dkPoleVecPos.attributeAffects(dkPoleVecPos.pointB, dkPoleVecPos.outPos)
    dkPoleVecPos.attributeAffects(dkPoleVecPos.pointC, dkPoleVecPos.outPos)     

def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(nodeName, nodeId, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write('Failed to register node: %s\n' %nodeName)
        
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(nodeId)
    except:
        sys.stderr.write('Failed to unregister node %s\n' %nodeName)