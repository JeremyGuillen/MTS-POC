from app.api.molds import MoldsAPI
from app.api.users import UsersAPI
from app.common.routers.main_router import MainRouter

base_router = MainRouter()

base_router.register_route(path="/molds", cls=MoldsAPI)
base_router.register_route(path="/users", cls=UsersAPI)