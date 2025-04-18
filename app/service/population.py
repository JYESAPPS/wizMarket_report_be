import logging
from dotenv import load_dotenv
from fastapi import HTTPException


from app.crud.population import (
    select_population_by_store_business_number as crud_select_population_by_store_business_number,
)
from app.schemas.report import (
    LocalStorePopulationDataOutPut,
)

logger = logging.getLogger(__name__)


def select_population_by_store_business_number(
    store_business_id: str,
) -> LocalStorePopulationDataOutPut:
    # logger.info(f"Fetching store info for business ID: {store_business_id}")

    try:
        return crud_select_population_by_store_business_number(store_business_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Service LocalStorePopulationDataOutPut Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Service LocalStorePopulationDataOutPut Error: {str(e)}",
        )
