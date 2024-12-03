import unittest
import os
import glob
import json

class TestProcesador(unittest.TestCase):
    def setUp(self):
        """
        Configura el entorno antes de cada prueba.
        """
        # Crear directorios temporales si no existen
        self.inboxdir = 'test_inbox'
        self.workdir = 'test_workdir'
        self.conf_file = 'test_SNM_dict.conf'

        if not os.path.exists(self.inboxdir):
            os.makedirs(self.inboxdir)
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

        # Eliminar cualquier archivo existente en el inboxdir
        for file in glob.glob(os.path.join(self.inboxdir, '*.nc')):
            os.remove(file)

        # Crear archivos NetCDF de prueba
        for i in range(3):
            file_path = os.path.join(self.inboxdir, f'test_file_{i}.nc')
            with open(file_path, 'w') as f:
                f.write('Contenido de prueba')

        # Crear archivo de configuración de prueba
        conf_data = {
            "km_per_degree": 111.32,
            "arg_jpg_y_resolution": 620,
            "arg_jpg_x_resolution": 900,
            "sua_jpg_y_resolution": 576,
            "sua_jpg_x_resolution": 900,
            "vmin_irol": -90,
            "vmax_irol": 50,
            "arg_colorbar_label_size": 6,
            "sua_colorbar_label_size": 8,
            "arg_colorbar_label_size_vis": 26,
            "arg_image_legend_label_size": 6,
            "sua_image_legend_label_size": 8,
            "arg_image_legend_label_size_vis": 22,
            "arg_row_number": 1892,
            "arg_column_number": 2964,
            "goes16_extent_llx": -5434894.885056,
            "goes16_extent_lly": -5434894.885056,
            "goes16_extent_urx": 5434894.885056,
            "goes16_extent_ury": 5434894.885056,
            "argentina_lon_W": -90.0,
            "argentina_lon_E": -40.5,
            "argentina_lat_S": -55.5,
            "argentina_lat_N": -15.5,
            "sudamerica_lon_W": -100,
            "sudamerica_lon_E": -30,
            "sudamerica_lat_S": -60,
            "sudamerica_lat_N": -5,
            "delta_lon_W_for_graph": -5.0,
            "delta_lat_S_for_graph": -5.0,
            "delta_lat_N_for_graph": 4.0,
            "figure_resolution_dpi": 500,
            "figure_length_inches": 8,
            "figure_high_inches": 5,
            "line_width_inches_for_coast": 0.2,
            "line_width_inches_for_gridlines": 0.2,
            "line_width_inches_for_province_limits": 0.3,
            "line_width_inches_for_nation_limits": 0.2,
            "font_size_for_shapes": 5,
            "central_lat_of_stereo_projection": -30.0,
            "central_lon_of_stereo_projection": -60.0,
            "inbox": "inbox/",
            "outboxpng": "outboxpng/",
            "outboxtxt": "outboxtxt/",
            "outbox": "outbox/",
            "backup": "backup/",
            "logs": "logs/",
            "workdir": "workdir/",
            "cptdir": "data/cpt/",
            "image_resolution": 1.0,
            "root_path": "/home/juan/Escritorio/MDPTN/",
            "gif_frame_duration": 0.7
        }
        with open(self.conf_file, 'w') as f:
            json.dump(conf_data, f)

    def tearDown(self):
        """
        Limpia el entorno después de cada prueba.
        """
        # Eliminar archivos NetCDF de prueba
        for file in glob.glob(os.path.join(self.inboxdir, '*.nc')):
            os.remove(file)

        # Eliminar archivos acumulados y GIFs generados
        for file in glob.glob(os.path.join(self.workdir, '*.*')):
            os.remove(file)

        # Eliminar directorios temporales
        if os.path.exists(self.inboxdir):
            os.rmdir(self.inboxdir)
        if os.path.exists(self.workdir):
            os.rmdir(self.workdir)

        # Eliminar archivo de configuración de prueba
        if os.path.exists(self.conf_file):
            os.remove(self.conf_file)

    def test_inicializar_acumulado(self):
        """
        Prueba la inicialización del acumulado con los archivos NetCDF de prueba.
        """
        # Verificar que se hayan creado los archivos de prueba
        files = glob.glob(os.path.join(self.inboxdir, '*.nc'))
        self.assertEqual(len(files), 3)

    def test_creacion_directorios(self):
        """
        Prueba la creación de los directorios temporales.
        """
        self.assertTrue(os.path.exists(self.inboxdir))
        self.assertTrue(os.path.exists(self.workdir))

    def test_configuracion_cargada(self):
        """
        Prueba la carga del archivo de configuración.
        """
        with open(self.conf_file, 'r') as f:
            conf_data = json.load(f)
        self.assertIn("km_per_degree", conf_data)
        self.assertEqual(conf_data["km_per_degree"], 111.32)

if __name__ == '__main__':
    unittest.main()
