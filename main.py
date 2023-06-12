import numpy as np
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic

A = np.array([[1,1,3],[0,1,3],[-1,3,0]])
b = np.array([[1],[3],[5]])

class DespreWindow(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("Despre.ui", self)
        self.setWindowTitle("Despre")

class MyGUI(QMainWindow):
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("proiectGUI.ui", self)
        
        self.setWindowTitle("Calculator matrice")
        self.UiComponents()
        
        self.show()
        self.actionDespre.triggered.connect(self.arataDespre)
    def arataDespre(self):
        self.d = DespreWindow()
        self.d.show()
    def UiComponents(self):
        self.btnAutentificare.clicked.connect(self.login)
        self.actionInchide.triggered.connect(exit)
        self.actionLog_Out.triggered.connect(self.logout)
        self.rbtManual.clicked.connect(self.check)
        self.rbtFisier.clicked.connect(self.check)
        self.rbtAutomat.clicked.connect(self.check)
        self.btnAlegeFisier.clicked.connect(self.alegeFisier)
        self.btnIntroducere.clicked.connect(self.introducereMatrice)
        self.btnCalculeaza.clicked.connect(self.calculeazaMatrice)
     
    def login(self):
        if self.txtUtilizator.text() == "1" and self.txtParola.text() == "1":
            self.lblIntrebare.setEnabled(True)   
            self.rbtManual.setEnabled(True)
            self.rbtFisier.setEnabled(True)
            self.rbtAutomat.setEnabled(True)
            self.btnIntroducere.setEnabled(True)
            self.txtLinii.setEnabled(True)
            self.txtColoane.setEnabled(True)
            self.lblDimensiune.setEnabled(True)
            self.lblIntrebare_3.setEnabled(True)
            self.lblIntrebare_4.setEnabled(True)
        else:
            message = QMessageBox()
            message.setText("Credentiale invalide.")      
            message.exec_()
            
    def logout(self):
            self.txtUtilizator.setText("")
            self.txtParola.setText("")
            self.lblIntrebare.setEnabled(False)   
            self.rbtManual.setEnabled(False)
            self.rbtFisier.setEnabled(False)
            self.rbtAutomat.setEnabled(False)
            self.btnIntroducere.setEnabled(False)
            self.txtLinii.setEnabled(False)
            self.txtColoane.setEnabled(False)
            self.txtManualA.setEnabled(False)
            self.txtManualB.setEnabled(False)
            self.lblDimensiune.setEnabled(False)
            self.lblIntrebare_3.setEnabled(False)
            self.lblIntrebare_4.setEnabled(False)
            self.btnCalculeaza.setEnabled(False)
            self.btnAlegeFisier.setEnabled(False)
            self.txtMatriceExtinsa.setText("")
            self.txtMatriceExtinsa_2.setText("")
            self.txtRezultat.setText("")
            self.txtLinii.setText("") 
            self.txtColoane.setText("") 
            self.txtManualA.setText("")
            self.txtManualB.setText("") 
            self.txtFisier.setText("")     
                  
    def alegeFisier(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        self.txtFisier.setText(fname[0])
            
    def check(self):
        if(self.rbtManual.isChecked()):
            self.txtManualA.setEnabled(True)
            self.txtManualB.setEnabled(True)
        else:
            self.txtManualA.setEnabled(False)
            self.txtManualB.setEnabled(False)
        if(self.rbtFisier.isChecked()):
            self.btnAlegeFisier.setEnabled(True)
        else:
            self.btnAlegeFisier.setEnabled(False)
    
    def introducereMatrice(self):
        linii = self.txtLinii.text()
        coloane = self.txtColoane.text()
        if(linii == "" and  coloane == "" or linii != coloane):
            message = QMessageBox()
            message.setText("Numarul de linii si/sau coloane este invalid.")      
            message.exec_()
            return
        l = int(float(linii))
        c = int(float(coloane))
        A = []
        b = []
        if(self.rbtManual.isChecked()):
            matriceA = self.txtManualA.text()
            matriceB = self.txtManualB.text()
            elemeteleMatA = list(map(int, matriceA.split(" "))) 
            A = np.array(elemeteleMatA).reshape(l, c)
            elemeteleMatB = list(map(int, matriceB.split(" ")))
            b = np.array(elemeteleMatB).reshape(l, c - l + 1)
        elif(self.rbtAutomat.isChecked()):
            A = np.random.randint(1, 20,(l, c))
            b = np.random.randint(1, 20,(l, c - l + 1))
        elif(self.rbtFisier.isChecked()):
            caleFisier = self.txtFisier.text()
            with open(caleFisier) as cf:
                fisier = cf.readlines()
                elemeteleMatA = list(map(int, fisier[0].split(" ")))
                A = np.array(elemeteleMatA).reshape(l, c)
                elemeteleMatB = list(map(int, fisier[1].split(" ")))
                b = np.array(elemeteleMatB).reshape(l, c - l + 1)
            cf.close()
        self.txtMatriceExtinsa.setText(str(A))
        self.txtMatriceExtinsa_2.setText(str(b))
        self.btnCalculeaza.setEnabled(True)
        return A, b
    
    def calculeazaMatrice(self):
        A, b = self.introducereMatrice() 
        rezultatArr = []
        qm = QMessageBox()
        ret = qm.question(self,'', "Vrei sa folosesc pivotarea?", qm.Yes | qm.No)
        if A.shape[0] != A.shape[1]:
            return
        if b.shape[1] > 1 or b.shape[0] != A.shape[0]:
            return  
        n = len(b)
        m = n-1
        i = 0
        j = i-1
        x = np.zeros(n)
        
        matrice_extinsa = np.concatenate((A, b), axis = 1, dtype= float)
        
        while i<n:
            if ret == qm.Yes:
                for p in range(i+1, n):
                    if abs(matrice_extinsa[i,i]) < abs(matrice_extinsa[p,i]):
                        matrice_extinsa[[p, i]] = matrice_extinsa[[i, p]]
            if matrice_extinsa[i][i] == 0.0:
                return
            for j in range(i+1, n):
                coeficient_scalare = matrice_extinsa[j][i] / matrice_extinsa[i][i]
                matrice_extinsa[j] = matrice_extinsa[j] - (coeficient_scalare * matrice_extinsa[i])
            i = i + 1
        
        x[m] = matrice_extinsa[m][n] / matrice_extinsa[m][m]
        
        for k in range (n-2, -1, -1):
            x[k] = matrice_extinsa[k][n]
            for j in range(k + 1, n):
                x[k] = x[k] - matrice_extinsa[k][j] * x[j]
            x[k] = x[k] / matrice_extinsa[k][k]
    
        for rezultat in range(n):
            rezultatArr.append(str(f"x{rezultat} este {x[rezultat]}"))
        self.txtRezultat.setText(str(rezultatArr))
        

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

main()

"""
def eliminare_gauss(A, b):
    if A.shape[0] != A.shape[1]:
        return
    if b.shape[1] > 1 or b.shape[0] != A.shape[0]:
        return
    
    n = len(b)
    m = n-1
    i = 0
    j = i-1
    x = np.zeros(n)
    
    matrice_extinsa = np.concatenate((A, b), axis = 1, dtype= float)
    print(matrice_extinsa)
    
    while i<n:
        if matrice_extinsa[i][i] == 0.0:
            return
        for j in range(i+1, n):
            coeficient_scalare = matrice_extinsa[j][i] / matrice_extinsa[i][i]
            matrice_extinsa[j] = matrice_extinsa[j] - (coeficient_scalare * matrice_extinsa[i])
            print(matrice_extinsa)
        i = i + 1
        
    x[m] = matrice_extinsa[m][n] / matrice_extinsa[m][m]
    
    for k in range (n-2, -1, -1):
        x[k] = matrice_extinsa[k][n]
        for j in range(k + 1, n):
            x[k] = x[k] - matrice_extinsa[k][j] * x[j]
        x[k] = x[k] / matrice_extinsa[k][k]
    
    for rezultat in range(n):
        print(f"x{rezultat} is {x[rezultat]}")   
                     
    
eliminare_gauss(A, b)

def eliminare_gaussPP(A, b):
    if A.shape[0] != A.shape[1]:
        return
    if b.shape[1] > 1 or b.shape[0] != A.shape[0]:
        return
    n = len(b)
    m = n-1
    i = 0
    x = np.zeros(n)
    
    matrice_extinsa = np.concatenate((A, b), axis = 1, dtype= float)
    print(matrice_extinsa)
    
    while i<n:
        for p in range(i+1, n):
            if abs(matrice_extinsa[i,i]) < abs(matrice_extinsa[p,i]):
                matrice_extinsa[[p, i]] = matrice_extinsa[[i, p]]
        
        if matrice_extinsa[i][i] == 0.0:
            return
        for j in range(i+1, n):
            coeficient_scalare = matrice_extinsa[j][i] / matrice_extinsa[i][i]
            matrice_extinsa[j] = matrice_extinsa[j] - (coeficient_scalare * matrice_extinsa[i])
            print(matrice_extinsa)
        i = i + 1
        
    x[m] = matrice_extinsa[m][n] / matrice_extinsa[m][m]
    
    for k in range (n-2, -1, -1):
        x[k] = matrice_extinsa[k][n]
        for j in range(k + 1, n):
            x[k] = x[k] - matrice_extinsa[k][j] * x[j]
        x[k] = x[k] / matrice_extinsa[k][k]
    
    for rezultat in range(n):
        print(f"x{rezultat} is {x[rezultat]}")      
eliminare_gaussPP(A, b)        
"""