# Prompt java project

测试接入方法网址：https://github.com/open-compass/code-evaluator

## 运行测试

### 构建docker
```bash
git clone https://github.com/open-compass/code-evaluator.git
cd code-evaluator
docker build -t code-eval-humanevalx:latest -f docker/humanevalx/Dockerfile .
```

### 运行docker
```bash
# Output Log Format
sudo docker run -it -p 5000:5000 code-eval-humanevalx:latest python server.py
```

### 提交测试
```bash
curl -X POST -F 'file=@./output.jsonl' -F 'dataset=humanevalx/java' localhost:5000/evaluate
```

### 查询余额
```bash
curl -X POST -H "Content-Type: application/json" -d '{"api_key":"sk-x1Tf548857Gvrkxr69D1Be7b453e473cB8B9D4D4Eb015dE5"}' https://billing.openkey.cloud/api/token
```