import pickle
from typing import Any, Dict, Optional

from redis.asyncio import Redis
from telegram.ext import BasePersistence, PersistenceInput


class RedisPersistence(BasePersistence):
    """Redis-backed persistence for PTB user_data, chat_data, bot_data, and conversations."""

    def __init__(self, redis_url: str, ttl: int = 86400 * 30) -> None:
        super().__init__(
            store_data=PersistenceInput(
                bot_data=True, chat_data=True, user_data=True, callback_data=False
            ),
            update_interval=1,
        )
        self.redis = Redis.from_url(redis_url, decode_responses=False)
        self.ttl = ttl
        self._bot_data: Dict[str, Any] = {}
        self._chat_data: Dict[int, Any] = {}
        self._user_data: Dict[int, Any] = {}
        self._conversations: Dict[str, Any] = {}

    # --- load ---
    async def get_bot_data(self) -> Dict[str, Any]:
        raw = await self.redis.get("ptb:bot_data")
        return pickle.loads(raw) if raw else {}

    async def get_chat_data(self) -> Dict[int, Any]:
        keys = await self.redis.keys("ptb:chat:*")
        return {
            int(k.split(b":")[-1]): pickle.loads(await self.redis.get(k)) for k in keys
        }

    async def get_user_data(self) -> Dict[int, Any]:
        keys = await self.redis.keys("ptb:user:*")
        return {
            int(k.split(b":")[-1]): pickle.loads(await self.redis.get(k)) for k in keys
        }

    async def get_conversations(self, name: str) -> Dict[Any, Any]:
        raw = await self.redis.get(f"ptb:conv:{name}")
        return pickle.loads(raw) if raw else {}

    # --- update ---
    async def update_bot_data(self, data: Dict[str, Any]) -> None:
        await self.redis.set("ptb:bot_data", pickle.dumps(data), ex=self.ttl)

    async def update_chat_data(self, chat_id: int, data: Any) -> None:
        await self.redis.set(f"ptb:chat:{chat_id}", pickle.dumps(data), ex=self.ttl)

    async def update_user_data(self, user_id: int, data: Any) -> None:
        await self.redis.set(f"ptb:user:{user_id}", pickle.dumps(data), ex=self.ttl)

    async def update_conversation(
        self, name: str, key: Any, new_state: Optional[object]
    ) -> None:
        convs = await self.get_conversations(name)
        if new_state is None:
            convs.pop(key, None)
        else:
            convs[key] = new_state
        await self.redis.set(f"ptb:conv:{name}", pickle.dumps(convs), ex=self.ttl)

    async def flush(self) -> None:
        pass  # writes are immediate
