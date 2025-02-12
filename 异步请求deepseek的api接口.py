import os
from dotenv import load_dotenv, find_dotenv
import time
import asyncio
import aiohttp

# 加载环境变量中的 DeepSeek API 密钥
load_dotenv(find_dotenv())
deepseek_api_key = os.getenv("DeepSeek_API_KEY")

# 设置最大并发数
semaphore = asyncio.Semaphore(1000)

async def _get_response(message, max_retries=3):
    """
    异步获取 DeepSeek API 响应。

    参数:
    - message (str): 用户的请求消息。
    - max_retries (int): 最大重试次数，默认为 3。

    返回:
    - dict: 成功时返回 API 响应，失败时返回错误信息。
    """
    async with semaphore:
        for i in range(max_retries):
            try:
                # 创建异步会话
                async with aiohttp.ClientSession(
                    base_url='https://api.deepseek.com/v1/',
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {deepseek_api_key}"}
                ) as session:
                    # 构造请求载荷
                    payload = {
                        'model': 'deepseek-chat',
                        'messages': [
                            {'role': 'system', 'content': 'you are an ai assistant'},
                            {'role': 'user', 'content': message}
                        ]
                    }
                    # 发送 POST 请求
                    async with session.post(url='chat/completions', json=payload) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            print(f"Request failed with status {response.status}")
            except Exception as e:
                print(f'Error: {e}, Retrying {i + 1}/{max_retries}')
            await asyncio.sleep(2 ** i)  # 指数退避策略
        print(f'{message} 请求未发送成功')
        return {'error': 'Failed after retries', 'message': message}

async def _main(num):
    """
    主函数：执行批量 API 请求并处理失败请求。

    参数:
    - num (int): 要发送的请求数量。
    """
    start = time.time()

    # 构造请求消息列表
    messages = [f'{i}加100等于多少，只回答最后的结果即可' for i in range(num)]

    # 创建任务列表
    tasks = [_get_response(i) for i in messages]

    # 执行所有任务
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 记录失败的请求
    failed_requests = [messages[i] for i, result in enumerate(results) if 'error' in result]

    # 对失败请求进行重试
    while failed_requests:
        print(f"Retrying {len(failed_requests)} failed requests...")
        retry_tasks = [_get_response(msg) for msg in failed_requests]
        retry_results = await asyncio.gather(*retry_tasks, return_exceptions=True)

        # 更新失败请求列表
        failed_requests = [failed_requests[i] for i, result in enumerate(retry_results) if 'error' in result]
        results.extend(retry_results)

    # 打印结果
    success_count = len([res for res in results if 'error' not in res])
    print(f"成功的请求数量: {success_count}/{num}")

    end = time.time()
    print(f'{num}次请求用{semaphore._value}个最大并发数下耗费总时间为 {end - start:.2f} 秒')

# 执行主函数
if __name__ == "__main__":
    asyncio.run(_main(2000))
