from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers.batch_controller import get_batches, get_batch_names_sorted_by_date, insert_batch, update_batch, delete_batch
from app.models import Batch  # Assuming your models are defined in `models.py`
from app.database.db import get_db  # Assuming `get_db` is defined in `database.py`

router = APIRouter()

# Route to get batches with pagination and search
@router.get("/batches")
def get_batch_list(search_query: str = "", page: int = 1, page_size: int = 100, db: Session = Depends(get_db)):
    skip = (page - 1) * page_size
    batches = get_batches(db=db, search_query=search_query, skip=skip, limit=page_size)
    return {"data": batches, "totalRows": len(batches)}

# Route to get batch names sorted by date
@router.get("/batchnames")
def get_batch_names(db: Session = Depends(get_db)):
    batch_names = get_batch_names_sorted_by_date(db)
    return {"batchNames": [batch.batchname for batch in batch_names]}

# Route to insert a new batch
@router.post("/batches/insert")
def create_batch(batch: dict, db: Session = Depends(get_db)):
    new_batch = insert_batch(db=db, batch=batch)
    return {"id": new_batch.batchid, "batchname": new_batch.batchname}

# Route to update an existing batch
@router.put("/batches/update/{batch_id}")
def update_existing_batch(batch_id: int, batch: dict, db: Session = Depends(get_db)):
    updated_batch = update_batch(db=db, batch_id=batch_id, updated_batch=batch)
    return {"batchid": updated_batch.batchid, "batchname": updated_batch.batchname}

# Route to delete a batch
@router.delete("/batches/delete/{batch_id}")
def delete_existing_batch(batch_id: int, db: Session = Depends(get_db)):
    delete_batch(db=db, batch_id=batch_id)
    return {"message": "Batch deleted successfully"}
