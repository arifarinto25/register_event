from pydantic import BaseModel
from datetime import datetime, date

class RegisterInBase(BaseModel):
    createTime : datetime = None
    updateTime : datetime = None
    nama : str = None
    nohp : str = None
    email : str = None
    namaSekolah : str = None
    alamatSekolah : str = None
    ip : str = None

class RegisterInDB(RegisterInBase):
    id_ : str = None