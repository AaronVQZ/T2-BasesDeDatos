import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Carga datos desde XML usando SPs sin cursores'

    def handle(self, *args, **kwargs):
        tree = ET.parse('datos_mejorados.xml')
        root = tree.getroot()

        self.cargar_puestos(root)
        self.cargar_tipos_movimiento(root)
        self.cargar_tipos_evento(root)
        self.cargar_usuarios(root)
        self.cargar_empleados(root)
        self.cargar_movimientos(root)
        self.cargar_errores(root)
        

    def ejecutar_sp(self, query, params, descripcion_ok=None):
        connection.ensure_connection()
        conn = connection.connection
        try:
            conn.execute(query, params)
            if descripcion_ok:
                self.stdout.write(self.style.SUCCESS(descripcion_ok))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error ejecutando SP: {query} | {params}'))
            self.stdout.write(self.style.ERROR(f'→ {str(e)}'))

    def cargar_puestos(self, root):
        for puesto in root.find('Puestos').findall('Puesto'):
            self.ejecutar_sp(
                "EXEC dbo.sp_InsertarPuesto @Id=?, @Nombre=?, @SalarioxHora=?",
                (puesto.attrib['Id'], puesto.attrib['Nombre'], puesto.attrib['SalarioxHora']),
                f"Puesto insertado: ID={puesto.attrib['Id']}, Nombre={puesto.attrib['Nombre']}"
            )

    def cargar_tipos_movimiento(self, root):
        for tm in root.find('TiposMovimientos').findall('TipoMovimiento'):
            self.ejecutar_sp(
                "EXEC dbo.sp_InsertarTipoMovimiento @Id=?, @Nombre=?, @TipoAccion=?",
                (tm.attrib['Id'], tm.attrib['Nombre'], tm.attrib['TipoAccion']),
                f"TipoMovimiento insertado: ID={tm.attrib['Id']}, Nombre={tm.attrib['Nombre']}"
            )

    def cargar_tipos_evento(self, root):
        for te in root.find('TiposEvento').findall('TipoEvento'):
            self.ejecutar_sp(
                "EXEC dbo.sp_InsertarTipoEvento @Id=?, @Nombre=?",
                (te.attrib['Id'], te.attrib['Nombre']),
                f"TipoEvento insertado: ID={te.attrib['Id']}, Nombre={te.attrib['Nombre']}"
            )

    def cargar_usuarios(self, root):
        for user in root.find('Usuarios').findall('usuario'):
            self.ejecutar_sp(
                "EXEC dbo.sp_InsertarUsuario @Id=?, @Username=?, @Password=?",
                (user.attrib['Id'], user.attrib['Nombre'], user.attrib['Pass']),
                f"Usuario insertado: ID={user.attrib['Id']}, Username={user.attrib['Nombre']}"
            )

    def cargar_empleados(self, root):
        for empleado in root.find('Empleados').findall('empleado'):
            self.ejecutar_sp(
                "EXEC dbo.sp_InsertarEmpleado @IdPuesto=?, @ValorDocumentoIdentidad=?, @Nombre=?, @FechaContratacion=?, @SaldoVacaciones=?, @EsActivo=?",
                (
                    empleado.attrib['IdPuesto'],
                    empleado.attrib['ValorDocumentoIdentidad'],
                    empleado.attrib['Nombre'],
                    empleado.attrib['FechaContratacion'],
                    empleado.attrib['SaldoVacaciones'],
                    empleado.attrib['EsActivo']
                ),
                f"Empleado insertado: {empleado.attrib['Nombre']} ({empleado.attrib['ValorDocumentoIdentidad']})"
            )

    def cargar_movimientos(self, root):
        for movimiento in root.find('Movimientos').findall('movimiento'):
            self.ejecutar_sp(
                "EXEC dbo.sp_InsertarMovimiento @ValorDocId=?, @IdTipoMovimiento=?, @Fecha=?, @Monto=?, @PostByUser=?, @PostInIP=?, @PostTime=?",
                (
                    movimiento.attrib['ValorDocId'],
                    movimiento.attrib['IdTipoMovimiento'],
                    movimiento.attrib['Fecha'],
                    movimiento.attrib['Monto'],
                    movimiento.attrib['PostByUser'],
                    movimiento.attrib['PostInIP'],
                    movimiento.attrib['PostTime']
                ),
                f"Movimiento insertado: Doc={movimiento.attrib['ValorDocId']}, Fecha={movimiento.attrib['Fecha']}"
            )

    def cargar_errores(self, root):
        for err in root.find('Error').findall('error'):
            self.ejecutar_sp(
                "EXEC dbo.sp_InsertarError @Codigo=?, @Descripcion=?",
                (
                    err.attrib['Codigo'],
                    err.attrib['Descripcion']
                ),
                f"✅ Error insertado: Código={err.attrib['Codigo']} - {err.attrib['Descripcion']}"
            )

    
    
    
