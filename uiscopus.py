# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scopus.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from extout import get_auth_id
from getfullinfo import get_info
from filter import filter_authors
from Email import get_email
from save_csv import savecsv
import time
import threading

class Communicate(QtCore.QObject):
    myGUI_signal = QtCore.pyqtSignal(str)



def myThread(callbackFunc):
# Setup the signal-slot mechanism.
    mySrc = Communicate()
    mySrc.myGUI_signal.connect(callbackFunc) 

    # Endless loop. You typically want the thread
    # to run forever.
    # Do something useful here.
    while True:
        if ui.Signal==1:
            mySrc.myGUI_signal.emit('Looking for all Author ids')
            mySrc.myGUI_signal.emit('this might take up to 30-40 seconds')
            mySrc.myGUI_signal.emit('Please Wait ...')
            t1 = time.time()
            ui.new_get_auth()
            t2 = time.time()
            mySrc.myGUI_signal.emit(f'extracted {len (ui.extractor.authors.keys())} Author ids in {int(t2 - t1)} seconds')
            ui.Signal = 2

        elif ui.Signal==2:
            mySrc.myGUI_signal.emit('trying to get some informations about theese authors...')
            mySrc.myGUI_signal.emit('this might take up to 1-2 minutes')
            mySrc.myGUI_signal.emit('please wait ...')
            t1 = time.time()
            ui.new_get_info()
            t2 = time.time()
            mySrc.myGUI_signal.emit(f'got {len (ui.info_class.authors.keys())} Author information in {int(t2- t1)} seconds')
            ui.Signal=3
            print('finished')
            #mySrc.myGUI_signal.emit(str(ui.info_class.authors))
            pass
        
        elif ui.Signal==3:
            mySrc.myGUI_signal.emit('trying to filter authors according to your inputs \n this shoud not take too long')
            mySrc.myGUI_signal.emit('please Wait ...')
            t1 = time.time()
            ui.filter_auth()
            t2 = time.time()
            time.sleep(0.3)
            mySrc.myGUI_signal.emit(f'{len(ui.filterd_class.authors.keys())} authors left \n proccess took {int(t2-t1)} seconds')
            ui.Signal = 4
            pass

        elif ui.Signal == 4:
            mySrc.myGUI_signal.emit('trying to find remaining authors email')
            mySrc.myGUI_signal.emit('please Wait ...')
            t1 = time.time()
            ui.find_email()
            t2 = time.time()
            time.sleep(0.3)
            mySrc.myGUI_signal.emit(f'{len(ui.email_class.authors.keys())} authors email found \n proccess took {int(t2-t1)} seconds')
            #mySrc.myGUI_signal.emit(str(ui.email_class.authors))
            ui.Signal =5

        elif ui.Signal == 5:
            #time.sleep(0.3)
            mySrc.myGUI_signal.emit('fetching data done.\ntrying to save outputs')
            ui.save_output()
            mySrc.myGUI_signal.emit('finish')
            mySrc.myGUI_signal.emit('**************')
            ui.Signal =6
            print('finish')

        else:
            #print('passed')
            pass




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1119, 1121)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scopusaccessgroup = QtWidgets.QGroupBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scopusaccessgroup.sizePolicy().hasHeightForWidth())
        self.scopusaccessgroup.setSizePolicy(sizePolicy)
        self.scopusaccessgroup.setObjectName("scopusaccessgroup")
        self.formLayout_2 = QtWidgets.QFormLayout(self.scopusaccessgroup)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.scopusaccessgroup)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.IntenetConu = QtWidgets.QRadioButton(self.scopusaccessgroup)
        self.IntenetConu.setChecked(True)
        self.IntenetConu.setObjectName("IntenetConu")
        self.horizontalLayout_2.addWidget(self.IntenetConu)
        self.userpassu = QtWidgets.QRadioButton(self.scopusaccessgroup)
        self.userpassu.setObjectName("userpassu")
        self.horizontalLayout_2.addWidget(self.userpassu)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_2 = QtWidgets.QLabel(self.scopusaccessgroup)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.scopusaccessgroup)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.passwordu = QtWidgets.QLineEdit(self.scopusaccessgroup)
        #self.passwordu = gui.QgsPasswordLineEdit(self.scopusaccessgroup)
        self.passwordu.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passwordu.sizePolicy().hasHeightForWidth())
        self.passwordu.setSizePolicy(sizePolicy)
        self.passwordu.setEchoMode(QtWidgets.QLineEdit.Password)
        #self.passwordu.setShowLockIcon(False)
        self.passwordu.setObjectName("passwordu")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.passwordu)
        self.usernameu = QtWidgets.QLineEdit(self.scopusaccessgroup)
        self.usernameu.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usernameu.sizePolicy().hasHeightForWidth())
        self.usernameu.setSizePolicy(sizePolicy)
        self.usernameu.setTabletTracking(True)
        self.usernameu.setInputMask("")
        self.usernameu.setText("")
        self.usernameu.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.usernameu.setPlaceholderText("")
        self.usernameu.setClearButtonEnabled(False)
        self.usernameu.setObjectName("usernameu")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.usernameu)
        self.verticalLayout.addWidget(self.scopusaccessgroup)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName("groupBox_4")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox_4)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.searchenteryu = QtWidgets.QLineEdit(self.groupBox_4)
        self.searchenteryu.setObjectName("searchenteryu")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.searchenteryu)
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setObjectName("label_5")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setObjectName("label_6")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.fromyearu = QtWidgets.QSpinBox(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fromyearu.sizePolicy().hasHeightForWidth())
        self.fromyearu.setSizePolicy(sizePolicy)
        self.fromyearu.setMinimum(1999)
        self.fromyearu.setMaximum(2021)
        self.fromyearu.setProperty("value", 2017)
        self.fromyearu.setObjectName("fromyearu")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.fromyearu)
        self.toyearu = QtWidgets.QSpinBox(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toyearu.sizePolicy().hasHeightForWidth())
        self.toyearu.setSizePolicy(sizePolicy)
        self.toyearu.setMinimum(1999)
        self.toyearu.setMaximum(2021)
        self.toyearu.setProperty("value", 2018)
        self.toyearu.setObjectName("toyearu")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.toyearu)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setObjectName("groupBox_5")
        self.formLayout_4 = QtWidgets.QFormLayout(self.groupBox_5)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_7 = QtWidgets.QLabel(self.groupBox_5)
        self.label_7.setObjectName("label_7")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.minhindexu = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minhindexu.sizePolicy().hasHeightForWidth())
        self.minhindexu.setSizePolicy(sizePolicy)
        self.minhindexu.setObjectName("minhindexu")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.minhindexu)
        self.label_8 = QtWidgets.QLabel(self.groupBox_5)
        self.label_8.setObjectName("label_8")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.paperfromu = QtWidgets.QSpinBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.paperfromu.sizePolicy().hasHeightForWidth())
        self.paperfromu.setSizePolicy(sizePolicy)
        self.paperfromu.setMinimum(1999)
        self.paperfromu.setMaximum(2021)
        self.paperfromu.setProperty("value", 2004)
        self.paperfromu.setObjectName("paperfromu")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.paperfromu)
        self.label_9 = QtWidgets.QLabel(self.groupBox_5)
        self.label_9.setObjectName("label_9")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.papertou = QtWidgets.QSpinBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.papertou.sizePolicy().hasHeightForWidth())
        self.papertou.setSizePolicy(sizePolicy)
        self.papertou.setMinimum(1999)
        self.papertou.setMaximum(2021)
        self.papertou.setProperty("value", 2020)
        self.papertou.setObjectName("papertou")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.papertou)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout_5 = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setObjectName("label_10")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.firstnameu = QtWidgets.QCheckBox(self.groupBox_3)
        self.firstnameu.setChecked(True)
        self.firstnameu.setObjectName("firstnameu")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.firstnameu)
        self.lastnameu = QtWidgets.QCheckBox(self.groupBox_3)
        self.lastnameu.setChecked(True)
        self.lastnameu.setObjectName("lastnameu")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lastnameu)
        self.emailu = QtWidgets.QCheckBox(self.groupBox_3)
        self.emailu.setChecked(True)
        self.emailu.setTristate(True)
        self.emailu.setObjectName("emailu")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.emailu)
        self.affiliationu = QtWidgets.QCheckBox(self.groupBox_3)
        self.affiliationu.setChecked(True)
        self.affiliationu.setTristate(False)
        self.affiliationu.setObjectName("affiliationu")
        self.formLayout_5.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.affiliationu)
        self.countryu = QtWidgets.QCheckBox(self.groupBox_3)
        self.countryu.setChecked(True)
        self.countryu.setObjectName("countryu")
        self.formLayout_5.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.countryu)
        self.Documentu = QtWidgets.QCheckBox(self.groupBox_3)
        self.Documentu.setChecked(True)
        self.Documentu.setObjectName("Documentu")
        self.formLayout_5.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.Documentu)
        self.citationu = QtWidgets.QCheckBox(self.groupBox_3)
        self.citationu.setChecked(True)
        self.citationu.setObjectName("citationu")
        self.formLayout_5.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.citationu)
        self.hindexu = QtWidgets.QCheckBox(self.groupBox_3)
        self.hindexu.setChecked(True)
        self.hindexu.setObjectName("hindexu")
        self.formLayout_5.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.hindexu)
        self.authidu = QtWidgets.QCheckBox(self.groupBox_3)
        self.authidu.setObjectName("authidu")
        self.formLayout_5.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.authidu)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Logsu = QtWidgets.QTextEdit(self.groupBox_2)
        self.Logsu.setObjectName("Logsu")
        self.verticalLayout_3.addWidget(self.Logsu)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.startu = QtWidgets.QPushButton(self.centralwidget)
        self.startu.setTabletTracking(True)
        self.startu.setObjectName("startu")
        self.verticalLayout_2.addWidget(self.startu)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1119, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.userpassu.toggled.connect(self.showuserpass)
        #self.startu.clicked.connect(self.run)
        self.startu.clicked.connect(self.startTheThread)
        self.Signal = 1


    

    def theCallbackFunc(self, msg):
        self.Logsu.append(msg)

    def startTheThread(self):
        # Create the new thread. The target function is 'myThread'. The
        # function we created in the beginning.
        self.Signal =1
        t = threading.Thread(name = 'myThread', target = myThread, args = ([self.theCallbackFunc]))
        t.start()

    def new_get_auth(self):
        query = self.searchenteryu.text()
        stime = self.fromyearu.value()
        ftime = self.toyearu.value()
        self.extractor = get_auth_id(query,stime,ftime)
        self.extractor.get_all_pages_result()
    
    def new_get_info(self):
        self.info_class = get_info(self.extractor.authors)

    def filter_auth(self):
        minH = int(self.minhindexu.text())
        stime = str(self.paperfromu.value())
        ftime = str(self.papertou.value())
        self.filterd_class = filter_authors(self.info_class.authors,minH,stime,ftime)
        pass

    def find_email(self):
        self.email_class = get_email(self.filterd_class.authors)
        pass

    def save_output(self):
        fname = self.firstnameu.isChecked()
        lname = self.lastnameu.isChecked()
        email = self.emailu.isChecked()
        aff = self.affiliationu.isChecked()
        country = self.countryu.isChecked()
        doc = self.Documentu.isChecked()
        cit = self.citationu.isChecked()
        hind = self.hindexu.isChecked()
        id = self.authidu.isChecked()
        output_name = self.lineEdit.text()
        savecsv(self.email_class.authors,fname,lname,email,aff,country,doc,cit,hind,id,output_name)
        pass

    def showuserpass(self):
        if self.userpassu.isChecked():
            self.usernameu.setEnabled(True)
            self.passwordu.setEnabled(True)
        else:
            self.usernameu.setEnabled(False)
            self.passwordu.setEnabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "inputs"))
        self.scopusaccessgroup.setTitle(_translate("MainWindow", "Scopus Access"))
        self.label.setText(_translate("MainWindow", "Type of your Scopus Access:"))
        self.IntenetConu.setText(_translate("MainWindow", "Internet Connection"))
        self.userpassu.setText(_translate("MainWindow", "User, Pass"))
        self.label_2.setText(_translate("MainWindow", "Scopus Username:"))
        self.label_3.setText(_translate("MainWindow", "Scopus Password:"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Search Entery"))
        self.label_4.setText(_translate("MainWindow", "Search entery: "))
        self.searchenteryu.setText(_translate("MainWindow", "Nature Reviews Molecular Cell Biology"))
        self.label_5.setText(_translate("MainWindow", "From year:"))
        self.label_6.setText(_translate("MainWindow", "To year:"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Author filter"))
        self.label_7.setText(_translate("MainWindow", "Minimum h-index:"))
        self.minhindexu.setText(_translate("MainWindow", "10"))
        self.label_8.setText(_translate("MainWindow", "First paper year:"))
        self.label_9.setText(_translate("MainWindow", "Last paper year:"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Output Settings"))
        self.label_10.setText(_translate("MainWindow", "file name:"))
        self.lineEdit.setText(_translate("MainWindow", "ScopusOut.csv"))
        self.firstnameu.setText(_translate("MainWindow", "First Name"))
        self.lastnameu.setText(_translate("MainWindow", "Last Name"))
        self.emailu.setText(_translate("MainWindow", "Email"))
        self.affiliationu.setText(_translate("MainWindow", "Affiliation"))
        self.countryu.setText(_translate("MainWindow", "Country"))
        self.Documentu.setText(_translate("MainWindow", "Documents"))
        self.citationu.setText(_translate("MainWindow", "Citation"))
        self.hindexu.setText(_translate("MainWindow", "h-Index"))
        self.authidu.setText(_translate("MainWindow", "Auth id"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Logs"))
        self.startu.setText(_translate("MainWindow", "Start!"))

#from qgis import gui


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
