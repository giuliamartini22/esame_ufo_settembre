import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handle_graph(self, e):
        latitude = float(self._view.txt_latitude.value)
        longitude = float(self._view.txt_longitude.value)
        maxLat, minLat = self._model.populateLimitiLat()
        maxLon, minLon = self._model.populateLimitiLong()

        try:
            sogliaIns = float(maxLat)
        except ValueError:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Il numero inserito non è valido"))
            self._view.update_page()
            return

        if latitude < minLat or latitude > maxLat:
            self._view.create_alert("Valore di latitudine non valida!")
            return
        if longitude < minLon or longitude > maxLon:
            self._view.create_alert("Valore di longitudine non valida!")
            return

        shape = self._view.ddshape.value
        self._model.buildGraph(latitude, longitude, shape)
        #self._model.buildGraph(41, -100, "sphere")
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self._view.txt_result1.controls.append(
            ft.Text(f"I 5 nodi di grado magggiore sono:"))
        listaBest1 = self._model.archiGradiMaggiori()
        for arco in listaBest1:
            self._view.txt_result1.controls.append(ft.Text(f"{arco[0]} ->  degree = {arco[1]}"))

        self._view.txt_result1.controls.append(
            ft.Text(f"I 5 archi di peso magggiore sono:"))
        listaBest = self._model.archiPesiMaggiori()
        for arco in listaBest:
            self._view.txt_result1.controls.append(ft.Text(f"{arco[0]} -> {arco[1]} | weight = {arco[2]}"))
        self._view.update_page()


    def handle_path(self, e):
        pass

    def fill_ddshape(self):
        self._listShape = self._model.getShape()
        for shape in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()

    def read_shape(self, e):
        if e.control.value is None:
            self._shape = None
        else:
            self._shape = e.control.value
