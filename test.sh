curl -N http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "what can vllm do"
  }'