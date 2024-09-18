from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
import sys
import os
import networkx as nx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import netgraph as nt
import numpy as np
import re
import json
import time
import traceback
import copy
from queue import PriorityQueue, Queue
from TG2A import Problem
from bitsets import bitset
np.seterr(divide='ignore', invalid='ignore')

class CentralWidget(QWidget):

    createNode = pyqtSignal(float, float)
    reableAllActions = pyqtSignal()
    clickPositions = pyqtSignal(float, float)

    def __init__(self):
        super(CentralWidget, self).__init__()
        self.ax = None
        self.x = None
        self.y = None
        # Drag a node
        self.isWaitingClickPosition = False
        # Drag an edge
        self.isWaitingClickTwoNodesPosition = False
        self.initUI()
    
    def initUI(self):
        # Canva
        self._createCentralWidget()
    
    def _createCentralWidget(self):

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.ax = self.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
        self.ax.set_xlim(0.0, 1)
        self.ax.set_ylim(0.0, 1)
        self.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['left'].set_visible(False)

        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
    
    def on_press(self, event):
        self.x = event.x
        self.y = event.y
        if self.isWaitingClickPosition == True:
            self.createNode.emit(event.xdata, event.ydata)
            self.reableAllActions.emit()
            self.isWaitingClickPosition = False

    def on_release(self, event):
        self.clickPositions.emit(self.x, self.y)

class ChronoGraphUI(QMainWindow):
    
    # INIT

    def keyPressEvent(self, event):
        pass
        # print("Key pressed")

    def __init__(self):
        super(ChronoGraphUI, self).__init__()
        self.ax = None
        self._setBaseParameters() 
        self.initUI()

    def _setBaseParameters(self):
        self.ax = None
        self.graph = nx.Graph()
        self.InteractiveGraph  = None
        self.node_color = dict()
        self.edge_color = dict()
        self.edges_labels = dict()
        self.positions = []
        self.actions = []
        self.buttons = []
        self.node_size = 3.0
        self.edge_width = 1.0
        self.scaleX = 1.0
        self.scaleY = 1.0
        self.startX = 0.0
        self.startY = 0.0
        self.clickPositionX = None
        self.clickPositionY = None
        self.editingMode = False
        self.stricte = False
        self.DragAnEdgeNode1 = None
        self.DragAnEdgeNode2 = None
        self.lastDetectedNode = None
        self.lastDetectedEdge = None
        self.deleting = False
        self.typeOfPath = "Foremost"
        self.typeOfWay = "Path"
        self.lifetime = 0
        self.defaultColor = "black"
        self.defaultSize = 12
        self.edge_label_fontdict = {"color" : self.defaultColor, "size" : self.defaultSize}
        
    def initUI(self):
        # Canva
        self._setBaseUIParameters()

        # Actions
        self._createActions()

        # Menubar
        self._createMenuBar()

        # Toolbar
        self._createToolBar()

        # Context Menu
        # self._createContextMenu()

        # Connect Actions
        self._connectActions()

        # Connect signals
        self._connectSignals()

        # Connect shortcuts
        self._setShortcut()
        
    def _setBaseUIParameters(self):
        # Canva size
        self.setFixedSize(800, 800)
        # Title
        self.setWindowTitle('ChronoGraph')
        # Icon
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "icons/appIcons.png")))
        # Position
        self.center()
        # 
        self._createCentralWidget()
        # font
        font = QFont()
        font.setPointSize(10)

    # MENUBAR

    def _createMenuBar(self):
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        # Add Menu

        ## File
        fileMenu = self.menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exportAction)
        fileMenu.addAction(self.clearAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        ## Layout
        LayoutMenu = self.menuBar.addMenu("&Layout")
        NodeMenu = LayoutMenu.addMenu("Nodes")
        NodeMenu.addAction(self.randomNodeLayoutAction)
        NodeMenu.addAction(self.circularNodeLayoutAction)
        NodeMenu.addAction(self.springNodeLayoutAction)
        NodeMenu.addAction(self.dotNodeLayoutAction)
        NodeMenu.addAction(self.radialNodeLayoutAction)

        ## Color
        ColorMenu = self.menuBar.addMenu("&Color")
        NodeColorMenu = ColorMenu.addMenu("Nodes")
        NodeColorMenu.addAction(self.ResetNodeColorAction)
        NodeColorMenu.addAction(self.changeColorNodesAction)
        EdgeColorMenu = ColorMenu.addMenu("Edges")
        EdgeColorMenu.addAction(self.ResetEdgeColorAction)
        EdgeColorMenu.addAction(self.changeColorEdgesAction)
        LabelColorMenu = ColorMenu.addMenu("Labels")
        LabelColorMenu.addAction(self.ResetLabelColorAction)
        LabelColorMenu.addAction(self.changeColorLabelsAction)
        ColorMenu.addAction(self.ResetColorAction)


        ## Size
        SizeMenu = self.menuBar.addMenu("&Size")
        NodeSizeMenu = SizeMenu.addMenu("Nodes")
        NodeSizeMenu.addAction(self.UpNodeSizeAction)
        NodeSizeMenu.addAction(self.DownNodeSizeAction)
        EdgeSizeMenu = SizeMenu.addMenu("Edges")
        EdgeSizeMenu.addAction(self.UpEdgeSizeAction)
        EdgeSizeMenu.addAction(self.DownEdgeSizeAction)
        LabelSizeMenu = SizeMenu.addMenu("Labels")
        LabelSizeMenu.addAction(self.UpLabelSizeAction)
        LabelSizeMenu.addAction(self.DownLabelSizeAction)
        SizeMenu.addAction(self.ResetSize)

        ## Spanner
        SpannerMenu = self.menuBar.addMenu("Spanner")
        SpannerMenu.addAction(self.SpannerAction)
        SpannerMenu.addAction(self.SpannerBitsetsAction)

        ## Dismountability
        DismountabilityMenu = self.menuBar.addMenu("Dismountability")
        # DismountabilityMenu.addAction(self.delegationAction)
        DismountabilityMenu.addAction(self.vertexDismountabilityAction)
        DismountabilityMenu.addAction(self.spannerDismountabilityAction)

    # TOOLBAR

    def _createToolBar(self):
        # Add toolbar
        ToolBar = self.addToolBar("File")
        ToolBar.setMovable(False)
        # Examples
        ToolBar.addAction(self.exampleAction)
        ToolBar.addSeparator()
        # Drag&Drop
        ToolBar.addAction(self.dragNodeAction)
        ToolBar.addAction(self.createEdgeAction)
        ToolBar.addAction(self.deleteNodeEdgeAction)
        ToolBar.addSeparator()
        # Zoom
        ToolBar.addAction(self.zoomInAction)
        ToolBar.addAction(self.zoomOutAction)
        ToolBar.addAction(self.zoomResetAction)
        ToolBar.addSeparator()
        # Moving or editing mode
        ToolBar.addAction(self.editingModeAction)
        ToolBar.addSeparator()
        # Temporal features
        ToolBar.addAction(self.RestlessAction)
        ToolBar.addAction(self.completeTemporalConnectedAction)
        ToolBar.addAction(self.biPathAction)
        # Mooving features
        ToolBar.addSeparator()
        ToolBar.addAction(self.mooveLeftAction)
        ToolBar.addAction(self.mooveRightAction)
        ToolBar.addAction(self.mooveUpAction)
        ToolBar.addAction(self.mooveDownAction)

    # ACTIONS

    def _createActions(self):
        # Add actions
        ## File Menu
        self.openAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/open.svg")),"&Open", self)
        self.newAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/new.svg")),"&New", self)
        self.saveAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/save.svg")),"&Save", self)
        self.exportAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/export.svg")),"&Export", self)
        self.clearAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/trash.svg")),"&Clear", self)
        self.exitAction = QAction("&Exit", self)
        ## Help Menu
        self.manualAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/manual.svg")),"&Manual", self)
        self.aboutAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/info.svg")),"&About", self)
        # Example
        self.exampleAction = QAction("&Example", self)
        # graph operations
        self.addNodeAction = QAction("&Add node", self)
        self.removeNodeAction = QAction("&Remove node", self)
        self.addEdgeAction = QAction("&Add Edge", self)
        self.removeEdgeAction = QAction("&Remove Edge", self)
        # Layout
        self.randomNodeLayoutAction = QAction("&Random Layout", self)
        self.circularNodeLayoutAction = QAction("&Circular Layout", self)
        self.springNodeLayoutAction = QAction("&Spring Layout", self)
        self.dotNodeLayoutAction = QAction("&Dot Layout", self)
        self.radialNodeLayoutAction = QAction("&Radial Layout", self)
        # Color
        self.ResetNodeColorAction = QAction("Reset", self)
        self.ResetEdgeColorAction = QAction("Reset", self)
        self.ResetLabelColorAction = QAction("Reset", self)
        self.ResetColorAction = QAction("Reset all", self)
        self.changeColorEdgesAction = QAction("&Personalize", self)
        self.changeColorNodesAction = QAction("&Personalize", self)
        self.changeColorLabelsAction = QAction("&Personalize", self)
        # Debug
        self.debugAction = QAction("&Debug", self)
        # Drag&Drop
        self.dragNodeAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/circle.svg")),"&Drag Node", self)
        self.createEdgeAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/edges.svg")),"&Drag Edge", self)
        self.icon_deleting = QIcon()
        self.pix_deleting = QPixmap(os.path.join(os.path.dirname(__file__), "icons/minus.svg"))
        self.icon_deleting.addPixmap(self.pix_deleting)
        self.deleteNodeEdgeAction = QAction(self.icon_deleting,"&Delete Edge or Node", self)
        # Zoom
        self.zoomInAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/zoomIn.svg")),"&Zoom In", self)
        self.zoomOutAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/zoomOut.svg")),"&Zoom Out", self)
        self.zoomResetAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/zoomReset.svg")),"&Zoom Out", self)
        # Moove the caneva
        self.mooveLeftAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/arrowLeft.svg")),"&Moove Left", self)
        self.mooveRightAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/arrowRight.svg")),"&Moove Right", self)
        self.mooveUpAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/arrowUp.svg")),"&Moove Up", self)
        self.mooveDownAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/arrowDown.svg")),"&Moove Down", self)
        # Moving mode
        self.icon_editing = QIcon()
        self.pix_editing = QPixmap(os.path.join(os.path.dirname(__file__), "icons/hand.svg"))
        self.icon_editing.addPixmap(self.pix_editing)
        self.editingModeAction = QAction(self.icon_editing,"&Editing Mode", self)
        # Size
        self.UpNodeSizeAction = QAction("Up", self)
        self.DownNodeSizeAction = QAction("Down", self)
        self.UpEdgeSizeAction = QAction("Up", self)
        self.DownEdgeSizeAction = QAction("Down", self)
        self.UpLabelSizeAction = QAction("Up", self)
        self.DownLabelSizeAction = QAction("Down", self)
        self.ResetSize = QAction("Reset", self)
        # Temporals features
        self.RestlessAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/delta.svg")),"&Restless", self)
        self.completeTemporalConnectedAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/paths.svg")),"&Temporaly connected", self)
        self.biPathAction = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icons/biPaths.svg")),"&Bi path", self)
        # Spanner
        self.SpannerAction = QAction("&Minimal Spanner", self)
        self.SpannerBitsetsAction = QAction("&Minimal Spanner (bitsets)", self)
        # Dismountability
        self.delegationAction = QAction("&Delegation", self)
        self.vertexDismountabilityAction = QAction("&Vertex dismountability", self)
        self.spannerDismountabilityAction = QAction("&Spanner dismountability", self)

        # list of all actions
        self.actions.append(self.openAction)
        self.actions.append(self.newAction)
        self.actions.append(self.saveAction)
        self.actions.append(self.exportAction)
        self.actions.append(self.clearAction)
        self.actions.append(self.exitAction)
        self.actions.append(self.manualAction)
        self.actions.append(self.aboutAction)
        self.actions.append(self.exampleAction)
        self.actions.append(self.addNodeAction)
        self.actions.append(self.removeNodeAction)
        self.actions.append(self.addEdgeAction)
        self.actions.append(self.removeEdgeAction)
        self.actions.append(self.randomNodeLayoutAction)
        self.actions.append(self.circularNodeLayoutAction)
        self.actions.append(self.springNodeLayoutAction)
        self.actions.append(self.dotNodeLayoutAction)
        self.actions.append(self.radialNodeLayoutAction)
        self.actions.append(self.ResetNodeColorAction)
        self.actions.append(self.ResetEdgeColorAction)
        self.actions.append(self.ResetLabelColorAction)
        self.actions.append(self.ResetColorAction)
        self.actions.append(self.changeColorNodesAction)
        self.actions.append(self.changeColorEdgesAction)
        self.actions.append(self.changeColorLabelsAction)
        self.actions.append(self.debugAction)
        self.actions.append(self.dragNodeAction)
        self.actions.append(self.createEdgeAction)
        self.actions.append(self.deleteNodeEdgeAction)
        self.actions.append(self.zoomInAction)
        self.actions.append(self.zoomOutAction)
        self.actions.append(self.zoomResetAction)
        self.actions.append(self.mooveLeftAction)
        self.actions.append(self.mooveRightAction)
        self.actions.append(self.mooveDownAction)
        self.actions.append(self.mooveUpAction)
        self.actions.append(self.editingModeAction)
        self.actions.append(self.UpNodeSizeAction)
        self.actions.append(self.DownNodeSizeAction)
        self.actions.append(self.UpEdgeSizeAction)
        self.actions.append(self.DownEdgeSizeAction)
        self.actions.append(self.UpLabelSizeAction)
        self.actions.append(self.DownLabelSizeAction)
        self.actions.append(self.completeTemporalConnectedAction)
        self.actions.append(self.RestlessAction)
        self.actions.append(self.biPathAction)
        self.actions.append(self.SpannerAction)
        self.actions.append(self.SpannerBitsetsAction)
        self.actions.append(self.delegationAction)
        self.actions.append(self.vertexDismountabilityAction)
        self.actions.append(self.spannerDismountabilityAction)

    def _connectActions(self):
        # Connect File actions
        ## File Menu
        self.newAction.triggered.connect(self.new)
        self.saveAction.triggered.connect(self.saveJson)
        self.exportAction.triggered.connect(self.export)
        self.openAction.triggered.connect(self.open)
        self.clearAction.triggered.connect(self.clearGraph)
        ## Exit
        self.exitAction.triggered.connect(self.close)
        # Example
        self.exampleAction.triggered.connect(lambda: self.example(['A', 'B', 'C', 'D', 'E', 'F', 'G'], np.array([['A', 'B'], ['A', 'C'], ['B', 'D'], ['B', 'E'], ['C', 'F'], ['C', 'G']]), edges_labels=[[["A", "B"], "1"], [["A", "C"], "2"], [["B", "D"], "3"], [["B", "E"], "4"], [["C", "F"], "5"], [["C", "G"], "6"]]))
        # graph operations
        self.addNodeAction.triggered.connect(lambda: self.add_node(x=None, y=None))
        self.removeNodeAction.triggered.connect(lambda: self.remove_node(None))
        self.addEdgeAction.triggered.connect(lambda: self.add_edge(None, None))
        self.removeEdgeAction.triggered.connect(lambda: self.remove_edge(None))
        # Layout
        self.randomNodeLayoutAction.triggered.connect(lambda: self.nodeLayout('random'))
        self.circularNodeLayoutAction.triggered.connect(lambda: self.nodeLayout('circular'))
        self.springNodeLayoutAction.triggered.connect(lambda: self.nodeLayout('spring'))
        self.dotNodeLayoutAction.triggered.connect(lambda: self.nodeLayout('dot'))
        self.radialNodeLayoutAction.triggered.connect(lambda: self.nodeLayout('radial'))
        # Color
        self.ResetNodeColorAction.triggered.connect(lambda : self.changeColor("reset_color_nodes", perso=None))
        self.ResetEdgeColorAction.triggered.connect(lambda : self.changeColor("reset_color_edges", perso=None))
        self.ResetLabelColorAction.triggered.connect(lambda : self.changeColor("reset_color_labels", perso=None))
        self.ResetColorAction.triggered.connect(lambda : self.changeColor("reset_colors", perso=None))
        self.changeColorNodesAction.triggered.connect(lambda : self.changeColor("change_color_nodes", perso=None))
        self.changeColorEdgesAction.triggered.connect(lambda : self.changeColor("change_color_edges", perso=None))
        self.changeColorLabelsAction.triggered.connect(lambda : self.changeColor("change_color_labels", perso=None))
        # debug
        self.debugAction.triggered.connect(self.debug)
        # Drag&Drop
        self.dragNodeAction.triggered.connect(self.dragANode)
        self.createEdgeAction.triggered.connect(self.dragAnEdge)
        self.deleteNodeEdgeAction.triggered.connect(self.deletingMode)
        # Zoom
        self.zoomInAction.triggered.connect(lambda : self.zoom(scale=0.05, key=None))
        self.zoomOutAction.triggered.connect(lambda : self.zoom(scale=-0.05, key=None))
        self.zoomResetAction.triggered.connect(lambda : self.zoom(scale=None, key="reset"))
        # Moving mode
        self.editingModeAction.triggered.connect(self.selectEditingMode)
        self.mooveLeftAction.triggered.connect(lambda : self.zoom(scale=1.0,key="mooveLeft"))
        self.mooveRightAction.triggered.connect(lambda : self.zoom(scale=1.0,key="mooveRight"))
        self.mooveUpAction.triggered.connect(lambda : self.zoom(scale=1.0,key="mooveUp"))
        self.mooveDownAction.triggered.connect(lambda : self.zoom(scale=1.0,key="mooveDown"))
        # Size 
        self.UpNodeSizeAction.triggered.connect(lambda : self.changeSize(1.10, 1, 0))
        self.DownNodeSizeAction.triggered.connect(lambda : self.changeSize(0.90, 1, 0))
        self.UpEdgeSizeAction.triggered.connect(lambda : self.changeSize(1, 1.10, 0))
        self.DownEdgeSizeAction.triggered.connect(lambda : self.changeSize(1, 0.90, 0))
        self.UpLabelSizeAction.triggered.connect(lambda : self.changeSize(1, 1, 2))
        self.DownLabelSizeAction.triggered.connect(lambda : self.changeSize(1, 1, -2))
        self.ResetSize.triggered.connect(lambda : self.changeSize(None, None, None))
        # Temporals features
        self.RestlessAction.triggered.connect(self.computes_optimal_walks)
        self.completeTemporalConnectedAction.triggered.connect(lambda : self.isTemporalyConnected(one_edge=None, target=None, changeColor=True, method=None))
        self.biPathAction.triggered.connect(lambda : self.bipath(key=None, target=None))
        # Spanner
        self.SpannerAction.triggered.connect(lambda : self.minimalSpanner(bitsets=False))
        self.SpannerBitsetsAction.triggered.connect(lambda : self.minimalSpanner(bitsets=True))
        # Dismountability
        self.delegationAction.triggered.connect(lambda : self.delegation(node_v=None, verbose=True))
        self.vertexDismountabilityAction.triggered.connect(lambda : self.vertex_dismountability(node_v=None, verbose=True))
        self.spannerDismountabilityAction.triggered.connect(self.spanner_dismountability)

    # SIGNALS

    def _connectSignals(self):
        # Create a node
        self.centralWidget.createNode.connect(self.add_node)
        #  Reable all actions
        self.centralWidget.reableAllActions.connect(self.reableAllActions)
        # Get click positions
        self.centralWidget.clickPositions.connect(self.detect)

    # CENTRAL WIDGET - CANVA

    def _createCentralWidget(self): 
        self.centralWidget = CentralWidget()

        self.centralWidget.grid = QGridLayout()
        self.centralWidget.setFocusPolicy(Qt.StrongFocus)
        self.centralWidget.setLayout(self.centralWidget.grid)

        buttonAddNode = QPushButton("Add Node")
        buttonAddNode.setObjectName("Add Node")
        self.buttons.append(buttonAddNode)
        buttonAddNode.clicked.connect(lambda: self.add_node(x=0.5, y=0.5))

        buttonRemoveNode = QPushButton("Remove Node")
        buttonRemoveNode.setObjectName("Remove Node")
        self.buttons.append(buttonRemoveNode)
        buttonRemoveNode.clicked.connect(lambda: self.remove_node(None))

        buttonAddEdge = QPushButton("Add Edge")
        buttonAddEdge.setObjectName("Add Edge")
        self.buttons.append(buttonAddEdge)
        buttonAddEdge.clicked.connect(lambda: self.add_edge(None, None))

        buttonRemoveEdge = QPushButton("Remove Edge")
        buttonRemoveEdge.setObjectName("Remove Edge")
        self.buttons.append(buttonRemoveEdge)
        buttonRemoveEdge.clicked.connect(lambda: self.remove_edge(None))

        # création du champ de texte
        self.champ = QLineEdit("")
        self.champ.setFixedWidth(75)
        self.champ.show()

        ## DEBUG

        buttonDebug = QPushButton("Debug")
        buttonDebug.setObjectName("Debug")
        self.buttons.append(buttonDebug)
        buttonDebug.clicked.connect(self.debug)

        case = QCheckBox("Strict")
        case.stateChanged.connect(self.setStricte)
        case.show()

        combobox1 = QComboBox()
        combobox1.addItem('Foremost')
        combobox1.addItem('Shortest')
        combobox1.addItem('Fastest')
        combobox1.currentTextChanged.connect(self.setForemostShortestFastest)

        ## HORIZONTAL

        self.centralWidget.grid.addWidget(self.centralWidget.canvas, 1, 1, 9, 9)
        self.centralWidget.grid.addWidget(self.champ, 0, 0)
        self.centralWidget.grid.addWidget(buttonAddNode, 1, 0)
        self.centralWidget.grid.addWidget(buttonRemoveNode, 2, 0)
        self.centralWidget.grid.addWidget(buttonAddEdge, 3, 0)
        self.centralWidget.grid.addWidget(buttonRemoveEdge, 4, 0)

        self.centralWidget.grid.addWidget(case, 7, 0)
        self.centralWidget.grid.addWidget(combobox1, 8, 0)
        self.centralWidget.grid.addWidget(buttonDebug, 9, 0)
        
        self.centralWidget.show()

        self.setCentralWidget(self.centralWidget)

    # SHORTCUT

    def _setShortcut(self):
        # https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtgui/qkeysequence.html#enums
        self.newAction.setShortcut(QKeySequence.New)
        self.openAction.setShortcut(QKeySequence.Open)
        self.saveAction.setShortcut(QKeySequence.Save)
        self.exportAction.setShortcut(QKeySequence('Ctrl+E'))
        self.clearAction.setShortcut(QKeySequence.Delete)
        self.zoomInAction.setShortcut(QKeySequence.ZoomIn)
        self.zoomOutAction.setShortcut(QKeySequence.ZoomOut)
        self.dragNodeAction.setShortcut(QKeySequence("Ctrl+&"))
        self.createEdgeAction.setShortcut(QKeySequence("Ctrl+é"))
        self.deleteNodeEdgeAction.setShortcut(QKeySequence("Del"))
        self.mooveLeftAction.setShortcut(QKeySequence("Left"))
        self.mooveRightAction.setShortcut(QKeySequence("Right"))
        self.mooveUpAction.setShortcut(QKeySequence("Up"))
        self.mooveDownAction.setShortcut(QKeySequence("Down"))


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    ## Actions functions
    
    def example(self, nodes, edges, edges_labels):
        print("Create an example.")
        self.clearGraph()

        if nodes == [] and edges == []:
            print("Empty graph")
            return -1

        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)

        # Re-open, reset lifetime
        self.lifetime = 0

        for element in edges_labels:
            self.edges_labels[(element[0][0], element[0][1])] = element[1]
            if ',' in element[1]:
                labels_splited = element[1].split(',')
                for lab in labels_splited:
                    if int(lab) > self.lifetime:
                        self.lifetime = int(lab)
            else:
                if int(element[1]) > self.lifetime:
                    self.lifetime = int(element[1])

        self.edges_labels = dict(self.edges_labels)

        if self.node_color == dict():
            for node in self.graph.nodes:
                self.node_color[node] = "w"

        if self.edge_color == dict():
            for edge in self.graph.edges:
                self.edge_color[edge] = '#2c404c'
                self.edge_color[edge[::-1]] = '#2c404c'

        self.ax = self.centralWidget.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
        self.centralWidget.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)

        self.ax.set_xlim(self.startX, self.scaleX)
        self.ax.set_ylim(self.startY, self.scaleY)
        
        if self.positions == []:
            self.positions = "spring"
        self.InteractiveGraph  = nt.InteractiveGraph(self.graph, ax=self.ax, node_layout=self.positions, node_labels=True, node_color=self.node_color, edge_color=self.edge_color, edge_labels=self.edges_labels, node_size=self.node_size, edge_width=self.edge_width,edge_label_fontdict=self.edge_label_fontdict)

        self.positions = self.InteractiveGraph.node_positions

    def new(self):
        if self.InteractiveGraph  != None:
            alert = self.saveMsgBox()
        else:
            self.clearGraph()

    def export(self):
        if self.InteractiveGraph  != None:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Exporter le fichier", "", "PNG files (*.png)", options=options)
            if file_path:
                plt.savefig(file_path,format='png')
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("No graph to export.")
            msgBox.setWindowTitle("Alert")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            _ = msgBox.exec()

    def clearGraph(self):
        if self.InteractiveGraph  != None:
            self.centralWidget.figure.clf()
            ## Clear the canvas
            self.ax.clear()
            self.centralWidget.canvas.draw_idle()
            ## Clear the variables
            self.graph = nx.Graph()
            self.InteractiveGraph  = None
            self.node_color = dict()
            self.edge_color = dict()
            self.edges_labels = dict()
            self.positions = []

            self.ax = self.centralWidget.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
            self.centralWidget.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
            self.ax.set_xlim(self.startX, self.scaleX)
            self.ax.set_ylim(self.startY, self.scaleY)

            self.ax.spines['top'].set_visible(False)
            self.ax.spines['left'].set_visible(False)

        else:
            print("Nothing to clear.")

    def open(self):
        if self.InteractiveGraph  != None:
            alert = self.saveMsgBox()
            if alert == False:
                return
            self.clearGraph()
        self.openJson()

    def askUser(self):
        """
        Pop-up window with QLineEdit.
        """
        dialog = QDialog()
        dialog.setWindowTitle('Popup')
        dialog.layout = QVBoxLayout()
        dialog.setLayout(dialog.layout)

        dialog.label = QLabel('Entrez du texte:')
        dialog.text_edit = QLineEdit()
        dialog.submit_button = QPushButton('Valider')
        dialog.submit_button.clicked.connect(dialog.accept)

        dialog.layout.addWidget(dialog.label)
        dialog.layout.addWidget(dialog.text_edit)
        dialog.layout.addWidget(dialog.submit_button)

        if dialog.exec_():
            text = dialog.text_edit.text()
            print('Texte entré:', text)
            return text
        else:
            return -1

    ## Save

    def saveMsgBox(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Do you want to save?")
        msgBox.setWindowTitle("Alert")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes:
            self.saveJson()
            self.clearGraph()
            return True
        elif returnValue == QMessageBox.No:
            self.clearGraph()
        elif returnValue == QMessageBox.Cancel:
            print('Cancel clicked')
            return False

    def saveJson(self):
        """
        Affiche une boîte de dialogue pour enregistrer une variable dans un fichier.

        Args:
            parent (QWidget): Le widget parent de la boîte de dialogue.
            variable: La variable à sauvegarder.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier", "", "JSON files (*.json)", options=options)
        if file_path:
            jsonFile = self.graphToJson()
            with open(file_path, 'w') as f:
                f.write(jsonFile)
        else:
            return -1

    def graphToJson(self):

        print('self.positions = ', self.positions)

        if self.positions != []:
            for key,value in self.positions.items():
                self.positions[key] = [value[0], value[1]]
            new_positions = self.positions.items()
        else:
            new_positions = []

        graph = { 
            "nodes": list(self.graph.nodes), 
            "edges": list(self.graph.edges),
            "nodes_colors": dict(self.node_color.items()),
            "edges_colors": list(self.edge_color.items()),
            "edges_labels": list(self.edges_labels.items()),
            "layout": dict(new_positions),
            "node_size": self.node_size,
            "edge_width": self.edge_width,
            "startX": self.startX,
            "startY": self.startY,
            "scaleX": self.scaleX,
            "scaleY": self.scaleY,
            "text_perso": self.edge_label_fontdict
            }
        return json.dumps(graph) 

    def openJson(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Ouvrir le fichier", "", "JSON files (*.json)")
        if file_path:
            with open(file_path, "r") as f:
                data = json.load(f)
                self.positions = data["layout"]
                self.node_color = data["nodes_colors"]
                self.edge_color = dict()
                if "startX" in data.keys():
                    self.startX = data["startX"]
                if "startY" in data.keys():
                    self.startY = data["startY"]
                if "scaleX" in data.keys():
                    self.scaleX = data["scaleX"]
                if "scaleY" in data.keys():
                    self.scaleY = data["scaleY"]
                for element in data["edges_colors"]:
                    self.edge_color[(element[0][0], element[0][1])] = element[1]
                self.node_size = data["node_size"]
                self.edge_width = data["edge_width"]
                if "text_perso" in data.keys():
                    self.edge_label_fontdict = data['text_perso']
                else:
                    self.edge_label_fontdict = {"color" : self.defaultColor, "size" : self.defaultSize}
                self.example(data['nodes'], data["edges"],data["edges_labels"])

    ## Informations functions

    def debug(self):
        print(" ----------------------------------------------- ")
        if self.graph != None:
            print("#nodes = ", len(self.graph.nodes))
            print("Nodes : ", self.graph.nodes)
            print("#edges = ", len(self.graph.edges))
            print("Edges : ", self.graph.edges)
        if self.InteractiveGraph  != None:
            print("Positions : ")
            for node in self.InteractiveGraph.node_positions:
                print(f"{node} : ({self.InteractiveGraph.node_positions[node][0]},{self.InteractiveGraph.node_positions[node][1]}) : {self.node_color[node]}")
        for edge,label in self.edges_labels.items():
            print(f"{edge} : {label} : {self.edge_color[edge]}")
        if self.editingMode == True:
            print("Mode = Editing")
        else:
            print("Mode = Moving")
        if self.stricte == True:
            print("Stricte")
        else:
            print("Non stricte")
        print(f"Last detected node : {self.lastDetectedNode}")
        print(f"Last detected edge : {self.lastDetectedEdge}")

        if self.ax != None:
            print("x lim : ", self.ax.get_xlim())
            print("y lim : ", self.ax.get_ylim())
            
        print('type of paths = ', self.typeOfPath)
    
    # Convertions function 

    def labelsToList(self, labels):
        if type(labels) == int:
            return [labels]
        if type(labels) == str:
            new_labels = labels.split(",")
            return [int(a) for a in new_labels]

    ## Graph operations
        
    def add_node(self, x, y): 

        name_node = self.champ.text()

        if x == None and y == None:
            pass

        if self.InteractiveGraph  != None:
            self.positions = self.InteractiveGraph.node_positions
        else:
            self.positions = dict()

        if name_node == "":
            print("Please choose a valid name.")
            return -1

        for node in self.graph.nodes:
            if self.node_color[node] == "tab:green":
                self.node_color[node] = "w"

        if name_node not in self.graph.nodes:
            self.graph.add_node(name_node)
            self.node_color[name_node] = "tab:green"
        else:
            print("Already existing node.Please choose another name.")
            return -1
        
        self.centralWidget.figure.clf()

        self.positions[name_node] = (x,y)

        self.ax = self.centralWidget.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
        self.centralWidget.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax.set_xlim(self.startX, self.scaleX)
        self.ax.set_ylim(self.startY, self.scaleY)

        self.InteractiveGraph  = nt.InteractiveGraph (self.graph, ax=self.ax, node_labels=True,node_layout=self.positions,node_color=self.node_color, edge_color=self.edge_color, edge_labels=self.edges_labels, node_size=self.node_size, edge_width=self.edge_width, edge_label_fontdict=self.edge_label_fontdict)

    def remove_node(self, node):

        if node == None:
            name_node = self.champ.text()
        else:
            name_node = node
        
        print("node = ", node)

        if self.InteractiveGraph  != None:
            self.positions = self.InteractiveGraph.node_positions
        else:
            self.positions = dict()

        if name_node == "":
            print("Please choose a valid name.")
            return -1

        if name_node not in self.graph.nodes:
            print("Please choose an existing node.")
            return -1
        else:
            # Remove node
            self.graph.remove_node(name_node)
            # Remove position of this node
            _ = self.positions.pop(name_node)
            _ = self.node_color.pop(name_node)
            # Reset all the color of existing edge
            new_edges_labels = dict()
            for edge in self.graph.edges:
                if edge in self.edges_labels:
                    new_edges_labels[edge] = self.edges_labels[edge]
            self.edges_labels = new_edges_labels
        
        self.centralWidget.figure.clf()

        self.ax = self.centralWidget.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
        self.centralWidget.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax.set_xlim(self.startX, self.scaleX)
        self.ax.set_ylim(self.startY, self.scaleY)

        if self.graph.nodes != {}:
            self.InteractiveGraph  = nt.InteractiveGraph (self.graph, ax=self.ax, node_labels=True,node_layout=self.positions,node_color=self.node_color, edge_color=self.edge_color, edge_labels=self.edges_labels, node_size=self.node_size, edge_width=self.edge_width, edge_label_fontdict=self.edge_label_fontdict)
        else:
            self.clearGraph()
        
    def add_edge(self, node_from, node_to):

        # check format
        if node_from == None and node_to == None:
            name_node = self.champ.text()
        else:
            name_node = f'{node_from}->{node_to}'

        if not (re.match(r".*->.*", name_node) or re.match(r".*->.* : .*", name_node)):
            print("*->* or *->* : * required.")
            return -1
        
        if re.match(r".*->.*", name_node):
            node_from, node_to = name_node.split("->")
            label_node_to = ""

        if re.match(r".*->.* : .*", name_node):
            node_from, node_to = name_node.split("->")
            node_to, label_node_to = node_to.split(" : ")
            if ',' in label_node_to:
                labels_splited = label_node_to.split(",")
                for element in labels_splited:
                    if int(element) > self.lifetime:
                        self.lifetime = int(element)
            else:
                if int(label_node_to) > self.lifetime:
                    self.lifetime = int(element)


        # Check if both nodes exists
        if node_from not in self.graph.nodes or node_to not in self.graph.nodes:
            print("At least one nodes not exists.")
            return -1
        if (node_from, node_to) in self.graph.edges:
            print("Edge already exists.")
            return -1

        self.centralWidget.figure.clf()

        self.graph.add_edge(node_from, node_to)

        for edge in self.graph.edges:
            if edge[0] == node_from and edge[1] == node_to:
                self.edges_labels[(node_from, node_to)] = label_node_to
            if edge[0] == node_to and edge[1] == node_from:
                self.edges_labels[(edge[0], edge[1])] = label_node_to   

        if self.InteractiveGraph  != None:
            self.positions = self.InteractiveGraph.node_positions
        else:
            self.positions = dict()
        
        # Reset the color of the edges:
        for edge in self.graph.edges:
            if edge in self.edge_color.keys():
                if self.edge_color[edge] == 'tab:green':
                    self.edge_color[edge] = '#2c404c'
            if edge[::-1] in self.edge_color.keys():
                if self.edge_color[edge[::-1]] == 'tab:green':
                    self.edge_color[edge[::-1]] = '#2c404c'


        self.edge_color[(node_from, node_to)] = "tab:green"
        self.edge_color[(node_to, node_from)] = "tab:green"

        self.ax = self.centralWidget.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
        self.centralWidget.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax.set_xlim(self.startX, self.scaleX)
        self.ax.set_ylim(self.startY, self.scaleY)

        self.InteractiveGraph  = nt.InteractiveGraph (self.graph, ax=self.ax, node_labels=True,node_layout=self.positions,node_color=self.node_color, edge_color=self.edge_color, edge_labels=self.edges_labels, node_size=self.node_size, edge_width=self.edge_width, edge_label_fontdict=self.edge_label_fontdict)

    def remove_edge(self, edge):

        # check format
        if edge == None:
            name_node = self.champ.text()
        else:
            name_node = edge
        if not (re.match(r".*->.*", name_node) or re.match(r".*->.* : .*", name_node)):
            print("*->* or *->* : * required.")
            return -1
        
        if re.match(r".*->.*", name_node):
            node_from, node_to = name_node.split("->")

        if re.match(r".*->.* : .*", name_node):
            node_from, node_to = name_node.split("->")
            node_to, label_node_to = node_to.split(" : ")

        # Check if both nodes exists
        if node_from not in self.graph.nodes or node_to not in self.graph.nodes:
            print("At least one nodes not exists.")
            return -1
        if (node_from, node_to) not in self.graph.edges:
            print("Edge not already exists.")
            return -1
        
        self.centralWidget.figure.clf()

        if self.InteractiveGraph  != None:
            self.positions = self.InteractiveGraph.node_positions
        else:
            self.positions = dict()

        # edges labels
        if (node_from, node_to) in self.edges_labels:
            del self.edges_labels[(node_from, node_to)]
        if (node_to, node_from) in self.edges_labels:
            del self.edges_labels[(node_to, node_from)]

        self.graph.remove_edge(node_from, node_to)
        print("------------------------------")
        traceback.print_stack()
        print("------------------------------")
        if (node_from, node_to) in self.edge_color.keys():
            _ = self.edge_color.pop((node_from, node_to))
        elif (node_to, node_from) in self.edge_color.keys():
            _ = self.edge_color.pop((node_to, node_from))

        self.ax = self.centralWidget.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
        self.centralWidget.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax.set_xlim(self.startX, self.scaleX)
        self.ax.set_ylim(self.startY, self.scaleY)

        self.InteractiveGraph  = nt.InteractiveGraph (self.graph, ax=self.ax, node_labels=True,node_layout=self.positions,node_color=self.node_color, edge_color=self.edge_color, edge_labels=self.edges_labels, node_size=self.node_size, edge_width=self.edge_width, edge_label_fontdict=self.edge_label_fontdict)

    ## Graph layout
        
    def nodeLayout(self, layout):
        '''
        Redraw the graph, change something (color,size...)
        '''
        if self.InteractiveGraph  == None:
            print("A graph is needed to layout.")
            return -1
        
        self.centralWidget.figure.clf()
        self.ax = self.centralWidget.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
        self.centralWidget.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax.set_xlim(self.startX, self.scaleX)
        self.ax.set_ylim(self.startY, self.scaleY)

        self.InteractiveGraph  = nt.InteractiveGraph (self.graph, ax=self.ax, node_labels=True,node_layout=layout,node_color=self.node_color, edge_color=self.edge_color, edge_labels=self.edges_labels, node_size=self.node_size, edge_width=self.edge_width, edge_label_fontdict=self.edge_label_fontdict)
        self.positions = self.InteractiveGraph.node_positions

    ## Graph Color
    
    def changeColor(self, action, perso):

        if self.InteractiveGraph  == None:
            print("A graph is needed to change the colors.")
            return -1

        if action == "reset_color_nodes":
            for element in self.node_color:
                self.node_color[element] = "w"
        
        if action == "reset_color_edges":
            for element in self.edge_color:
                self.edge_color[element] = '#2c404c'
        
        if action == "reset_color_labels":
            self.edge_label_fontdict= {"color" : self.defaultColor, "size" : self.defaultSize}

        if action == 'change_color_edges':
            # Pop-up : ask user
            dialog = QDialog()
            dialog.setWindowTitle('Alert')
            dialog.layout = QVBoxLayout()
            dialog.setLayout(dialog.layout)

            dialog.label = QLabel('Please choose edges:')
            dialog.text_edit = QLineEdit()
            dialog.submit_button = QPushButton('Valider')
            dialog.submit_button.clicked.connect(dialog.accept)

            dialog.label2 = QLabel("Format : <edge> : <color> \n<edge> is an existing edge or 'all'\n<color> is an existing color")
            dialog.label3 = QLabel("Possible colors formats : RGBA")

            dialog.layout.addWidget(dialog.label)
            dialog.layout.addWidget(dialog.text_edit)
            dialog.layout.addWidget(dialog.submit_button)
            dialog.layout.addWidget(dialog.label2)
            dialog.layout.addWidget(dialog.label3)

            if dialog.exec_():
                text = dialog.text_edit.text()
            # Cancel case
            else:
                print("Cancel")
                return -1
            
            if re.match(r".*->.* : .*", text):
                edges, color = text.split(" : ")
                edges = edges.split("->")
                edges = [[edges[0], edges[1]]]

            elif re.match(r"all : .*", text):
                _, color = text.split(" : ")
                edges = self.graph.edges
            else:
                print("Bad format.")
                return -1
            
            for edge in edges:
                for element in self.edge_color:
                    if element ==  (edge[0], edge[1]) or element == (edge[1], edge[0]):
                        self.edge_color[element] = color
        
        if action == 'change_color_nodes':
            # Pop-up : ask user
            dialog = QDialog()
            dialog.setWindowTitle('Alert')
            dialog.layout = QVBoxLayout()
            dialog.setLayout(dialog.layout)

            dialog.label = QLabel('Please choose one node:')
            dialog.text_edit = QLineEdit()
            dialog.submit_button = QPushButton('Valider')
            dialog.submit_button.clicked.connect(dialog.accept)

            dialog.label2 = QLabel("Format : <node> : <color> \n<node> is an existing node or 'all'\n<color> is an existing color")
            dialog.label3 = QLabel("Possible colors formats : RGBA")

            dialog.layout.addWidget(dialog.label)
            dialog.layout.addWidget(dialog.text_edit)
            dialog.layout.addWidget(dialog.submit_button)
            dialog.layout.addWidget(dialog.label2)
            dialog.layout.addWidget(dialog.label3)

            if dialog.exec_():
                text = dialog.text_edit.text()
            # Cancel case
            else:
                print("Cancel")
                return -1
            
            if re.match(r".* : .*", text):
                nodes, color = text.split(" : ")
                if nodes == 'all':
                    for node in self.graph.nodes:
                        self.node_color[node] = color
                if nodes in self.graph.nodes:
                    self.node_color[nodes] = color
        
        if action == "perso_edges_nodes_temporal_path":
            nodes_already_colored = []

            for edge in perso:
                for element in self.edge_color:
                    if element ==  (edge[0], edge[1]) or element == (edge[1], edge[0]):
                        self.edge_color[element] = 'lightcoral'
                
                if edge[0] not in nodes_already_colored:
                    nodes_already_colored.append(edge[0])
                    self.node_color[edge[0]] = 'firebrick'
                if edge[1] not in nodes_already_colored:
                    nodes_already_colored.append(edge[1])
                    self.node_color[edge[1]] = 'firebrick'
        
        if action == "reset_colors":
            self.changeColor("reset_color_nodes", perso=None)
            self.changeColor("reset_color_edges", perso=None)
            self.changeColor("reset_color_labels", perso=None)
        
        if action == "change_color_labels":
            text = self.askUser()
            self.edge_label_fontdict["color"] = text 

        self.centralWidget.figure.clf()
        self.ax = self.centralWidget.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
        self.centralWidget.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax.set_xlim(self.startX, self.scaleX)
        self.ax.set_ylim(self.startY, self.scaleY)

        self.positions = self.InteractiveGraph.node_positions
        self.InteractiveGraph  = nt.InteractiveGraph (self.graph, ax=self.ax, node_labels=True,node_layout=self.positions,node_color=self.node_color, edge_color=self.edge_color, edge_labels=self.edges_labels, node_size=self.node_size, edge_width=self.edge_width, edge_label_fontdict=self.edge_label_fontdict)

    # Drag&DRop

    def dragANode(self):
        # Click on canva
        if self.editingMode == True:
            print("Please go to moving mode.")
            return -1
        print("Please click on the canva.")
        self.centralWidget.isWaitingClickPosition = True
        self.disableAllActions()

    def dragAnEdge(self):
        if self.centralWidget.isWaitingClickTwoNodesPosition == True:
            self.reableAllActions()
            self.centralWidget.isWaitingClickTwoNodesPosition = False
            print("self.centralWidget.isWaitingClickTwoNodesPosition = ", self.centralWidget.isWaitingClickTwoNodesPosition)
            return -1
        if self.editingMode == True:
            print("Please go to moving mode.")
            return -1
        print("Please click on two nodes.")
        self.centralWidget.isWaitingClickTwoNodesPosition = True
        self.disableAllActions()
        self.createEdgeAction.setEnabled(True)

    def deletingMode(self):
        # Click one time
        if self.editingMode:
            print("Please go to mooving mode")
            return -1
        if self.deleting == False:
            print("if")
            self.deleting = True
            new_pix = QPixmap(os.path.join(os.path.dirname(__file__), "icons/minus_cancel.svg"))
            self.icon_deleting.addPixmap(new_pix)
            self.deleteNodeEdgeAction.setIcon(self.icon_deleting)
        # Click two times
        else:
            print("else")
            self.deleting = False
            new_pixx = QPixmap(os.path.join(os.path.dirname(__file__), "icons/minus.svg"))
            self.icon_deleting.addPixmap(new_pixx)
            self.deleteNodeEdgeAction.setIcon(self.icon_deleting)

    # Disable All actions

    def disableAllActions(self):

        for action in self.actions: 
            action.setEnabled(False)
        
        self.menuBar.setEnabled(False)

        for button in self.buttons:
            button.setEnabled(False)

    def reableAllActions(self):
        
        for action in self.actions:
            action.setEnabled(True)

        self.menuBar.setEnabled(True)

        for button in self.buttons:
            button.setEnabled(True)

    # Zoom

    def zoom(self, scale, key):

        if self.InteractiveGraph == None:
            print("Need figure to zoom.")
            return -1

        if key == "reset":
            self.scaleX = 1.0
            self.scaleY = 1.0
            self.startX = 0.0
            self.startY = 0.0

        elif key == "mooveLeft":
            self.startX -= 0.1
            self.scaleX -= 0.1
        elif key == "mooveRight":
            self.startX += 0.1
            self.scaleX += 0.1
        elif key == "mooveUp":
            self.startY += 0.1
            self.scaleY += 0.1
        elif key == "mooveDown":
            self.startY -= 0.1
            self.scaleY -= 0.1
        
        else:
            self.startX += scale
            self.startY += scale
            self.scaleX -= scale
            self.scaleY -= scale

        self.centralWidget.figure.clf()
        self.ax = self.centralWidget.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
        self.centralWidget.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
        print()
        self.ax.set_xlim(self.startX, self.scaleX)
        self.ax.set_ylim(self.startY, self.scaleY)

        self.InteractiveGraph  = nt.InteractiveGraph (self.graph, ax=self.ax, node_labels=True,node_layout=self.positions,node_color=self.node_color, edge_color=self.edge_color, edge_labels=self.edges_labels, node_size=self.node_size, edge_width=self.edge_width, edge_label_fontdict=self.edge_label_fontdict)

    # Click positions 
    
    def detect(self, x, y):
        """
        Detect position of the user-clikc and if the user click on a node or an edge.
        """

        self.clickPositionX = x
        self.clickPositionY = y

        detectedNode = None
        detectedEdge = None

        if self.InteractiveGraph != None:
            for node in self.graph.nodes:
                if self.InteractiveGraph.node_artists[node].contains_point((self.clickPositionX, self.clickPositionY), radius=0.1):
                    detectedNode = node
                    self.lastDetectedNode = node
            for edge in self.graph.edges:
                if self.InteractiveGraph.edge_artists[edge].contains_point((self.clickPositionX, self.clickPositionY), radius=0.1):
                    detectedEdge = edge
                    self.lastDetectedEdge = edge
        
        if self.centralWidget.isWaitingClickTwoNodesPosition == True and self.editingMode == False:
            # Name modification
            if self.InteractiveGraph == None or len(self.graph.nodes) < 2:
                print("No enough nodes.")
                self.reableAllActions()
                self.centralWidget.isWaitingClickTwoNodesPosition = False
            if detectedNode != None:
                if self.DragAnEdgeNode1 != None and self.DragAnEdgeNode2 == None:
                    self.DragAnEdgeNode2 = detectedNode
                if self.DragAnEdgeNode1 == None:
                    self.DragAnEdgeNode1 = detectedNode
                if self.DragAnEdgeNode1 != None and self.DragAnEdgeNode2 != None:
                    self.add_edge(self.DragAnEdgeNode1, self.DragAnEdgeNode2)
                    self.DragAnEdgeNode1 = None
                    self.DragAnEdgeNode2 = None
                    self.reableAllActions()
                    self.centralWidget.isWaitingClickTwoNodesPosition = False
                    return
        
        if self.deleting == True:
            if detectedNode != None:
                self.remove_node(detectedNode)
            elif detectedEdge != None:
                to_delete = detectedEdge[0] + "->" + detectedEdge[1]
                self.remove_edge(to_delete)
            self.deletingMode()

        if self.editingMode == False:
            return

        if detectedNode != None and detectedEdge != None:
            # Node priority
            detectedEdge = None
        
        if detectedNode != None:
            # Name modification
            self.changeNameNode(detectedNode)
            
        if detectedEdge != None:
            # Temporal label modification
            self.changeLabelEdge(detectedEdge)

    # Change mode : editing/Moving

    def selectEditingMode(self):
        # Click one time
        if self.editingMode == False:
            self.editingMode = True
            new_pix = QPixmap(os.path.join(os.path.dirname(__file__), "icons/pen.svg"))
            self.icon_editing.addPixmap(new_pix)
            self.editingModeAction.setIcon(self.icon_editing)
        # Click two times
        else:
            self.editingMode = False
            new_pix = QPixmap(os.path.join(os.path.dirname(__file__), "icons/hand.svg"))
            self.icon_editing.addPixmap(new_pix)
            self.editingModeAction.setIcon(self.icon_editing)

    # Size

    def changeSize(self, factor_node, factor_edge, factor_labels):

        if factor_node == None:
            #Reset
            self.node_size = 3.0
            self.edge_width = 1
            self.edge_label_fontdict["size"] = 12
        else:
            #Perso
            self.node_size = self.node_size*factor_node
            self.edge_width = self.edge_width*factor_edge
            self.edge_label_fontdict["size"] += factor_labels

        self.centralWidget.figure.clf()
        self.ax = self.centralWidget.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
        self.centralWidget.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax.set_xlim(self.startX, self.scaleX)
        self.ax.set_ylim(self.startY, self.scaleY)

        self.InteractiveGraph  = nt.InteractiveGraph (self.graph, ax=self.ax, node_labels=True,node_layout=self.positions,node_color=self.node_color, edge_color=self.edge_color, edge_labels=self.edges_labels, node_size=self.node_size, edge_width=self.edge_width, edge_label_fontdict=self.edge_label_fontdict)

    # Change name node

    def changeNameNode(self, node):
        # Change the name of the node:

        new_node = self.askUser()
        if new_node == -1:
            print("Cancel")
            return
        if new_node in self.graph.nodes:
            print("Please, choose an non already existing name.")
            return -1
        
        nx.relabel_nodes(self.graph, dict({node : new_node}), copy=False)

        # Change the color:
        self.node_color[new_node] = self.node_color[node]
        self.node_color.pop(node)
        self.edge_color = {(new_node if node == key[0] else key[0], new_node if node == key[1] else key[1]): value for key, value in self.edge_color.items()}
        # And the corresponding edges of the nodes:
        # Change the edge labels

        self.edges_labels = {(new_node if node == key[0] else key[0], new_node if node == key[1] else key[1]): value for key, value in self.edges_labels.items()}
        
        print('self.graph.edges = ', self.graph.edges)
        print('self.edges_labels.keys() = ', self.edges_labels.keys())

        for edge in self.graph.edges:
            if edge not in self.edges_labels.keys():
                self.edges_labels[edge] = self.edges_labels[(edge[1], edge[0])]
                self.edges_labels.pop((edge[1], edge[0]))

        # Update the positions : replace node by text
        self.positions = {new_node if node == key else key: value for key, value in self.positions.items()}
        self.nodeLayout(self.positions)
    
    # change temporal label of edges

    def changeLabelEdge(self, edge):
        # Change edges label

        # New name
        dialog = QDialog()
        dialog.setWindowTitle('Popup')
        dialog.layout = QVBoxLayout()
        dialog.setLayout(dialog.layout)

        dialog.label = QLabel('Entrez du texte:')
        dialog.text_edit = QLineEdit()
        dialog.submit_button = QPushButton('Valider')
        dialog.submit_button.clicked.connect(dialog.accept)

        dialog.layout.addWidget(dialog.label)
        dialog.layout.addWidget(dialog.text_edit)
        dialog.layout.addWidget(dialog.submit_button)

        if dialog.exec_():
            text = dialog.text_edit.text()
            print('Texte entré:', text)
        else:
            return -1
    
        self.edges_labels[edge] = text
        if ',' in text:
            labels_splited = text.split(",")
            for element in labels_splited:
                if int(element) > self.lifetime:
                    self.lifetime = int(element)
        else:
            if int(text) > self.lifetime:
                self.lifetime = int(text)
        self.nodeLayout(self.positions)
    
    # Stricte/Non-stricte

    def setStricte(self):
        self.stricte = not(self.stricte)
        
    # Temporal features

    def atLeastOneLarger(self, valueToCompare, setOfValues, key):
        finals_values = []
        if key == 'stricte' or key == True:
            for value in setOfValues:
                if value > valueToCompare:
                    finals_values.append(value)
        elif key == 'non-stricte' or key == False:
            for value in setOfValues:
                if value >= valueToCompare:
                    finals_values.append(value)
        
        if finals_values != []:
            return min(finals_values)
        else:
            return -1

    def isTemporalyConnected(self, one_edge, target, changeColor, method):
        # Pop-up : ask user

        if self.InteractiveGraph == None:
            print("A graph is needed.")
            return -1

        if one_edge != None:
            text = one_edge
        
        else:
            dialog = QDialog()
            dialog.setWindowTitle('Alert')
            dialog.layout = QVBoxLayout()
            dialog.setLayout(dialog.layout)

            dialog.label = QLabel('Please choose states:')
            dialog.text_edit = QLineEdit()
            dialog.submit_button = QPushButton('Valider')
            dialog.all_states_button = QPushButton('All states')
            dialog.submit_button.clicked.connect(dialog.accept)

            dialog.layout.addWidget(dialog.label)
            dialog.layout.addWidget(dialog.text_edit)
            dialog.layout.addWidget(dialog.submit_button)

            if dialog.exec_():
                text = dialog.text_edit.text()
            # Cancel case
            else:
                print("Cancel")
                return -1

        if re.match('.*->.*', text):
            node_from, node_to = text.split("->")
            if node_from not in self.graph.nodes or node_to not in self.graph.nodes:
                print("Please choose existing nodes.")
                return -1

        elif text not in self.graph.nodes and text != "all":
            print("Please choose an existing node.")
            return -1

        elif text == "all":
            # Node from =  node to = all the nodes
            new_nodes = [element for element in self.graph.nodes]
            for i in range(len(self.graph.nodes)):
                for j in range(i+1, len(self.graph.nodes)):
                    text = new_nodes[i] + "->" + new_nodes[j]
                    tmp = self.isTemporalyConnected(one_edge=text, target="all", changeColor=True, method="spanner")
                    if tmp == False or tmp == -1:
                        print("The graph is NOT temporally connected.")
                        return False
            
            print("The graph is temporally connected.")
            if changeColor == True:
                self.changeColor("perso_edges_nodes_temporal_path", self.graph.edges)
            return True
        else:
            node_from = text
            node_to = None

        # After a valid try, reset the color
        self.changeColor("reset_color_nodes", perso=None)
        self.changeColor("reset_color_edges", perso=None)

        for color in self.edge_color.keys():
            if self.edge_color[color] == "lightcoral":
                self.edge_color[color] = "#2c404c"
        for color in self.node_color.keys():
            if self.node_color[color] == "firebrick":
                self.node_color[color] = "w"

        if self.typeOfPath == "Foremost":
            _, labels, paths = self.foremost_temporal_dijkstra(node_from, min_value=-1)
            print("labels = ", labels)
            print("paths = ", paths)
        elif self.typeOfPath == "Shortest":
            _, labels, paths = self.shortest_temporal_dijkstra(self.graph, self.edges_labels, node_from)
        elif self.typeOfPath == "Fastest":
            if node_to != None:
                min_path, min_label, paths, labels = self.fastest_temporal_dijkstra(self.graph, self.edges_labels, node_from, node_to)
                print("min_path = ",min_path)
                print("min_label = ",min_label)
                print("paths = ",paths)
                print("labels = ",labels)
                if min_path != '':
                    print(f"{node_from} is temporally connected to {node_to}, path : {min_path}, labels : {min_label}")
                    edges = []
                    nodes = min_path
                    nodes = nodes.split("->")
                    for i in range(len(nodes) - 1):
                        if (nodes[i],nodes[i+1]) in self.graph.edges:
                            edges.append((nodes[i],nodes[i+1]))
                        elif (nodes[i+1],nodes[i]) in self.graph.edges:
                            edges.append((nodes[i+1],nodes[i]))
                    if target != "all":
                        print('Edges = ', edges)
                        self.changeColor("perso_edges_nodes_temporal_path", edges)
                    return 1
                else:
                    print(f"{node_from} is NOT temporally connected to {node_to}")
                    return -1
    
            else:
                max_value = 0
                # Find the maximum temporal value
                for key in self.edges_labels.keys():
                    labs = self.labelsToList(self.edges_labels[key])
                    for lab in labs:
                        if lab > max_value:
                            max_value = lab
                final_last_label = max_value
                for i in range(max_value+1):
                    _, labels, paths = self.foremost_temporal_dijkstra(node_from, min_value=i)
                    last_label = 0
                    last_person = None
                    for key in labels.keys():
                        if labels[key] != '':
                            labels_splited = labels[key].split("+")
                            last_person_duration = labels_splited[-1]
                            if int(last_person_duration) > last_label:
                                last_label = int(last_person_duration)
                                last_person = key
                    if last_person != None:
                        if last_label <= final_last_label:
                            final_last_label = last_label
                            final_person = last_person
                            final_paths_person = paths[last_person]
                            final_labels_person = labels[last_person]
                            final_paths = paths
                            final_labels = labels
                    
                print("Result : ")
                print("last person = ", final_person)
                print("last path = ", final_paths_person)
                print("last labels = ", final_labels_person)
                print("\n")
                paths = final_paths
                labels = final_labels

        edges_already = []
        finals_labels = []

        if text in self.graph.nodes:
            for element in paths.keys():
                brut_edges = node_from + paths[element]
                brut_labels = labels[element]
                if '->' in brut_edges:
                    fresh_nodes = brut_edges.split("->")
                    fresh_labels = brut_labels.split("+")
                    fresh_labels.pop(0)
                    for i in range(len(fresh_nodes)-1):
                        if (fresh_nodes[i], fresh_nodes[i+1]) not in edges_already:
                            finals_labels.append(fresh_labels[i])
                            edges_already.append((fresh_nodes[i], fresh_nodes[i+1]))
            print('Edges = ', edges_already)
            self.changeColor("perso_edges_nodes_temporal_path", edges_already)
            return 1
    
        if self.typeOfPath == "Fastest":
            return 1

        if node_to != None:
            if paths[node_to] != '':
                edges = []
                nodes = node_from + paths[node_to]
                nodes = nodes.split("->")
                for i in range(len(nodes) - 1):
                    if (nodes[i],nodes[i+1]) in self.graph.edges:
                        edges.append((nodes[i],nodes[i+1]))
                    elif (nodes[i+1],nodes[i]) in self.graph.edges:
                        edges.append((nodes[i+1],nodes[i]))
                if target != "all":
                    print('Edges = ', edges)
                    self.changeColor("perso_edges_nodes_temporal_path", edges)
            else:
                print("No connexion")
                return -1
        else:
            print("node : ", node_from)
            print("labels = ", labels)
            print("paths = ", paths)

        if method != "spanner":
            self.centralWidget.figure.clf()
            self.ax = self.centralWidget.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
            self.centralWidget.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
            self.ax.set_xlim(self.startX, self.scaleX)
            self.ax.set_ylim(self.startY, self.scaleY)

            self.positions = self.InteractiveGraph.node_positions

            self.InteractiveGraph  = nt.InteractiveGraph (self.graph, ax=self.ax, node_labels=True,node_layout=self.positions,node_color=self.node_color, edge_color=self.edge_color, edge_labels=self.edges_labels, node_size=self.node_size, edge_width=self.edge_width, edge_label_fontdict=self.edge_label_fontdict)
            
    def temporal_dijkstra(self, start_node):
        # init all the distances to inf
        distances  = {node:float('inf') for node in self.graph.nodes}
        # dist(A,A) = 0
        distances[start_node] = 0
        # labels
        labels = {node:'' for node in self.graph.nodes}
        # edges
        paths = {node:'' for node in self.graph.nodes}
        # nodes already visited
        visited = []

        pq = PriorityQueue()
        pq.put((0, start_node))

        while not pq.empty():
            (dist, current_node) = pq.get()
            visited.append(current_node)

            for neighbor in self.graph.neighbors(current_node):
                temporals_labels = []
                # Start : all temporals labels
                if (current_node, neighbor) in self.edges_labels.keys() and self.edges_labels[(current_node, neighbor)] != "":
                    temporals_labels = self.labelsToList(self.edges_labels[(current_node, neighbor)])
                elif (neighbor, current_node) in self.edges_labels.keys() and self.edges_labels[(neighbor, current_node)] != "":
                    temporals_labels = self.labelsToList(self.edges_labels[(neighbor, current_node)])
                # Processing : taking the min possible value
                temporals_label_available = self.atLeastOneLarger(dist, temporals_labels, self.stricte)
                print("temporals_label_available = ", temporals_label_available)
                # Edge current_node->neighbor is not possible
                if temporals_label_available and neighbor not in visited:
                    old_cost = distances[neighbor]
                    new_cost = temporals_label_available
                    if new_cost < old_cost:
                        labels[neighbor] = labels[current_node] + "+" + str(new_cost)
                        paths[neighbor] = paths[current_node] + "->" + neighbor
                        pq.put((new_cost, neighbor))
                        distances[neighbor] = new_cost
                    
        return distances, labels, paths

    # Restless : from https://appliednetsci.springeropen.com/articles/10.1007/s41109-020-00311-0

    # G = (V,E,T,alpha,Beta)
    # V = set of vertices
    # E = set of edges
    # T = lifetime
    # Beta = minimum waiting time
    # alpha = maximum waiting time

    def computes_optimal_walks(self):
        '''
        Algo from https://appliednetsci.springeropen.com/articles/10.1007/s41109-020-00311-0 p13
        
        Inputs:
            An instantaneous temporal graph G = (V, E, T, β)
            two cost functions c, cλ
            two vertex functions ind,A
            a source vertex s ∈ V.
        Output: 
            For each v ∈ V the specific length of an optimal s-v walk.
        Variables :
            opt(v) stores the value of an optimal walk from s to v within time interval [ 0, t];
            L(v) is a sorted list [ (opta1 , a1), . . . , (optak , ak)] where optai is an optimal value of a walk from s to v that arrives at time ai with t + β(v) ≤ ai ≤ t.
            δ1, ..., δ7 linear combination of the optimality criteria foremost, reverse-foremost, fastest, shortest, cheapest, minimum hop-count, and minimum waiting time, respectively.
        
        Case 1 : G is not an instantaneous temporal graph --> Use the transformation

        Case 2 : G is already an instantaneous temporal graph --> c = c', cλ ≡ 0, ind ≡ 1, and A ≡ 0

        We admit that :
            - all v in V have the same maximum waiting time beta
        
        '''
        text = self.askUser()

        if text == -1:
            print("Empty")
            return -1
        if '->' not in text:
            print("Bad format")
            return -1
        s, rest = text.split("->")
        if "," not in rest:
            print("Bad format")
            return -1
        target, beta = rest.split(",")
        beta = int(beta)
        # Initialisation
        opt = {node:np.inf for node in self.graph.nodes if node != s}
        ## Adaptation
        paths_walks = [s]
        paths_opt = {node:[] for node in self.graph.nodes if node != s}
        L = {node:[] for node in self.graph.nodes if node != s}
        # Compute delta
        delta = [1 if self.typeOfPath == "Foremost" else 0, 0, 1 if self.typeOfPath == "Fastest" else 0, 1 if self.typeOfPath == "Shortest" else 0, 0, 0, 0]
        # Tentative to get the paths/walk
        V_prime_s = []
        E_t_g_s = []
        E_r_s = []

        for t in range(1,self.lifetime+1):
            # Compute E_t, need to be != None
            E_t, V_t = self.E(t)
            if E_t != dict():
                V_t_g, E_t_g, E_r, d_t, d_r = self.generateGraph(t, s, delta, L, beta)
                curr_etg = []
                for node_f, node_t in E_t_g:
                    if (node_f, node_t) not in curr_etg and (node_t, node_f) not in curr_etg:
                        curr_etg.append((node_f, node_t))
                E_t_g_s.append(curr_etg)
                E_r_s.append(E_r)
                if () in E_t_g | E_r:
                    E_t_g.remove(())
                V_prime, opt_t, V_prime_edges = self.modDijkstra(t, s,V_t_g, E_t_g | E_r, d_t, d_r)
                V_prime_s.append(V_prime)

                for v in V_prime:
                    # Update step
                    if v != s:
                        if min(opt[v], delta[0]*t - delta[1]*self.lifetime + delta[2]*(t-self.lifetime) + opt_t[v]) == delta[0]*t - delta[1]*self.lifetime + delta[2]*(t-self.lifetime) + opt_t[v] and opt[v] != delta[0]*t - delta[1]*self.lifetime + delta[2]*(t-self.lifetime) + opt_t[v]:
                            paths_walks.append(v)
                            finded_edges = []
                        opt[v] = min(opt[v], delta[0]*t - delta[1]*self.lifetime + delta[2]*(t-self.lifetime) + opt_t[v])
                        # Delete redundants tuples
                        signal = True
                        for opt_,a_ in L[v]:
                            if t < a_ and opt_ <= opt_t[v] + delta[6] * 1 * (a_ - t):
                                signal = False
                        if signal == True:
                            L[v].append((opt_t[v], t))          

        print("sorted = ", sorted(opt.items(), key=lambda t: t[1]) )
        colored = []
    
        for element in E_t_g_s:
            colored.append(element)
            for obj in element:
                if obj[0] == s:
                    paths_opt[obj[1]].append([obj])
                elif obj[1] == s:
                    paths_opt[obj[0]].append([obj])
                else:
                    # Identify wich node is already known
                    # case [], Known
                    if paths_opt[obj[0]] == [] and paths_opt[obj[1]] != []:
                
                        for paths in paths_opt[obj[1]]:
                            curr = []
                            for edg in paths:
                                curr.append(edg)
                            curr.append(obj)
                            paths_opt[obj[0]].append(curr)
                    # case Known, []
                    elif paths_opt[obj[1]] == [] and paths_opt[obj[0]] != []:
                        
                        for paths in paths_opt[obj[0]]:
                            curr = []
                            for edg in paths:
                                curr.append(edg)
                            curr.append(obj)
                            paths_opt[obj[1]].append(curr)
                    # case Known, Known
                    else:
                        # Add a path
                        # node 1
                        for paths in paths_opt[obj[1]]:
                            curr = []
                            for edg in paths:
                                curr.append(edg)
                            curr.append(obj)
                            paths_opt[obj[0]].append(curr)
                        # Node 2
                        for paths in paths_opt[obj[0]]:
                            curr = []
                            for edg in paths:
                                curr.append(edg)
                            curr.append(obj)
                            paths_opt[obj[1]].append(curr)
        final_paths_opt = {node:[] for node in self.graph.nodes if node != s}
        for key in paths_opt.keys():
            visited_paths = []
            for paths in paths_opt[key]:
                var_time = 0
                paths_cpy = copy.deepcopy(paths)
                new_paths = []
                while len(paths_cpy) > 0:
                # for edge in paths:
                    edge = paths_cpy.pop(0)
                    verif = True
                    all_labels = []
                    labels = self.labelsToList(self.edges_labels[edge])
                    for label in labels:
                        if label <= var_time + beta:
                            all_labels.append(label)
                            new_paths.append(edge)
                    if all_labels != []:
                        # delete this paths
                        var_time = min(all_labels)
                    else:
                        # Regarde si un allé retour n'est pas possible
                        # var_time = 5
                        # edge = C,F
                        # Je dois trouver le node from = commun
                        if len(new_paths) == 1:
                            if new_paths[0][0] == s:
                                commun = new_paths[0][1]
                            else:
                                commun = new_paths[0][0]
                        if len(new_paths) >= 2:
                            if new_paths[-1][0] in new_paths[-2]:
                                commun = new_paths[-1][1]
                            else:
                                commun = new_paths[-1][0]
                        finded = False
                        for k in self.edges_labels.keys():
                            if commun in k and finded == False:
                                all_labels_to_test = []
                                labels_to_test = self.labelsToList(self.edges_labels[k])

                                for label in labels_to_test:
                                    if label > var_time and label <= var_time + beta:
                                        all_labels_to_test.append(label)
                                if all_labels_to_test != []:
                                    var_time = min(all_labels_to_test)
                                    finded = True
                                    new_paths.append(k)
                                    new_paths.append(k)
                                    paths_cpy.insert(0,edge)
                        if all_labels_to_test == []:
                            verif = False
                                    
                if new_paths not in final_paths_opt[key] and verif == True:
                    final_paths_opt[key].append(new_paths)

        self.changeColor("reset_color_edges", perso=None)
        self.changeColor("reset_color_nodes", perso=None)

        if final_paths_opt[target] != []:
            lon = np.inf
            for element in final_paths_opt[target]:
                if len(element) < lon:
                    final_path = element
                    lon = len(element)
            print("ELEMENT == ", final_path)
            self.changeColor("perso_edges_nodes_temporal_path", perso=final_path)

        return opt
    
    def generateGraph(self, t, s, delta, L, beta):
        E_t, V_t = self.E(t)

        # Initilisation
        E_r = []
        d_r = {(v,w):np.inf for v in (set(V_t) | set(s)) for w in (set(V_t) | set(s))}
        d_t = {(v,w):np.inf for v in (set(V_t) | set(s)) for w in (set(V_t) | set(s))}
        for v,w in E_t:
            if v == s:
                # Here, we admit that c_lamba = c = 0
                d_t[(v,w)] = (delta[1]+delta[2]) * (self.lifetime - t) + delta[3] * 0 + delta[4] * 0 + delta[5]
            else:
                d_t[(v,w)] = delta[3] * 0 + delta[4] * 0 + delta[5]
        
        for v in V_t:
            if v != s:
                tuples_to_delete = []
                for opt_, a_ in L[v]:
                    if a_ + beta < t:
                        tuples_to_delete.append((opt_, a_))
                L[v] = [item for item in L[v] if item not in tuples_to_delete]
                if L[v] != []:
                    if (s,v) not in E_r:
                        E_r.append((s,v))
                    # NOT SURE
                    opt = min(opt_ for opt_, a_ in L[v])
                    # Here, we admit that ind(A) = 0 and A = 0
                    d_r[(s,v)] = opt + delta[6] * 1 * (t - a_ + 0)
        E_t_keys = E_t.keys()
        return set(V_t) | set(s), E_t_keys, set(E_r), d_t, d_r

    def modDijkstra(self, t, s, V_t_g, E_t_g, d_t, d_r):
        # Initialisation
        E_t, V_t = self.E(t)
        opt_t = {node:np.inf for node in V_t}
        r = {node:np.inf for node in V_t}
        r[s] = 0
        Q = [node for node in V_t_g]
        V_prime = []
        V_prime_edges = []
        while Q != []:
            chosen_node = None
            chosen_r = np.inf
            for node in Q:
                if node in r.keys():
                    if r[node] <= chosen_r:
                        chosen_r = r[node]
                        chosen_node = node
            v = chosen_node
            if v != None:
                Q.remove(v)
            for v,w in E_t_g:
                r[w] = min( r[w], r[v] + min(d_t[(v,w)], d_r[(v,w)]) )
                if (v,w) in E_t:
                    opt_t[w] = min(opt_t[w], r[v] + d_t[(v,w)])
                    V_prime = set(V_prime) | set(w)
                    if [v,w] not in V_prime_edges and [w,v] not in V_prime_edges:
                        V_prime_edges.append([v,w])
        return V_prime, opt_t, V_prime_edges


    # Temporal Connectivity : algo from https://arxiv.org/pdf/1404.7634

    def E(self,time_i):
        """
        Edge set a time i.
        """
        # print("self.edges = ", self.graph.edges)

        E = dict()
        V = []

        for edge in self.graph.edges:
            edge_from = edge[0]
            edge_to = edge[1]
            if (edge_from, edge_to) in self.edges_labels.keys():
                edge_to_consider = self.edges_labels[(edge_from, edge_to)]
            elif (edge_to, edge_from) in self.edges_labels.keys():
                edge_to_consider = self.edges_labels[(edge_to, edge_from)]
            else:
                return -1
            
            # str contains "," or not
            if "," in edge_to_consider:
                labels = edge_to_consider.split(",")
            else:
                labels = [edge_to_consider]

            if str(time_i) in labels:
                # print("yes")
                E[edge] = time_i
                E[(edge_to, edge_from)] = time_i
            
            for key in E.keys():
                node_from, node_to = key
                if node_from not in V:
                    V.append(node_from)
                if node_to not in V:
                    V.append(node_to)
            
        return E, V

    def P(self,node_v,time_t):
        """
        NOT USED

        Let P(v, t) be the set of known predecessors of
        v by the end of the t first steps of the algorithm (i.e. after taking into account edge sets:
        E1, ..., Et).
        """
        P_v_t = []
        E_t = [self.E(i) for i in range(1,time_t+1)]
        print("E_t = ", E_t)
        for E_i in E_t:
            edges_i = E_i.keys()
            for edge_i in edges_i:
                (node_i_from, node_i_to) = edge_i
                if node_i_from == node_v and node_i_to not in P_v_t:
                    P_v_t.append(node_i_to)
                elif node_i_to == node_v and node_i_from not in P_v_t:
                    P_v_t.append(node_i_from)
        
        return P_v_t

    def G_s_t(self):
        # Initialization
        Rho = {node:set([node]) for node in self.graph.nodes}
        Rho_plus = {node:set([]) for node in self.graph.nodes}
        # 
        for i in range(self.lifetime+1):
            updateV = set([])
            E_i, _ = self.E(i)

            if self.stricte == False:
                E_i = self.transitive_closure(E_i)
            # List predecessors induced by the edges in Ei
            for element in E_i:
                (u,v) = element
                Rho_plus[v] = Rho_plus[v].union(Rho[u]) # =  {'D', 'B', 'C', 'A'}
                updateV = updateV.union(set([v]))
            # Add found predecessors to known predecessors
            for v in updateV:
                Rho[v] = Rho[v].union(Rho_plus[v])
                Rho_plus[v] = set([])
            # Test whether transitive closure is complete; if so, terminates
            is_complete = True
            for v in self.graph.nodes:
                if len(Rho[v]) < len(self.graph.nodes):
                    is_complete = False
                    break
            if is_complete:
                # The algorithm terminates returning a complete graph (edges)
                complete_edge = []
                for u in self.graph.nodes:
                    for v in self.graph.nodes:
                        if u != v:
                            complete_edge.append((u,v))
                return complete_edge
        # Build transitive closure based on predecessors
        E_star = set([])
        for v in self.graph.nodes:
            for u in Rho[v]:
                if u != v:
                    edge = (u,v)
                    if edge not in E_star:
                        E_star.add(edge)
        return E_star
    
    def G_s_t_bitsets(self):
        # Initialization
        Rho = {node:set([node]) for node in self.graph.nodes}
        Rho_plus = {node:set([]) for node in self.graph.nodes}
        # Adaptation bitsets
        Nodes_bitsets = bitset('Nodes_bitsets',tuple(self.graph.nodes))

        for i in range(self.lifetime+1):
            updateV = set([])
            E_i, _ = self.E(i)

            if self.stricte == False:
                E_i = self.transitive_closure(E_i)
            # List predecessors induced by the edges in Ei
            for element in E_i:
                (u,v) = element
                # Adaptation bitsets
                # Creation of bitsets
                Rho_to_bits = Nodes_bitsets(tuple(Rho[u])).bits()
                Rho_plus_to_bit = Nodes_bitsets(tuple(Rho_plus[v])).bits()
                # Bitsets "union" , replace the set union
                res = int(Rho_to_bits,2) | int(Rho_plus_to_bit,2)
                # 0b101011 --> 101011
                res = bin(res)[2:]
                # 101011 --> 00101011
                resultat_binaire_padded = res.zfill(len(self.graph.nodes))
                # 00101011 --> [C,E,G,H]
                Rho_plus[v] = set(Nodes_bitsets.frombits(str(resultat_binaire_padded)))

                # Creation of bitset
                updateV_to_bit = Nodes_bitsets(tuple(updateV)).bits()
                v_to_bit = Nodes_bitsets(tuple(v)).bits()
                # Bitsets "union" , replace the set union
                updateV_bitsets = int(updateV_to_bit,2) | int(v_to_bit,2)
                # 0b101011 --> 101011
                updateV_bitsets = bin(updateV_bitsets)[2:]
                # 101011 --> 00101011
                resultat_binaire_padded = updateV_bitsets.zfill(len(self.graph.nodes))
                # 00101011 --> [C,E,G,H]
                updateV = set(Nodes_bitsets.frombits(str(resultat_binaire_padded)))

            # Add found predecessors to known predecessors
            for v in updateV:

                Rho_to_bits = Nodes_bitsets(tuple(Rho[v])).bits()
                Rho_plus_to_bit = Nodes_bitsets(tuple(Rho_plus[v])).bits()
                res = int(Rho_to_bits,2) | int(Rho_plus_to_bit,2)
                res = bin(res)[2:]
                resultat_binaire_padded = res.zfill(len(self.graph.nodes))
                res_union = set(Nodes_bitsets.frombits(str(resultat_binaire_padded)))

                Rho[v] = res_union
                Rho_plus[v] = set([])
            # Test whether transitive closure is complete; if so, terminates
            is_complete = True
            for v in self.graph.nodes:
                if len(Rho[v]) < len(self.graph.nodes):
                    is_complete = False
                    break
            if is_complete:
                # The algorithm terminates returning a complete graph (edges)
                complete_edge = []
                for u in self.graph.nodes:
                    for v in self.graph.nodes:
                        if u != v:
                            complete_edge.append((u,v))
                return complete_edge
        # Build transitive closure based on predecessors
        E_star = set([])
        for v in self.graph.nodes:
            for u in Rho[v]:
                if u != v:
                    edge = (u,v)
                    if edge not in E_star:
                        E_star.add(edge)
        return E_star

    def G_s_t_bitsets_tentative(self):
        # Initialization
        Rho = {node:set([node]) for node in self.graph.nodes}
        Rho_plus = {node:set([]) for node in self.graph.nodes}
        # 
        Nodes_bitsets = bitset('Nodes_bitsets',tuple(self.graph.nodes))
        for i in range(self.lifetime+1):
            updateV = set([])
            E_i, _ = self.E(i)

            if self.stricte == False:
                E_i = self.transitive_closure(E_i)
            # List predecessors induced by the edges in Ei
            for element in E_i:
                (u,v) = element
                Rho_to_bits = Nodes_bitsets(tuple(Rho[u]))
                Rho_plus_to_bit = Nodes_bitsets(tuple(Rho_plus[v]))
                v_to_bit = Nodes_bitsets(tuple(v))
                updateV_to_bit = Nodes_bitsets(tuple(updateV))
                Rho_plus[v] = Rho_to_bits.union(Rho_plus_to_bit)
                updateV = updateV_to_bit.union(v_to_bit)
            # Add found predecessors to known predecessors
            for v in updateV:
                Rho_to_bits = Nodes_bitsets(tuple(Rho[u]))
                Rho_plus_to_bit = Nodes_bitsets(tuple(Rho_plus[v]))
                Rho[v] = Rho_plus_to_bit.union(Rho_to_bits)
                Rho_plus[v] = set([])
            # Test whether transitive closure is complete; if so, terminates
            is_complete = True
            for v in self.graph.nodes:
                if len(Rho[v]) < len(self.graph.nodes):
                    is_complete = False
                    break
            if is_complete:
                # The algorithm terminates returning a complete graph (edges)
                complete_edge = []
                for u in self.graph.nodes:
                    for v in self.graph.nodes:
                        if u != v:
                            complete_edge.append((u,v))
                return complete_edge
        # Build transitive closure based on predecessors
        E_star = set([])
        for v in self.graph.nodes:
            for u in Rho[v]:
                if u != v:
                    edge = (u,v)
                    if edge not in E_star:
                        E_star.add(edge)
        return E_star

    def transitive_closure(self, a):
        '''
        E_i in a non-strict case
        '''
        closure = set([])
        for key in a.keys():
            closure.add(key)
        new_dict = a
        while True:
            new_relations = {(x,w):new_dict[(q,w)] for x,y in closure for q,w in closure if q == y and x != w}
            new_relations_set = {(x,w) for x,y in closure for q,w in closure if q == y and x != w}

            for key in a.keys():
                new_relations[key] = a[key]
            
            new_relations_set = new_relations_set | closure

            if new_relations_set == closure:
                break

            closure = new_relations_set
            new_dict = new_relations

        return closure

    # Delegation : based on https://www.sciencedirecAVt.com/science/article/pii/S0022000021000428#se0110

    def delegation(self, node_v, verbose):
        '''
        Find e^+(v) and e^-(v)
        '''
        # Ask user the node to find both e^+ and e^-
        if node_v == None:
            node = self.askUser()
        else:
            node = node_v

        if node not in self.graph.nodes:
            print("Node not in graph.")
            return -1

        # Keep the edges implied
        incident_node = dict()
        for key in self.edges_labels.keys():
            edge = key
            if node in edge:
                incident_node[edge] = self.edges_labels[edge]
        e_plus = [None, -1]
        e_moins = [None,np.inf]
        for key in incident_node.keys():
            labels = self.labelsToList(incident_node[key])
            for label in labels:
                if label > e_plus[1]:
                    e_plus[0] = key
                    e_plus[1] = label
                if label < e_moins[1]:
                    e_moins[0] = key
                    e_moins[1] = label
        if verbose == True:
            print(f"incident node = {incident_node}")
            print(f"e_plus = {e_plus}")
            print(f"e_moins = {e_moins}")
        return incident_node, e_plus, e_moins

    def vertex_dismountability(self, node_v, verbose):
        '''
        Use the delegation to find a dismountable vertex.
        '''
        # Ask user the node to find both e^+ and e^-
        if node_v == None:
            node = self.askUser()
        else:
            node = node_v
        incident_nodes, e_plus, e_moins = self.delegation(node, verbose=False)

        nodes_incident_to_node_v = [u if u != node else v for u, v in incident_nodes]

        for u in nodes_incident_to_node_v:
            for w in nodes_incident_to_node_v:
                # Change this conditions if 1+hop dismountable
                if u != w:
                    _, e_plus_u, e_moins_u = self.delegation(u, verbose=False)
                    _, e_plus_w, e_moins_w = self.delegation(w, verbose=False)
                    if node in e_plus_u[0] and node in e_moins_w[0]:
                        # Find a dismountablme vertex
                        if verbose == True:
                            print("Dismountable vertex !")
                            print(f"{e_plus_u}, {e_moins_w}")
                        self.changeColor("perso_edges_nodes_temporal_path", perso=[e_plus_u[0],e_moins_w[0]])
                        return u,w,e_plus_u, e_moins_w
                    if node in e_plus_w[0] and node in e_moins_u[0]:
                        if verbose == True:
                            print("Dismountable vertex !")
                            print(f"{e_plus_w}, {e_moins_u}")
                        self.changeColor("perso_edges_nodes_temporal_path", perso=[e_plus_u[0],e_moins_w[0]])
                        return u,w,e_plus_w, e_moins_u
        return -1,-1,-1,-1
    
    def spanner_dismountability(self):
        """
        Find spanner using dismountability
        """
        # Need complete graph
        if len(self.graph.edges) != (len(self.graph.nodes) * (len(self.graph.nodes)-1))/2:
            print("Need complete graph to compute spanner with dismountability features.")
            return -1
        # Reset colors
        self.changeColor("reset_color_edges", perso=None)
        self.changeColor("reset_color_nodes", perso=None)

        nodes_to_dismount = [node for node in self.graph.nodes]
        # Finals edges of the spanner
        edges_in_spanner = []
        order = []
        # If a node is dismoutable, we delete edges
        edges_labels_copy = copy.deepcopy(self.edges_labels)
        for node in nodes_to_dismount:
            u,w,e_plus_w, e_moins_u = self.vertex_dismountability(node, verbose=False)
            if u == -1 or w == -1 or e_plus_w == -1 or e_moins_u == -1:
                pass
            else:
                # We need to delete all the edges related to the node
                keys = []
                for key in self.edges_labels.keys():
                    if node in key:
                        keys.append(key)
                for element in keys:
                    if element in self.edges_labels.keys():
                        _ = self.edges_labels.pop(element)
                    else:
                        _ = self.edges_labels.pop((element[1], element[0]))
                    edges_in_spanner.append(e_plus_w[0])
                    edges_in_spanner.append(e_moins_u[0])

        # Final condition : 2 nodes left
        if len(self.edges_labels) == 1:
            for key in self.edges_labels:
                edges_in_spanner.append(key)
            self.edges_labels = edges_labels_copy
            order = []
            for element in edges_in_spanner:
                if element not in order:
                    order.append(element)
            num = 0
            for i in range(0,len(order)-1,2):
                num = i
                principal = None
                second = []

                for element in order[i]:
                    if element in order[i+1]:
                        principal = element
                    else:
                        second.append(element)

                for element in order[i+1]:
                    if element in order[i]:
                        principal = element
                    else:
                        second.append(element)

                print(f"Step {i+1}, {second[0]}<---->{principal}<---->{second[1]}")
            
            print(f"Step {num+1}, {order[num+1][0]}<---->{order[num+1][0]}")
                    
            self.changeColor(action="perso_edges_nodes_temporal_path", perso=edges_in_spanner)
        else:
            self.edges_labels = edges_labels_copy
            print("The graph is not fully dismountable.")
            return -1

    # WORKING

    def setForemostShortestFastest(self, key):
        self.typeOfPath = key

    def setPathOrWalk(self,key):
        self.typeOfWay = key

    def foremost_temporal_dijkstra(self, start_node, min_value):
        """
        Adaptation of the famous dijkstra algo to find the foremost temporal path.
        Here, using priority on temporal label not weight.
        
        Input :
            - start_node : source node.
            - min_value : start the algorithm at this value.

        Output :
            - distances : distances used
            - labels : labels used
            - paths : Paths used
        """
        # init all the distances to inf
        distances  = {node:float('inf') for node in self.graph.nodes}
        # dist(A,A) = 0
        distances[start_node] = 0
        # labels
        labels = {node:'' for node in self.graph.nodes}
        # edges
        paths = {node:'' for node in self.graph.nodes}
        # nodes already visited
        visited = []

        pq = PriorityQueue()
        pq.put((min_value, start_node))

        while not pq.empty():
            (dist, current_node) = pq.get()
            visited.append(current_node)
            for neighbor in self.graph.neighbors(current_node):
                temporals_labels = []
                # Start : all temporals labels
                if (current_node, neighbor) in self.edges_labels.keys() and self.edges_labels[(current_node, neighbor)] != "":
                    temporals_labels = self.labelsToList(self.edges_labels[(current_node, neighbor)])
                elif (neighbor, current_node) in self.edges_labels.keys() and self.edges_labels[(neighbor, current_node)] != "":
                    temporals_labels = self.labelsToList(self.edges_labels[(neighbor, current_node)])
                temporals_label_available = self.atLeastOneLarger(dist, temporals_labels, self.stricte)
                if temporals_label_available != -1 and neighbor not in visited:
                    old_cost = distances[neighbor]
                    new_cost = temporals_label_available
                    if new_cost <= old_cost:
                        labels[neighbor] = labels[current_node] + "+" + str(new_cost)
                        paths[neighbor] = paths[current_node] + "->" + neighbor
                        pq.put((new_cost, neighbor))
                        distances[neighbor] = new_cost
                    
        return distances, labels, paths

    def shortest_temporal_dijkstra(self, graph, edges_labels, start_node):
        """
        Adaptation of the famous dijkstra algo to find the shortest temporal path.
        Here, using priority on temporal label not weight.
        
        Input :
            - graph : considered graph.
            - edges_labels : labels on edges.
            - start_node : source node.
        Output :
            - distances : distances used
            - labels : labels used
            - paths : Paths used
        """
        # init all the distances to inf
        distances  = {node:float('inf') for node in graph.nodes}
        # dist(A,A) = 0
        distances[start_node] = 0
        # labels
        labels = {node:'' for node in graph.nodes}
        # edges
        paths = {node:'' for node in graph.nodes}
        # nodes already visited
        considered = [start_node]

        queue = [(0, start_node)]
        while len(queue) != 0   :
            (dist, current_node) = queue.pop(0)

            for neighbor in graph.neighbors(current_node):
                temporals_labels = []
                # Start : all temporals labels
                if (current_node, neighbor) in edges_labels.keys() and edges_labels[(current_node, neighbor)] != "":
                    temporals_labels = self.labelsToList(edges_labels[(current_node, neighbor)])
                elif (neighbor, current_node) in edges_labels.keys() and edges_labels[(neighbor, current_node)] != "":
                    temporals_labels = self.labelsToList(edges_labels[(neighbor, current_node)])

                if labels[current_node] == '':
                    min_label = dist
                else:
                    min_label = int(labels[current_node][-1])
                temporals_label_available = self.atLeastOneLarger(min_label, temporals_labels, self.stricte)

                if temporals_label_available != -1 and neighbor not in considered:
                    queue.append((dist+1, neighbor))
                    labels[neighbor] = labels[current_node] + "+" + str(temporals_label_available)
                    paths[neighbor] = paths[current_node] + "->" + neighbor
                    distances[neighbor] = dist+1
                    considered.append(neighbor)
                        
        return distances, labels, paths

    def fastest_temporal_dijkstra(self, graph, edges_labels, node_from, node_to):
        '''
        Greedy method.
        Find the fastest journey using foremost from every time label and taking the minimum one.

        Inputs :
            - graph : considered graph.
            - edges_labels : labels on edges.
            - node_from : starting node.
            - node_to : ending node.
        
        Outputs :
            - min_path : shortest path.
            - min_labels : sortest labels.
            - finals_paths : paths.
            - finals_labels : labels.

        '''
        max_value = 0
        # Find the maximum temporal value
        for key in edges_labels.keys():
            labs = self.labelsToList(edges_labels[key])
            for lab in labs:
                if lab > max_value:
                    max_value = lab
        min_diff = float('inf')
        min_path = ''
        min_labels = ''
        finals_paths = []
        finals_labels = []
        for i in range(max_value+1):
            _, labels, paths = self.foremost_temporal_dijkstra(node_from, min_value=i)
            print("labels = ",labels)
            print("paths = ", paths)
            print("\n")
            if paths[node_to] != '':
                all_str_path = node_from + paths[node_to]
                all_labels = labels[node_to][1:].split("+")
                diff = int(all_labels[-1]) - int(all_labels[0])
                if diff < min_diff:
                    min_diff = diff
                    min_path = all_str_path
                    min_labels = all_labels
                    finals_paths = paths
                    finals_labels = labels

        return min_path, min_labels, finals_paths, finals_labels

    def bipath(self, key, target): 

        if self.InteractiveGraph == None:
            print("A graph is needed.")
            return -1

        if key != None:
            text = key

        else:
            dialog = QDialog()
            dialog.setWindowTitle('Alert')
            dialog.layout = QVBoxLayout()
            dialog.setLayout(dialog.layout)

            dialog.label = QLabel('Please choose states:')
            dialog.text_edit = QLineEdit()
            dialog.submit_button = QPushButton('Valider')
            dialog.all_states_button = QPushButton('All states')
            dialog.submit_button.clicked.connect(dialog.accept)

            dialog.layout.addWidget(dialog.label)
            dialog.layout.addWidget(dialog.text_edit)
            dialog.layout.addWidget(dialog.submit_button)

            if dialog.exec_():
                text = dialog.text_edit.text()
            # Cancel case
            else:
                print("Cancel")
                return -1
            
        if re.match('.*->.*', text):
            node_from, node_to = text.split("->")
            if node_from not in self.graph.nodes or node_to not in self.graph.nodes:
                print("Please choose existing nodes.")
                return -1

        elif text == "all":
            # Node from =  node to = all the nodes
            new_nodes = [element for element in self.graph.nodes]
            is_entiere_bpp = True
            for i in range(len(self.graph.nodes)):
                for j in range(i+1, len(self.graph.nodes)):
                    text = new_nodes[i] + "->" + new_nodes[j]
                    tmp = self.bipath(key=text, target="all")
                    if tmp == False or tmp == -1:
                        is_entiere_bpp = False
            
            if is_entiere_bpp == True:
                print("The graph solve the bpp.")
                self.changeColor("perso_edges_nodes_temporal_path", self.graph.edges)
            else:
                print("The graph NOT solve the bpp.")
            return 1

        elif text not in self.graph.nodes:
            print("Please choose an existing node.")
            return -1
        else:
            node_from = text
            node_to = None

        new_edges = []
        for edge in self.edges_labels.keys():
            new_edges.append( [ edge, self.labelsToList(self.edges_labels[edge]) ]) 

        for color in self.edge_color.keys():
            if self.edge_color[color] == "lightcoral":
                self.edge_color[color] = "#2c404c"
        for color in self.node_color.keys():
            if self.node_color[color] == "firebrick":
                self.node_color[color] = "w"

        bpp = Problem.BidirectionalPathProblem("Bidirectional Path Problem",self.graph.nodes, new_edges, start=node_from, target=[node_to], key=self.stricte)
        print("bpp created !")

        solutions = bpp.solve()

        new_graph, edges_labels = solutions.to_graph()

        if len(new_graph.edges) == 0:
            print("No solution to the bpp.")
            self.centralWidget.figure.clf()
            self.ax = self.centralWidget.figure.add_subplot(111, position=[0.0, 0.0, 1.0, 1.0])
            self.centralWidget.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
            self.ax.set_xlim(self.startX, self.scaleX)
            self.ax.set_ylim(self.startY, self.scaleY)
            self.positions = self.InteractiveGraph.node_positions
            self.InteractiveGraph  = nt.InteractiveGraph (self.graph, ax=self.ax, node_labels=True,node_layout=self.positions,node_color=self.node_color, edge_color=self.edge_color, edge_labels=self.edges_labels, node_size=self.node_size, edge_width=self.edge_width, edge_label_fontdict=self.edge_label_fontdict)
            return -1
        
        _, labels, paths = self.shortest_temporal_dijkstra(new_graph, edges_labels, node_from)
        _, labels_to, paths_to = self.shortest_temporal_dijkstra(new_graph, edges_labels, node_to)

        if paths[node_to] != '':

            # Juste pour mettre en page
            final_path = node_from + paths[node_to]
            path_split = final_path.split("->")
            labels_from = labels[node_to].split('+')
            labels_to = labels_to[node_from].split('+')
            from_to = node_from
            to_from = node_from
            for i in range(1, len(path_split)):
                from_to = from_to + '--' + labels_from[i] + '-->' + path_split[i]
                to_from = to_from + '<--' + labels_to[i] + '--' + path_split[i]
            print(f"{node_from} is temporally connected to {node_to}, paths : {from_to}, {to_from}")

            edges = []
            nodes = node_from + paths[node_to]
            nodes = nodes.split("->")
            for i in range(len(nodes) - 1):
                if (nodes[i],nodes[i+1]) in self.graph.edges:
                    edges.append((nodes[i],nodes[i+1]))
                elif (nodes[i+1],nodes[i]) in self.graph.edges:
                    edges.append((nodes[i+1],nodes[i]))
            if target != "all":
                self.changeColor("perso_edges_nodes_temporal_path", edges)
        else:
            print(f"{node_from} is NOT temporally connected to {node_to}")
            return -1

    # TENTATIVES

    def fastest_temporal(self):
        """
        TENTATIVE
        Implementation of Algo 3 & 4 from https://inria.hal.science/inria-00071996/file/RR-4589.pdf
        NOT WORKING
        """
        pass

    def shortest_temporal(self,start_node):
        '''
        TENTATIVE
        Implement algo from https://inria.hal.science/inria-00071996/file/RR-4589.pdf
        NOT WORKING
        '''
        # Step 1
        T = [(start_node,0,0)]
        earliest = {node:float('inf') for node in self.graph.nodes}
        earliest[start_node] = 0
        # Step 2
        d = 1
        # Step 3 
        location = dict()
        location[start_node] = (start_node,0)
        parents = { (start_node, 0): None }
        # Step 4
        while len(location) != len(earliest):
            # Step 4 : a
            for pair in T:
                if pair[2] != d-1:
                    continue
                # Step 4 : a : i
                for neighbor in self.graph.neighbors(pair[0]):
                    if (pair[0], neighbor) in self.edges_labels.keys() and self.edges_labels[(pair[0], neighbor)] != "":
                        temporals_labels = self.labelsToList(self.edges_labels[(pair[0], neighbor)])
                    elif (neighbor, pair[0]) in self.edges_labels.keys() and self.edges_labels[(neighbor, pair[0])] != "":
                        temporals_labels = self.labelsToList(self.edges_labels[(neighbor, pair[0])])
                    temporals_label_available = self.atLeastOneLarger(-1, temporals_labels, self.stricte)
                    # Step 4 : a : ii
                    if neighbor not in location.keys():
                        location[neighbor] = (neighbor, temporals_label_available)
                    if earliest[neighbor] > temporals_label_available:
                        earliest[neighbor] = temporals_label_available
                        T.append((neighbor,temporals_label_available,d))
                        parents[(neighbor,temporals_label_available)] = (pair[0], pair[1])
            # Step 4 : b
            d = d+1
        print('T = ', T)
        print('location = ', location)
        print('parents = ', parents)
        return T, location, parents

    # Spanner

    def minimalSpanner(self, bitsets):
        print("Running...")
        # Reset the color
        self.changeColor("reset_color_edges", perso=None)
        self.changeColor("reset_color_nodes", perso=None)
        # We need to have a graph
        if self.InteractiveGraph == None:
            print("A graph is needed")
            return -1

        # We need to have a spanner (graph tc)
        if bitsets:
            print("bitsets")
            start = time.time()
            transitive_closure = self.G_s_t_bitsets_tentative()
            print(f"exec time = {time.time() - start}")
        else:
            start = time.time()
            transitive_closure = self.G_s_t()
            print(f"exec time = {time.time() - start}")
        
        for node_i in self.graph.nodes:
            for node_j in self.graph.nodes:
                if node_i != node_j and (node_i, node_j) not in transitive_closure:
                    print("No initial spanner")
                    print(f"{node_i}->{node_j}")
                    # Reset the colors
                    self.changeColor("reset_color_nodes", perso=None)
                    self.changeColor("reset_color_edges", perso=None)
                    return -1

        # copy of self.edges_labels
        edges_copy = copy.deepcopy(self.graph.edges)

        # For each edge, we try to remote it and test if the graph is tc
        edge_to_recup = []

        for edge in edges_copy:
            self.graph.remove_edge(edge[0], edge[1])
            tmp = True
            transitive_closure = self.G_s_t()
            for node_i in self.graph.nodes:
                for node_j in self.graph.nodes:
                    if node_i != node_j and (node_i, node_j) not in transitive_closure:
                        tmp = False
            # The edge is not primordiale
            if tmp == False:
                # We need to keep it to continue
                self.graph.add_edge(edge[0], edge[1])
            else:
                edge_to_recup.append((edge[0], edge[1]))
        
        spanner = copy.deepcopy(self.graph.edges)
        for edge in edge_to_recup:
            self.graph.add_edge(edge[0], edge[1])
        self.changeColor(action="perso_edges_nodes_temporal_path", perso=spanner)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = ChronoGraphUI() 
    screen.show()   
    sys.exit(app.exec_())