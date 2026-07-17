FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir python-multipart

# 复制源码
COPY mock_api_server.py .

# 健康检查
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:3001/health')"

EXPOSE 3001

CMD ["uvicorn", "mock_api_server:app", "--host", "0.0.0.0", "--port", "3001", "--reload"]