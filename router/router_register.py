# backend/tancho/registers/routes.py

from bson.objectid import ObjectId
from config.config import DB, CONF
from fastapi import APIRouter, Depends, HTTPException, Security
from typing import List
from datetime import datetime
import logging
import random
import string

from model.model_register import RegisterInBase, RegisterInDB

router_register = APIRouter()


def validate_object_id(id_: str):
    try:
        _id = ObjectId(id_)
    except Exception:
        if CONF["fastapi"].get("debug", False):
            logging.warning("Invalid Object ID")
        raise HTTPException(status_code=400)
    return _id


async def _get_register_or_404(id_: str):
    _id = validate_object_id(id_)
    register = await DB.tbl_register.find_one({"_id": _id})
    if register:
        return fix_register_id(register)
    else:
        raise HTTPException(status_code=404, detail="register not found")


def fix_register_id(register):
    register["id_"] = str(register["_id"])
    return register


def randomString(stringLength=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# =================================================================================


@router_register.post("/register", response_model=RegisterInDB)
async def add_register(register: RegisterInBase):
    register_op = await DB.tbl_register.insert_one(register.dict())
    if register_op.inserted_id:
        register = await _get_register_or_404(register_op.inserted_id)
        register["id_"] = str(register["_id"])
        return register


@router_register.get("/register", response_model=List[RegisterInDB])
async def get_all_registers(size: int = 100, page: int = 0):
    filter_query = {}
    skip = page * size
    registers_cursor = DB.tbl_register.find(filter_query).skip(skip).limit(size)
    registers = await registers_cursor.to_list(length=size)
    return list(map(fix_register_id, registers))


@router_register.get("/register/{id_}", response_model=RegisterInDB)
async def get_register_by_id(id_: ObjectId = Depends(validate_object_id)):
    register = await DB.tbl_register.find_one({"_id": id_})
    if register:
        register["id_"] = str(register["_id"])
        return register
    else:
        raise HTTPException(status_code=404, detail="register not found")


@router_register.delete("/register/{id_}", dependencies=[Depends(_get_register_or_404)], response_model=dict)
async def delete_register_by_id(id_: str):
    register_op = await DB.tbl_register.delete_one({"_id": ObjectId(id_)})
    if register_op.deleted_count:
        return {"status": f"deleted count: {register_op.deleted_count}"}


@router_register.put("/register/{id_}", response_model=RegisterInDB)
async def update_register(id_: str, register: RegisterInBase):
    register.updateTime = datetime.utcnow()
    register_op = await DB.tbl_register.update_one(
        {"_id": ObjectId(id_)}, 
        {"$set": register.dict(skip_defaults=True)}
    )
    if register_op.modified_count:
        return await _get_register_or_404(id_)
    else:
        raise HTTPException(status_code=304)