# scripts/test_nvidia_agent.py
import asyncio
from app.ai.agent import assistant_agent


async def main() -> None:
    result = await assistant_agent.run("Say hello in one short sentence.")
    print("Output:", result.output)


if __name__ == "__main__":
    asyncio.run(main())
