import re
from datetime import datetime
from typing import Any, Dict, List, Union
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, ValidationError


class UserRegistration(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8)
    password_confirm: str = Field(exclude=True) 
    age: int = Field(ge=18, le=120) 
    registration_date: datetime = Field(default_factory=datetime.now) 
    
    full_name: str = Field(min_length=2)
    phone: str


    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValueError('Имя пользователя должно содержать только латинские буквы, цифры и символ подчёркивания.')
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not any(char.isdigit() for char in value):
            raise ValueError('Пароль должен содержать хотя бы одну цифру.')
        if not any(char.isupper() for char in value):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву.')
        if not any(char.islower() for char in value):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву.')
        return value

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserRegistration':
        if self.password != self.password_confirm:
            raise ValueError('Пароли не совпадают.')
        return self

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        if not value[0].isupper():
            raise ValueError('Реальное имя должно начинаться с заглавной буквы.')
        return value

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not re.match(r'^\+\d-\d{3}-\d{2}-\d{2}$', value):
            raise ValueError('Номер телефона должен быть в формате +X-XXX-XX-XX.')
        return value


def register_user(data: dict) -> Union[UserRegistration, List[str]]:
    try:
        user = UserRegistration(**data)
        return user
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            field_name = error['loc'][0] if error['loc'] else 'Модель'
            msg = error['msg'].replace('Value error, ', '')
            error_messages.append(f"Ошибка в поле '{field_name}': {msg}")
        return error_messages


from typing import Optional

# --- ЗАДАНИЕ 3 ---

class RecursiveNode(BaseModel):
    data: str
    child: Optional['RecursiveNode'] = None 

def create_recursive_json(depth: int) -> RecursiveNode:
    """
    Функция создает объект с произвольной вложенностью (depth - глубина).
    Возвращает Pydantic модель, которую можно легко сериализовать в JSON.
    """
    if depth <= 0:
        raise ValueError("Глубина должна быть больше 0")
    
    current_node = RecursiveNode(data="any_data")
    for _ in range(depth - 1):
        parent_node = RecursiveNode(data="any_data", child=current_node)
        current_node = parent_node
        
    return current_node

if __name__ == "__main__":
    print("=== ТЕСТ: Успешная регистрация ===")
    valid_data = {
        "username": "Ivan_2023",
        "email": "ivan@example.com",
        "password": "Password123",
        "password_confirm": "Password123",
        "age": 25,
        "full_name": "Иван Иванов",
        "phone": "+7-999-12-34"
    }
    
    result = register_user(valid_data)
    if isinstance(result, UserRegistration):
        print("Успех! Сериализованный вывод (password_confirm скрыт):")
        print(result.model_dump_json(indent=2)) 
    else:
        print(result)


    print("\n=== ТЕСТ: Ошибки валидации ===")
    invalid_data = {
        "username": "Иван!", # Русские буквы и знак восклицания (ошибка)
        "email": "not-an-email", # Неверный email
        "password": "password", # Нет цифр и заглавных букв
        "password_confirm": "password123", # Не совпадает
        "age": 15, # Меньше 18
        "full_name": "иван", # С маленькой буквы
        "phone": "89991234567" # Неверный формат
    }
    
    errors = register_user(invalid_data)
    for err in errors:
        print(err)


    print("\n=== ТЕСТ ЗАДАНИЯ 3 (Рекурсия) ===")
    recursive_model = create_recursive_json(3)
    print(recursive_model.model_dump_json(indent=2))
