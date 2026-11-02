# tests/test_transform.py
import pytest
from etl.transform import normalizar_email, calcular_total


# ---------- normalizar_email ----------

@pytest.mark.parametrize("entrada, esperado", [
    (" Ana@Mail.COM ", "ana@mail.com"),                        # espacios y mayúsculas
    ("luis.p+datos@uni.edu.co", "luis.p+datos@uni.edu.co"),    # caracteres válidos
    ("USUARIO@Dominio.org", "usuario@dominio.org"),
])
def test_normalizar_email_valido(entrada, esperado):
    assert normalizar_email(entrada) == esperado


@pytest.mark.parametrize("entrada", ["", " ", "sin-arroba", "a@b", None, 123])
def test_normalizar_email_invalido(entrada):
    with pytest.raises(ValueError):
        normalizar_email(entrada)


# ---------- calcular_total ----------

@pytest.mark.parametrize("precio, cantidad, descuento, esperado", [
    (10, 2, 0.0, 20.0),     # sin descuento
    (100, 1, 0.1, 90.0),    # descuento normal
    (100, 1, 1, 0.0),       # límite: descuento 100%
    (50, 0, 0.0, 0.0),      # límite: cantidad 0
    (0, 5, 0.0, 0.0),       # precio 0
])
def test_calcular_total_valido(precio, cantidad, descuento, esperado):
    assert calcular_total(precio, cantidad, descuento) == esperado


def test_calcular_total_redondeo():
    # 19.99 * 3 * 0.85 = 50.9745 -> se redondea a 2 decimales
    assert calcular_total(19.99, 3, 0.15) == 50.97


def test_calcular_total_descuento_por_defecto_es_cero():
    assert calcular_total(10, 3) == 30.0


def test_calcular_total_precio_negativo():
    with pytest.raises(ValueError):
        calcular_total(-1, 2)


def test_calcular_total_cantidad_negativa():
    with pytest.raises(ValueError):
        calcular_total(10, -2)


@pytest.mark.parametrize("descuento", [1.5, -0.1, 2])
def test_calcular_total_descuento_fuera_de_rango(descuento):
    with pytest.raises(ValueError, match="fuera de rango"):
        calcular_total(100, 1, descuento)