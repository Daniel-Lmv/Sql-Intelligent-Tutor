from backend.database.conceitos_repository import listar_conceitos

conceitos = listar_conceitos()

for conceito in conceitos:
    print(dict(conceito))