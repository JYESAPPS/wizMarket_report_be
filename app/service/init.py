from app.crud.init import (
    get_or_create_store_uuid as crud_get_or_create_store_uuid,
    get_uuid_store as crud_get_uuid_store,
)

def get_or_create_store_uuid (store_id): 
    uuid = crud_get_or_create_store_uuid(store_id)
    return uuid

def get_uuid_store (uuid): 
    store_id = crud_get_uuid_store(uuid)
    return store_id