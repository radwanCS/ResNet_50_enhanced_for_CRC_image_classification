import sys
import tensorflow as tf
from PyQt5.QtWidgets import QApplication,  QMainWindow,QFileDialog,QTableWidgetItem,QListWidget,QMessageBox,QPushButton,QWidget
import img_rc
from PyQt5 import QtCore, QtGui, QtWidgets
from  PyQt5.QtCore import Qt,QThread,pyqtSignal,QEvent
from  PyQt5.QtGui import QColor,QPixmap
import os
import shutil
from model import *
from PIL import Image

import cgitb
cgitb.enable()

#模型确认阈值
score_threshold = 60



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1491, 845)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/软件图标.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgba(255, 228, 193, 199);")
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_add_dir = QtWidgets.QPushButton(self.frame)
        self.pushButton_add_dir.setStyleSheet("QPushButton{\n"
"        background-color: rgb(170, 250, 255);\n"
"        color: green;   \n"
"        border-radius: 5px;  \n"
"        border: 2px groove gray;\n"
"        border-style: outset;\n"
"}\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/打开文件夹.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_add_dir.setIcon(icon1)
        self.pushButton_add_dir.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_add_dir.setObjectName("pushButton_add_dir")
        self.gridLayout.addWidget(self.pushButton_add_dir, 0, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label_all_img_num = QtWidgets.QLabel(self.frame)
        self.label_all_img_num.setText("")
        self.label_all_img_num.setObjectName("label_all_img_num")
        self.horizontalLayout.addWidget(self.label_all_img_num)
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        self.label_processed_img_num = QtWidgets.QLabel(self.frame)
        self.label_processed_img_num.setText("")
        self.label_processed_img_num.setObjectName("label_processed_img_num")
        self.horizontalLayout.addWidget(self.label_processed_img_num)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.label_check_img_num = QtWidgets.QLabel(self.frame)
        self.label_check_img_num.setText("")
        self.label_check_img_num.setObjectName("label_check_img_num")
        self.horizontalLayout.addWidget(self.label_check_img_num)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setMouseTracking(True)
        self.tableWidget.setStyleSheet("background-color: rgba(255, 253, 171, 64);")
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideNone)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.horizontalLayout_2.addWidget(self.tableWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 3)
        self.pushButton_add_file = QtWidgets.QPushButton(self.frame)
        self.pushButton_add_file.setStyleSheet("QPushButton{\n"
"        background-color: rgb(170, 170, 255);\n"
"        color: yellow;   \n"
"        border-radius: 5px;  \n"
"        border: 2px groove gray;\n"
"        border-style: outset;\n"
"}\n"
"")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/打开图片.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_add_file.setIcon(icon2)
        self.pushButton_add_file.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_add_file.setObjectName("pushButton_add_file")
        self.gridLayout.addWidget(self.pushButton_add_file, 0, 0, 1, 1)
        self.pushButton_run = QtWidgets.QPushButton(self.frame)
        self.pushButton_run.setStyleSheet("QPushButton{\n"
"        background-color: rgb(200, 230, 205);\n"
"        color: blue;    \n"
"        border-radius: 5px;  \n"
"        border: 2px ;\n"
"        border-style: outset;\n"
"}\n"
"")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/执行.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_run.setIcon(icon3)
        self.pushButton_run.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_run.setObjectName("pushButton_run")
        self.gridLayout.addWidget(self.pushButton_run, 0, 3, 1, 1)
        self.label_classify_status = QtWidgets.QLabel(self.frame)
        self.label_classify_status.setStyleSheet("font: 75 12pt \"Arial\";\n"
"color: rgb(205, 185, 64);")
        self.label_classify_status.setText("")
        self.label_classify_status.setObjectName("label_classify_status")
        self.gridLayout.addWidget(self.label_classify_status, 0, 4, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setStyleSheet("font: 75 12pt \"Arial\";\n"
"color: rgb(70, 70, 255);")
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.label_check_rate = QtWidgets.QLabel(self.frame)
        self.label_check_rate.setStyleSheet("font: 75 14pt \"Arial\";")
        self.label_check_rate.setAlignment(QtCore.Qt.AlignCenter)
        self.label_check_rate.setObjectName("label_check_rate")
        self.horizontalLayout_3.addWidget(self.label_check_rate)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.pushButton_check = QtWidgets.QPushButton(self.frame)
        self.pushButton_check.setStyleSheet("font: 75 9pt \"Arial\";\n"
"background-color: rgba(170, 255, 255, 155);")
        self.pushButton_check.setObjectName("pushButton_check")
        self.horizontalLayout_3.addWidget(self.pushButton_check)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_img = QtWidgets.QLabel(self.frame)
        self.label_img.setStyleSheet("background-color: rgba(230, 230, 230, 150);")
        self.label_img.setText("")
        self.label_img.setScaledContents(True)
        self.label_img.setObjectName("label_img")
        self.verticalLayout.addWidget(self.label_img)
        self.verticalLayout.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout, 1, 3, 1, 3)
        self.pushButton_clear = QtWidgets.QPushButton(self.frame)
        self.pushButton_clear.setStyleSheet("QPushButton{\n"
"        background-color: rgb(230, 170, 255);\n"
"        color: red;    \n"
"        border-radius: 5px;  \n"
"        border: 2px ;\n"
"        border-style: outset;\n"
"}\n"
"")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/清空.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_clear.setIcon(icon4)
        self.pushButton_clear.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.gridLayout.addWidget(self.pushButton_clear, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1491, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "图像分类"))
        self.pushButton_add_dir.setText(_translate("MainWindow", "添加目录"))
        self.label_2.setText(_translate("MainWindow", "图片总数:"))
        self.label_8.setText(_translate("MainWindow", "分类完成数:"))
        self.label_6.setText(_translate("MainWindow", "需人工确认数:"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "图片名"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "处理状态"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "识别类型"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "判定类别"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "模型分类结果"))
        self.pushButton_add_file.setText(_translate("MainWindow", "添加图片"))
        self.pushButton_run.setText(_translate("MainWindow", "执行分类"))
        self.label.setText(_translate("MainWindow", "需要人工判定剩余数:"))
        self.label_check_rate.setText(_translate("MainWindow", "0"))
        self.pushButton_check.setText(_translate("MainWindow", "手动判定"))
        self.pushButton_clear.setText(_translate("MainWindow", "清空图像"))

def _dir_image_list(path, allfile):
    """
    列出指定目录下的全部图片文件
    :param path:
    :param allfile:
    :return:
    """
    filelist = os.listdir(path)
    for filename in filelist:
        if filename.endswith(".jpeg") or  filename.endswith(".png") or  filename.endswith(".jpg") or filename.endswith(".tif"):
            filepath = os.path.join(path, filename)
            if os.path.isdir(filepath):
                _dir_image_list(filepath, allfile)
            else:
                allfile.append(filepath)
    return allfile

def dir_image_list(root_dir):
    """列出指定目录下的全部图片文件"""
    allfile = []
    _dir_image_list(root_dir,allfile)
    return allfile

class ImageInfo(object):
    def __init__(self,process_type = "",img_processed = False,final_target="未知", img_result = None):
        self.process_type = process_type
        self.img_processed = img_processed
        self.final_target = final_target
        self.img_result = img_result

class ClassifyThread(QThread):
    """执行识别时的自定义线程，识别线程应和主线程分开，不然界面会卡"""
    trigger = pyqtSignal(dict)
    finish_trigger =pyqtSignal()
    def __init__(self,all_img_info,output_root_dir):
        super(ClassifyThread, self).__init__()
        self.output_root_dir =output_root_dir
        self.all_img_info = all_img_info
        print("加载模型...")
        config = tf.ConfigProto(
            device_count={'GPU': 1},
            intra_op_parallelism_threads=1,
            allow_soft_placement=True
        )

        config.gpu_options.allow_growth = True
        config.gpu_options.per_process_gpu_memory_fraction = 0.6

        self.session = tf.Session(config=config)
        tf.keras.backend.set_session(self.session)
        self.Model = TrainCNNModel()
        self.Model.build()
        self.Model.reload_model()
        self.Model.model.summary()
        
        # 先用模型随意执行一次图片的预测，否则，后面Qt类中线程开始识别时，使用该模型会因为不在同一个线程中会报错
        img = Image.new('RGB', (224, 224))
        with self.session.as_default():
            with self.session.graph.as_default():
                data = self.Model.orc_img(img)
        print("模型加载完毕！")

    def run_model(self,img_path):
        """调用模型识别"""
        img = Image.open(img_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img = img.resize((224, 224))
        with self.session.as_default():
            with self.session.graph.as_default():
                result = self.Model.orc_img(img)
        return result

    def copy_file_to_target(self,img_path,target):
        """拷贝图片到指定target分类目录下"""
        shutil.copy(img_path, os.path.join(self.output_root_dir, target,
                                           os.path.basename(img_path)))

    def run(self):
        for img_path, img_info in self.all_img_info.items():
            if img_info.img_result is None:  # 识别没有处理的图片
                result = self.run_model(img_path)
                if float(result["predict"]) >= score_threshold:
                    # 模型自动处理，整个图像已被处理完成
                    self.all_img_info[img_path].img_processed = True
                    self.all_img_info[img_path].process_type = "模型"
                    # 自动确认类别
                    self.all_img_info[img_path].final_target = result["target"]
                    self.copy_file_to_target(img_path, result["target"])
                else:
                    # 需要等待手动处理完成
                    self.all_img_info[img_path].img_processed = False
                    self.all_img_info[img_path].process_type = "手动"
                self.all_img_info[img_path].img_result = result
                self.trigger.emit(self.all_img_info)
        self.finish_trigger.emit()

class mwindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(mwindow, self).__init__()
        self.setupUi(self)
        self.tableWidget.cellClicked.connect(self.tableWidget_click)
        self.tableWidget.cellEntered.connect(self.tabel_mouse_tracking)
        self.pushButton_add_file.clicked.connect(self.add_file)
        self.pushButton_add_dir.clicked.connect(self.add_dir)
        self.pushButton_clear.clicked.connect(self.clear_img)
        self.pushButton_run.clicked.connect(self.classify)
        self.pushButton_check.clicked.connect(self.check_img)



        self.all_img_info = {}
        self.should_check_img_paths = [] #需要手动确定的图片路径名
        self.current_check_img_index = 0
        self.output_root_dir = "output"
        self.target_name = ["ADI", "BACK", "DEB", "LYM", "MUC", "MUS", "NORM", "STR", "TUM"]

        for i in (self.target_name):
            dir_path = os.path.join(self.output_root_dir,i)
            if not os.path.exists(dir_path) :
                os.makedirs(dir_path)

        self.check_choose_qListWidget = QListWidget()
        self.check_choose_qListWidget.setWindowTitle("选择类别")
        for i in (self.target_name):
            self.check_choose_qListWidget.resize(300, 220) #设置大小和标题
            self.check_choose_qListWidget.addItem(i)
        self.check_choose_qListWidget.itemClicked.connect(self.check_clicked)
        self.check_choose_qListWidget.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.classify_thread = ClassifyThread(self.all_img_info, self.output_root_dir)
        self.classify_thread.trigger.connect(self.running_classify)
        self.classify_thread.finish_trigger.connect(self.finish_classify)

    def keyPressEvent(self, event):
        """监听鼠标事件"""
        # 兼容大键盘和小键盘回车键获取问题
        if event.key() == Qt.Key_Enter or event.key()==Qt.Key_Return :
            self.check_img()

    def copy_file_to_target(self,img_path,target):
        shutil.copy(img_path, os.path.join(self.output_root_dir, target,
                                           os.path.basename(img_path)))

    def tabel_mouse_tracking(self,row, col):
        """tableWidget鼠标点击监听监听"""
        if col==0 or col==2:#鼠标在第一列/第三列
            item = self.tableWidget.item(row, col)
            if item is  not None:
                image_path = self.tableWidget.item(row, col).text()
                #提示完整内容
                self.tableWidget.setToolTip(image_path)

    def show_img(self,image_path):
        """显示图片"""
        self.label_img.setPixmap(
            QPixmap(image_path).scaled(self.label_img.width(),
                                       self.label_img.height()))

    def tableWidget_click(self,row, col):
        """点击列表莫一行触发显示对应图片"""
        image_path = self.tableWidget.item(row,0).text()
        self.show_img(image_path)

    def get_table_item(self,s):
        Item = QTableWidgetItem()
        Item.setData(Qt.DisplayRole, s)
        return Item

    def append_table(self,img_paths):
        for index, image_path in enumerate(img_paths):
            self.tableWidget.insertRow(0)
            Item = self.get_table_item(image_path)
            self.tableWidget.setItem(0, 0, Item)
            Item = self.get_table_item("未处理")
            self.tableWidget.setItem(0, 1, Item)
            self.tableWidget.item(0, 1).setForeground(QColor(255, 0, 0))
            self.tableWidget.item(0, 1).setTextAlignment(
                Qt.AlignCenter)

    def update_table(self):
        #更新表格内容，ui控制核心，主要依据self.all_img_info内容
        self.label_all_img_num.setText(str(len(self.all_img_info)))
        processed_img_num = 0
        check_img_num = 0
        should_check_img_paths = []
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)
        for image_path,image_info in self.all_img_info.items():
            self.tableWidget.insertRow(0)
            #设置第2列
            Item = self.get_table_item(image_path)
            self.tableWidget.setItem(0, 0, Item)
            if image_info.img_processed:
                processed_img_num+=1
                Item = self.get_table_item("已处理")
                self.tableWidget.setItem(0, 1, Item)
                self.tableWidget.item(0, 1).setForeground(QColor(0, 255, 0))
            else:
                Item = self.get_table_item("未处理")
                self.tableWidget.setItem(0, 1, Item)
                self.tableWidget.item(0, 1).setForeground(QColor(255, 0, 0))
                if image_info.process_type=="手动":
                    check_img_num+=1
                    should_check_img_paths.append(image_path)

            # 设置第3列
            Item = self.get_table_item(image_info.process_type)
            self.tableWidget.setItem(0, 2, Item)
            if image_info.process_type=="模型":
                self.tableWidget.item(0, 2).setForeground(QColor(0, 205, 205))
            elif image_info.process_type=="手动":
                self.tableWidget.item(0, 2).setForeground(QColor(205, 205, 0))

            # 设置第4列
            Item = self.get_table_item(image_info.final_target)
            self.tableWidget.setItem(0, 3, Item)
            if image_info.final_target =="未知":
                self.tableWidget.item(0, 3).setForeground(QColor(255, 0, 0))
            else:
                self.tableWidget.item(0, 3).setForeground(QColor(0, 255, 0))

            # 设置第5列
            if image_info.img_result is not None:
                Item = self.get_table_item("{}:{}%,{}:{}%".format(image_info.img_result["target"],
                                                                  image_info.img_result["predict"],
                                                                  image_info.img_result["target2"],
                                                                  image_info.img_result["predict2"],
                                                                  ))
            else:
                Item = self.get_table_item("")
            self.tableWidget.setItem(0, 4, Item)

            for i in range(0,self.tableWidget.columnCount()):
                self.tableWidget.item(0, i).setTextAlignment(
                    Qt.AlignCenter)

            self.label_processed_img_num.setText(str(processed_img_num))
            self.label_check_img_num.setText(str(check_img_num))
        self.should_check_img_paths = should_check_img_paths
        self.update_check_status()

    def clear_img(self):
        if len(self.should_check_img_paths)!=0:
            rep = QMessageBox.warning(self, '提示', "还有{}张需要人工确定的图片\n确认执行清空？".format(len(self.should_check_img_paths)),
                                QMessageBox.Yes,QMessageBox.No)
            if rep == QMessageBox.No:
                return
        self.all_img_info = {}
        self.should_check_img_paths = []  # 需要手动确定的图片路径名
        self.current_check_img_index = 0
        self.update_table()

    def check_img(self):
        if len(self.should_check_img_paths):
            img_path = self.should_check_img_paths[self.current_check_img_index]
            self.show_img(img_path)
            self.check_choose_qListWidget.show()
        else:
            QMessageBox.warning(self, '提示', "暂无需要手动判定图!",
                                         QMessageBox.Yes)

    def check_clicked(self,item): #人工确认选择
        choose_target = item.text()
        choos_img_path = self.should_check_img_paths[0]
        self.copy_file_to_target(choos_img_path,choose_target)
        self.all_img_info[choos_img_path].final_target = choose_target
        self.all_img_info[choos_img_path].img_processed = True
        self.should_check_img_paths.remove(choos_img_path)
        self.update_table()
        self.check_choose_qListWidget.hide()
        if len(self.should_check_img_paths)==0:
            self.label_img.clear()

    def update_check_status(self):
        """更新手工检查的状态信息"""
        if len(self.should_check_img_paths):
            self.label_check_rate.setText(str(len(self.should_check_img_paths)))
            img_path = self.should_check_img_paths[self.current_check_img_index]
            self.show_img(img_path)
        else:
            self.label_check_rate.setText("0")



    def append_new_images(self,img_paths):
        for i in img_paths:
            if i not  in self.all_img_info:
                self.all_img_info[i] = ImageInfo()

    def add_file(self):
        """添加图片，可以一次选多张图"""
        filenames,_ = QFileDialog.getOpenFileNames(self, "OpenFile", ".",
                                                      "Image Files(*.jpg *.jpeg *.png *.tif)")

        if len(filenames):
            self.append_new_images(filenames)
            self.update_table()

    def add_dir(self):
        """目录选择功能"""
        directory = QFileDialog.getExistingDirectory(self,
                                                     "选取文件夹", "./")

        if len(directory):
            all_images = dir_image_list(directory)
            self.append_new_images(all_images)
        self.update_table()

    def running_classify(self,all_img_info):
        self.all_img_info = all_img_info
        self.update_table()

    def finish_classify(self):
        # 执行分类后取消执行按钮和清除按钮禁用
        self.pushButton_run.setDisabled(False)
        self.pushButton_clear.setDisabled(False)
        # 更新表格内容
        self.update_table()
        self.label_classify_status.setText("模型分类完成!")

    def classify(self):
        # 执行分类时设置执行按钮和清除按钮禁用
        #防止多次点击，有线程安全问题
        self.pushButton_run.setDisabled(True)
        self.pushButton_clear.setDisabled(True)
        self.label_classify_status.setText("正在执行模型分类任务中...")

        self.classify_thread.start()

    def closeEvent(self, *args, **kwargs):
        re = QMessageBox.warning(self, '提示', "确认退出吗!",
                            QMessageBox.Yes,QMessageBox.No)
        if re == QMessageBox.Yes:
            exit()

if __name__ == '__main__':
    #显示qt界面的固定操作

    app = QApplication(sys.argv)
    w = mwindow()
    w.show()
sys.exit(app.exec_())