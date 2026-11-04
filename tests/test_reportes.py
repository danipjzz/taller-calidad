import sqlite3
import pytest
from etl.reportes import buscar_cliente, evaluar_regla, total


@pytest.fixture
def conexion():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE clientes (id INTEGER PRIMARY KEY, email TEXT)")
    con.executemany(
        "INSERT INTO clientes VALUES (?, ?)",
        [(1, "ana@mail.com"), (2, "luis@mail.com")],
    )
    yield con
    con.close()


def test_buscar_cliente_existente(conexion):
    assert buscar_cliente(conexion, "ana@mail.com") == [(1, "ana@mail.com")]


def test_buscar_cliente_inexistente(conexion):
    assert buscar_cliente(conexion, "nadie@mail.com") == []


def test_buscar_cliente_resiste_inyeccion(conexion):
    assert buscar_cliente(conexion, "' OR '1'='1") == []


def test_evaluar_regla_literal():
    assert evaluar_regla("5", None) == 5


def test_evaluar_regla_rechaza_codigo():
    with pytest.raises(ValueError):
        evaluar_regla("__import__('os').getcwd()", None)


def test_total_suma_segunda_columna():
    assert total([(1, 10), (2, 20)]) == 30


def test_total_lista_vacia():
    assert total([]) == 0


@pytest.mark.parametrize("filas", [[(1, "x")], [(1,)]])
def test_total_filas_invalidas(filas):
    with pytest.raises(ValueError):
        total(filas)