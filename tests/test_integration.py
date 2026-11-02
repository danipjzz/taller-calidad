import sqlite3
import pytest
from etl.pipeline import ejecutar_pipeline

@pytest.fixture
def conexion():
    conex = sqlite3.connect(":memory:")
    yield conex
    conex.close()

def test_pipeline_carga_clientes(conexion, tmp_path):
    #El CSV tiene " Ana@Mail.com" con espacio y mayúsculas, y esperamos ana@mail.com en la base de datos.
    csv = tmp_path / "clientes.csv"
    csv.write_text("id,email\n1, Ana@Mail.com\n2,luis@mail.com\n")

    ejecutar_pipeline(csv, conexion)

    filas = conexion.execute("SELECT email FROM clientes ORDER BY id").fetchall()
    assert filas == [("ana@mail.com",), ("luis@mail.com",)]

def test_pipeline_es_idempotente(conexion, tmp_path):
    #ejecutar dos veces deja 2 filas, no 4
    csv = tmp_path / "clientes.csv"
    csv.write_text("id,email\n1, Ana@Mail.com\n2,luis@mail.com\n")

    ejecutar_pipeline(csv, conexion)
    ejecutar_pipeline(csv, conexion)  

    total = conexion.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    assert total == 2 

def test_pipeline_email_invalido_lanza_error(conexion, tmp_path):
    #el pipeline falla con ValueError y no carga nada
    csv = tmp_path / "malo.csv"
    csv.write_text("id,email\n1,ana@mail.com\n2,sin-arroba\n")

    with pytest.raises(ValueError):
        ejecutar_pipeline(csv, conexion)

    total = conexion.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    assert total == 0

