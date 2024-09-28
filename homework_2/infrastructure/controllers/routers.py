from homework_2.infrastructure.controllers.cart_controller import router as cart_router
from homework_2.infrastructure.controllers.item_controller import router as item_router

all_routers = [
    item_router,
    cart_router,
]
