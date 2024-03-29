from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo

class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr

    @field_validator('username', 'password1','password2','email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('필수 입력값 입니다.')
        return v

    @field_validator('password1')
    def check_password(cls, value):
        value = str(value)
        if len(value) < 8:
            raise ValueError("8글자 이상 입력하세요.")
        if not any(c.isupper() for c in value):
            raise ValueError("대문자 하나 이상 포함하세요.")
        if not any(c.islower() for c in value):
            raise ValueError("소문자 하나 이상 포함하세요.")
        if not any(c.isdigit() for c in value):
            raise ValueError("숫자 하나 이상 포함하세요.")
        return value

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
       
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str    

class User(BaseModel):
    id: int
    username: str
    email: str