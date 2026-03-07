from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Calculator App")

class SimpleOperation(BaseModel):
    a: float
    b: float

class ExpressionInput(BaseModel):
    expression: str


@app.post("/add")
async def add(item: SimpleOperation):
    """Сложение двух чисел"""
    return {"result": item.a + item.b}

@app.post("/sub")
async def subtract(item: SimpleOperation):
    """Вычитание второго числа из первого"""
    return {"result": item.a - item.b}

@app.post("/mul")
async def multiply(item: SimpleOperation):
    """Умножение двух чисел"""
    return {"result": item.a * item.b}

@app.post("/div")
async def divide(item: SimpleOperation):
    """Деление первого числа на второе"""
    if item.b == 0:
        raise HTTPException(status_code=400, detail="Деление на ноль запрещено")
    return {"result": item.a / item.b}


@app.post("/calculate")
async def calculate_expression(item: ExpressionInput):
    """
    Вычисляет результат математического выражения из строки.
    Поддерживает скобки и приоритет операций.
    """
    expr = item.expression
    
    allowed_chars = set("0123456789.+-*/() ")
    if not set(expr).issubset(allowed_chars):
        raise HTTPException(status_code=400, detail="Выражение содержит недопустимые символы")

    try:
        result = eval(expr)
        return {"result": result}
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Деление на ноль в выражении")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка вычисления: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Калькулятор готов к работе. Перейдите на /docs для проверки."}