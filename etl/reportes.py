import ast
import os

DB_PASSWORD = os.environ.get("DB_PASSWORD")


def buscar_cliente(con, email):
    return con.execute(
        "SELECT * FROM clientes WHERE email = ?", (email,)
    ).fetchall()


def evaluar_regla(expresion, fila):
    return ast.literal_eval(expresion)


def total(filas):
    try:
        return sum(f[1] for f in filas)
    except (TypeError, IndexError) as e:
        raise ValueError("filas inválidas") from e
