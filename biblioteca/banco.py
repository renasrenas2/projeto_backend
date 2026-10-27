import sqlite3

conexao = sqlite3.connect("biblioteca.db")
conexao.execute("PRAGMA foreign_keys = ON")

try:
    cursor = conexao.cursor()
        
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL, 
        nacionalidade TEXT NOT NULL
    )
    """)
        
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        ano TEXT NOT NULL,
        autorid INTEGER NOT NULL,
        FOREIGN KEY (autorid) 
        REFERENCES autores(id)
    )
    """)

    autores = [
        ("Machado de Assis", "Brasileira"),
        ("", ""),
        ("", ""),
    ]

    conexao.commit()

except Exception as erro:
    conexao.rollback()

finally:
    conexao.close()