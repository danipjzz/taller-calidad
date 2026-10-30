import pytest
from etl.transform import normalizar_email, calcular_total

@pytest.mark.parametrize("entrada, esperado", [
    (" Ana@Mail.COM ", "ana@mail.com"),
    ("luis.p+datos@uni.edu.co", "luis.p+datos@uni.edu.co"),
])
def test_normalizar_email_valido(entrada, esperado):
    assert normalizar_email(entrada) == esperado


@pytest.mark.parametrize("entrada", ["", " ", "sin-arroba", None])
def test_normalizar_email_invalido(entrada):
    with pytest.raises(ValueError):
        normalizar_email(entrada)