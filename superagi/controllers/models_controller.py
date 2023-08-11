from fastapi import APIRouter, Depends, HTTPException, Query
from superagi.helper.auth import check_auth, get_user_organisation
from superagi.helper.models_helper import ModelsHelper
from superagi.models.models_config import ModelsConfig
from superagi.models.models import Models
from fastapi_jwt_auth import AuthJWT
from fastapi_sqlalchemy import db
import logging
from pydantic import BaseModel
from main import get_config

router = APIRouter()

class ValidateAPIKeyRequest(BaseModel):
    model_provider: str
    model_api_key: str

class StoreModelRequest(BaseModel):
    model_name: str
    description: str
    end_point: str
    model_provider_id: int
    token_limit: int
    type: str
    version: str

@router.post("/storeApiKeys", status_code=200)
async def storeApiKeys(request: ValidateAPIKeyRequest, organisation=Depends(get_user_organisation)):
    try:
        return ModelsHelper(session=db.session, organisation_id=organisation.id).storeApiKey(request.model_provider, request.model_api_key)
    except Exception as e:
        logging.error(f"Error while storing API key: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/getApiKeys")
async def getApiKeys(organisation=Depends(get_user_organisation)):
    try:
        print(".........>>>>>>>>>>>>>>>................")
        print(get_config("MARKETPLACE_ORGANISATION_ID"))
        return ModelsHelper(session=db.session, organisation_id=organisation.id).fetchApiKeys()
    except Exception as e:
        logging.error(f"Error while retrieving API Keys: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/getApiKey", status_code=200)
async def getApiKey(model_provider: str = None, organisation=Depends(get_user_organisation)):
    try:
        return ModelsHelper(session=db.session, organisation_id=organisation.id).fetchApiKey(model_provider)
    except Exception as e:
        logging.error(f"Error while retrieving API Key: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/verifyEndPoint", status_code=200)
async def verifyEndPoint(model_api_key: str = None, end_point: str = None, model_provider: str = None, organisation=Depends(get_user_organisation)):
    try:
        return ModelsHelper(session=db.session, organisation_id=organisation.id).validateEndPoint(model_api_key, end_point, model_provider)
    except Exception as e:
        logging.error(f"Error validating Endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/storeModel", status_code=200)
async def storeModel(request: StoreModelRequest, organisation=Depends(get_user_organisation)):
    try:
        return ModelsHelper(session=db.session, organisation_id=organisation.id).storeModelDetails(request.model_name, request.description, request.end_point, request.model_provider_id, request.token_limit, request.type, request.version)
    except Exception as e:
        logging.error(f"Error storing the Model Details: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/fetchModels", status_code=200)
async def fetchModels(organisation=Depends(get_user_organisation)):
    try:
        return ModelsHelper(session=db.session, organisation_id=organisation.id).fetchModels()
    except Exception as e:
        logging.error(f"Error Fetching Models: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/fetchModel/{model_id}", status_code=200)
async def fetchModels(model_id: int, organisation=Depends(get_user_organisation)):
    try:
        return ModelsHelper(session=db.session, organisation_id=organisation.id).fetchModelDetails(model_id)
    except Exception as e:
        logging.error(f"Error Fetching Model Details: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/fetchModelData/{model}", status_code=200)
async def fetchModels(model: str, organisation=Depends(get_user_organisation)):
    try:
        return ModelsHelper(session=db.session, organisation_id=organisation.id).fetchData(model)
    except Exception as e:
        logging.error(f"Error Fetching Model Details: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get/list", status_code=200)
def get_knowledge_list(page: int = Query(None, title="Page Number"), organisation=Depends(get_user_organisation)):
    """
    Get Marketplace Model list.

    Args:
        page (int, optional): The page number for pagination. Defaults to None.

    Returns:
        dict: The response containing the marketplace list.

    """
    if page < 0:
        page = 0
    marketplace_models = Models.fetch_marketplace_list(page)
    marketplace_models_with_install = Models.get_model_install_details(db.session, marketplace_models, organisation)
    for knowledge in marketplace_models_with_install:
        knowledge["install_number"] = MarketPlaceStats.get_knowledge_installation_number(knowledge["id"])
    return marketplace_models_with_install

@router.get("/marketplace/list/{page}", status_code=200)
def get_marketplace_knowledge_list(page: int = 0):
    organisation_id = 2
    page_size = 30

    # Apply search filter if provided
    query = db.session.query(Models).filter(Models.org_id == organisation_id)
    print("qwwwwwwwwwwwwwwww")
    print(query)
    if page < 0:
        models = query.all()
    # Paginate the results
    models = query.offset(page * page_size).limit(page_size).all()

    return models