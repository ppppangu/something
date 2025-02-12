
### **使用步骤说明**

#### **1. 环境准备**
- 确保已安装以下依赖库：
  ```bash
  pip install aiohttp python-dotenv
  ```

#### **2. 配置 API 密钥**
- 在项目根目录下创建 `.env` 文件，并添加以下内容：
  ```env
  DeepSeek_API_KEY=你的API密钥
  ```

#### **3. 运行脚本**
- 执行脚本：
  ```bash
  python script.py
  ```

#### **4. 调整并发参数**
- 修改 `semaphore = asyncio.Semaphore(1000)` 中的 `1000`，根据硬件性能和 API 限制调整最大并发数。

#### **5. 查看结果**
- 脚本会打印以下信息：
  - 每个请求的结果。
  - 成功请求的数量。
  - 总耗时。

---

### **输出示例**
运行脚本后，终端将输出类似以下内容：

```plaintext
Error: ConnectionError, Retrying 1/3
Error: TimeoutError, Retrying 2/3
Retrying 5 failed requests...
{'role': 'assistant', 'content': '105'}
{'role': 'assistant', 'content': '110'}
成功的请求数量: 1998/2000
2000次请求用1000个最大并发数下耗费总时间为 12.34 秒
```

---

### **注意事项**
1. **API 限制**：
   - 确保 DeepSeek API 的调用频率和并发限制符合您的账户权限。
2. **超时处理**：
   - 如果网络不稳定或服务器响应慢，请适当增加重试次数（`max_retries`）和指数退避间隔。
3. **硬件性能**：
   - 高并发可能占用大量 CPU 和内存资源，请根据硬件性能调整 `semaphore` 的值。

---