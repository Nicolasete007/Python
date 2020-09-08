import numpy as np
from tkinter import *

def readData(data):
	data = data.replace(",", ".")
	dataFinal = np.fromstring(data, dtype=float, sep='\n')
	return dataFinal

class Window:
	def __init__(self, window):

		self.showR2 = BooleanVar()
		self.showEquation = BooleanVar()
		self.addTrendLine = BooleanVar()

		self.dataXArray = None
		self.dataYArray = None
		self.dataXerrArray = None
		self.dataYerrArray = None


		self.window = window
		window.title("Gnuplot 4 dummies")
		window.option_add("*Font", ("Comic Sans MS", "10"))
		window.geometry("740x300")

		self.nameLabel = Label(window, text="Nom del gràfic")
		self.nameEntry = Entry(window, width=10)

		self.dataNameLabel = Label(window, text="Nom")
		self.dataLabel = Label(window, text="Dades")

		self.dataXLabel = Label(window, text="Valors de X")
		self.dataYLabel = Label(window, text="Valors de Y")
		self.dataXerrLabel = Label(window, text="Errors de X")
		self.dataYerrLabel = Label(window, text="Errors de Y")

		self.dataXName = Entry(window, width=10)
		self.dataYName = Entry(window, width=10)

		self.dataXEntry = Text(window, width=10, height=10)
		self.dataYEntry = Text(window, width=10, height=10)
		self.dataXerrEntry = Text(window, width=10, height=10)
		self.dataYerrEntry = Text(window, width=10, height=10)

		self.scrollX = Scrollbar(window)
		self.scrollX.config(command=self.dataXEntry.yview)
		self.scrollY = Scrollbar(window)
		self.scrollY.config(command=self.dataYEntry.yview)
		self.scrollXerr = Scrollbar(window)
		self.scrollXerr.config(command=self.dataXerrEntry.yview)
		self.scrollYerr = Scrollbar(window)
		self.scrollYerr.config(command=self.dataYerrEntry.yview)

		self.dataXEntry.config(yscrollcommand=self.scrollX.set)
		self.dataYEntry.config(yscrollcommand=self.scrollY.set)
		self.dataXerrEntry.config(yscrollcommand=self.scrollXerr.set)
		self.dataYerrEntry.config(yscrollcommand=self.scrollYerr.set)

		self.checkTrendLine = Checkbutton(window, text="Mostra línia de tendència", variable=self.addTrendLine)
		self.checkR2 = Checkbutton(window, text="Mostra R²", variable=self.showR2)
		self.checkEquation = Checkbutton(window, text="Mostra\nequació", variable=self.showEquation)
		self.eqCoordinatesX = Entry(window, width=8)
		self.eqCoordinatesY = Entry(window, width=8)
		self.R2CoordinatesX = Entry(window, width=8)
		self.R2CoordinatesY = Entry(window, width=8)
		self.dataEntryButton = Button(window, width=21, text="Crea arxiu de dades", command=self.createDataFile)
		self.createGnuplotFileButton = Button(window, width=21, text="Crea arxiu de Gnuplot", command=self.createGnuplotText)

		self.nameLabel.grid(column=0, row=0, padx=(10, 0), pady=10)
		self.nameEntry.grid(column=1, row=0, padx=(0, 10), pady=10)

		self.dataNameLabel.grid(column=2, row=1, sticky='e')
		self.dataLabel.grid(column=2, row=2, rowspan=5, sticky='e')

		self.dataXLabel.grid(column=3, row=0, padx=10, pady=(10, 0))
		self.dataYLabel.grid(column=5, row=0, padx=10, pady=(10, 0))
		self.dataXerrLabel.grid(column=7, row=1, padx=10, pady=(10, 0))
		self.dataYerrLabel.grid(column=9, row=1, padx=10, pady=(10, 0))

		self.dataXName.grid(column=3, row=1, padx=10)
		self.dataYName.grid(column=5, row=1, padx=10)

		self.dataXEntry.grid(column=3, row=2, padx=10, rowspan=5)
		self.dataYEntry.grid(column=5, row=2, padx=10, rowspan=5)
		self.dataXerrEntry.grid(column=7, row=2, padx=10, rowspan=5)
		self.dataYerrEntry.grid(column=9, row=2, padx=10, rowspan=5)

		self.scrollX.grid(column=4, row=2, rowspan=5, sticky='ns')
		self.scrollY.grid(column=6, row=2, rowspan=5, sticky='ns')
		self.scrollXerr.grid(column=8, row=2, rowspan=5, sticky='ns')
		self.scrollYerr.grid(column=10, row=2, rowspan=5, sticky='ns')

		self.checkTrendLine.grid(column=0, row=1, columnspan=2)
		self.checkR2.grid(column=0, row=2)
		self.checkEquation.grid(column=1, row=2)
		self.eqCoordinatesX.grid(column=1, row=3, padx=(0, 12), sticky="e")
		self.eqCoordinatesY.grid(column=1, row=4, padx=(0, 12), sticky="e")
		self.R2CoordinatesX.grid(column=0, row=3, padx=(12, 0), sticky="w")
		self.R2CoordinatesY.grid(column=0, row=4, padx=(12, 0), sticky="w")
		self.dataEntryButton.grid(column=0, row=5, columnspan=2)
		self.createGnuplotFileButton.grid(column=0, row=6, columnspan=2)

	def createDataFile(self):
		global graphName
		graphName = self.nameEntry.get()

		self.dataXArray = readData(self.dataXEntry.get("1.0", "end-1c"))
		self.dataYArray = readData(self.dataYEntry.get("1.0", "end-1c"))
		self.dataXerrArray = readData(self.dataXerrEntry.get("1.0", "end-1c"))
		self.dataYerrArray = readData(self.dataYerrEntry.get("1.0", "end-1c"))

		with open(str(graphName)+"_data.txt", "w+") as dataFile:
			for i in range(np.size(self.dataXArray)):

				try:
					x = str(self.dataXArray[i])
				except:
					x = ""
				try:
					y = ",\t" + str(self.dataYArray[i])
				except:
					y = ""
				try:
					xerr = ",\t" + str(self.dataXerrArray[i])
				except:
					xerr = ""
				try:
					yerr = ",\t" + str(self.dataYerrArray[i])
				except:
					yerr = ""

				if np.size(self.dataXerrArray) == 1:
					xerr = ",\t" + str(self.dataXerrArray[0])
				if np.size(self.dataYerrArray) == 1:
					yerr = ",\t" + str(self.dataYerrArray[0])

				dataFile.write(x + y + xerr + yerr + "\n")

	def createGnuplotText(self):

		global graphName
		graphName = self.nameEntry.get()

		list1 = []

		with open(str(graphName)+"_data.txt", "r") as data:
			for line in data:
				list1.append(line.split(","))

		global dataArray
		dataArray = np.array(list1, dtype=float)

		minXtic = np.amin(dataArray, axis=0)[0]
		minYtic = np.amin(dataArray, axis=0)[1]
		maxXtic = np.amax(dataArray, axis=0)[0]
		maxYtic = np.amax(dataArray, axis=0)[1]

		XAxisMin = minXtic - (maxXtic - minXtic)/5
		XAxisMax = maxXtic + (maxXtic - minXtic)/5
		YAxisMin = minYtic - (maxYtic - minYtic)/5
		YAxisMax = maxYtic + (maxYtic - minYtic)/5

		R2, mFunc, nFunc, merr, nerr = self.calculateParameters()

		with open(str(graphName)+"_plot.txt", "w+") as plotFile:

			plotFile.write("set xrange [%f:%f]\n"%(XAxisMin, XAxisMax))
			plotFile.write("set yrange [%f:%f]\n"%(YAxisMin, YAxisMax))
			plotFile.write("set mxtics 10\n")
			plotFile.write("set mytics 5\n")
			plotFile.write("set xlabel '%s'\n"%(self.dataXName.get()))
			plotFile.write("set ylabel '%s'\n"%(self.dataYName.get()))
			plotFile.write("set tics out\n")
			plotFile.write("set size ratio 0.65\n")
			plotFile.write("set nokey\n")
			plotFile.write("unset label\n")

			plotFile.write("m = %f\n"%(mFunc))
			plotFile.write("n = %f\n"%(nFunc))
			plotFile.write("f(x) = m*x + n\n")
			plotFile.write("fit f(x) '%s_data.txt' using 1:2 via m, n\n"%(graphName))

			plotFile.write("set terminal svg enhanced font 'Helvetica,14'\n")
			plotFile.write("set output '%s.svg'\n"%(graphName))

			if self.showEquation.get():
				try:
					xEq = float(self.eqCoordinatesX.get())
					yEq = float(self.eqCoordinatesY.get())

				except:
					xEq = minXtic
					yEq = maxYtic

				mFunc = self.truncateParameter(mFunc, merr)
				if float(nFunc) < 0:
					nFunc = self.truncateParameter(abs(nFunc), nerr)
					plotFile.write("set label ('y = %sx - %s') at %f, %f\n"%(mFunc, nFunc, xEq, yEq))
				else:
					nFunc = self.truncateParameter(nFunc, nerr)
					plotFile.write("set label ('y = %sx + %s') at %f, %f\n"%(mFunc, nFunc, xEq, yEq))

			if self.showR2.get():
				try:
					xR2 = float(self.R2CoordinatesX.get())
					yR2 = float(self.R2CoordinatesY.get())
				except:
					xR2 = minXtic
					yR2 = maxYtic - (YAxisMax - YAxisMin)/18

				plotFile.write("set label ('R² = %f') at %f, %f\n"%(R2, xR2, yR2))

			self.dataXerrArray = readData(self.dataXerrEntry.get("1.0", "end-1c"))
			self.dataYerrArray = readData(self.dataYerrEntry.get("1.0", "end-1c"))
			errWrite = ""
			if np.size(self.dataXerrArray) == 0 and np.size(self.dataYerrArray) == 0:
				errWrite = "using 1:2 with points lt rgb 'blue' pt 7 ps 0.5"
			elif np.size(self.dataXerrArray) == 0 and np.size(self.dataYerrArray) != 0:
				errWrite = "using 1:2:3 with yerrorbars lt rgb 'blue' pt 7 ps 0.5"
			elif np.size(self.dataXerrArray) != 0 and np.size(self.dataYerrArray) == 0:
				errWrite = "using 1:2:3 with xerrorbars lt rgb 'blue' pt 7 ps 0.5"
			else:
				errWrite = "using 1:2:3:4 with xyerrorbars lt rgb 'blue' pt 7 ps 0.5"

			plotFile.write("\nplot '%s_data.txt' "%(graphName) + errWrite + " title sprintf(''),\\\n")

			if self.addTrendLine.get():
				plotFile.write("\tf(x) title sprintf('')")

	def calculateParameters(self):
		mFunc = np.polyfit(dataArray[:,0], dataArray[:,1], 1)[0]
		nFunc = np.polyfit(dataArray[:,0], dataArray[:,1], 1)[1]
		R2 = (np.corrcoef(dataArray[:,0], dataArray[:,1])[0,1])**2
		n = np.size(dataArray[:,0])
		delta = n*np.sum(dataArray[:,0]**2) - (np.sum(dataArray[:,0]))**2

		yerr = 0
		for i in range(n):
			yerr += (dataArray[i,1] - mFunc*dataArray[i,0] - nFunc)**2
		yerr *= 1/(n-2)
		yerr = np.sqrt(yerr)
		
		merr = np.sqrt(n/delta)*yerr
		nerr = np.sqrt(np.sum(dataArray[:,0]**2) / delta)*yerr

		return(R2, mFunc, nFunc, merr, nerr)

	def truncateParameter(self, func, err):
		roundV = 0
		if err < 1:
			for i in str(err):
				if i == ".":
					roundV = 0
				elif i == "0":
					roundV += 1
				else:
					if i == "1":
						roundV += 2
					else:
						roundV += 1
					break
		return str(round(func, roundV))

	def createWindow(self):
		t = Toplevel()
		t.wm_title("Window #")

if __name__ == "__main__":
	root = Tk()
	window = Window(root)
	root.mainloop()