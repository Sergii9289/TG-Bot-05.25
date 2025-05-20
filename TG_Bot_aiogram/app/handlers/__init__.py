from aiogram import Router
from .handlers import router as handlers_router
from .start import router as start_router
from .ask_gpt import router as gpt_router
from .random import router as random_router
from .talk import router as talk_router
from .quiz import router as quiz_router
from .translate import router as translate_router
from .recomendations import router as recomendations_router

router = Router()
router.include_router(handlers_router)
router.include_router(start_router)
router.include_router(gpt_router)
router.include_router(random_router)
router.include_router(quiz_router)
router.include_router(talk_router)
router.include_router(translate_router)
router.include_router(recomendations_router)