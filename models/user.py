from database import (
    save_user,
    get_user,
    add_xp,
    increment_stat,
    get_stats,
    is_banned,
    get_all_users,
    set_ban,
)
from typing import Optional


async def ensure_user(user_id: int, first_name: str) -> None:
    save_user(user_id, first_name)


async def reward_user(user_id: int, action: str, xp_amount: int) -> Optional[int]:
    new_level = add_xp(user_id, xp_amount)
    increment_stat(user_id, action)
    return new_level


async def get_user_stats(user_id: int) -> dict:
    return get_stats(user_id)


async def check_banned(user_id: int) -> bool:
    return is_banned(user_id)


async def get_user_info(user_id: int) -> Optional[tuple]:
    return get_user(user_id)
