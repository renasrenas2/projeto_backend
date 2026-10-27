import sqlite3

def conectar_banco():
    conexao = sqlite3.connect("biblioteca.db")
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

