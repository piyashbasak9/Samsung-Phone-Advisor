# 🆓 FREE Groq API Setup Guide

## What is Groq?

Groq is a **completely FREE** API for AI models. No credit card needed, unlimited free tier!

| Feature | Groq | OpenAI |
|---------|------|--------|
| **Cost** | FREE ✅ | PAID |
| **Credit Card** | NOT needed ✅ | REQUIRED |
| **Speed** | ⚡⚡⚡ Super Fast | Good |
| **Model** | Mixtral 8x7B | GPT-4o-mini |
| **Setup Time** | 1 minute | Requires billing |

---

## 📋 Step-by-Step Setup (Takes 1 Minute)

### Step 1️⃣: Go to Groq Console

Open this link in your browser:
```
https://console.groq.com/keys
```

You'll see the Groq API Keys page.

### Step 2️⃣: Sign Up (Free)

- Click **"Sign Up"** button
- Enter your email
- Create a password
- Check your email and click verify link
- Done! ✅

### Step 3️⃣: Create API Key

1. Go back to: https://console.groq.com/keys
2. Click **"Create API Key"** button
3. Give it a name (e.g., "Samsung Phone Advisor")
4. Click **"Create"**
5. Copy the key (it starts with `gsk_`)

### Step 4️⃣: Add to Your Project

1. Open `.env` file in your project
2. Find this line:
   ```
   GROQ_API_KEY=gsk_YOUR_KEY_HERE
   ```
3. Replace `gsk_YOUR_KEY_HERE` with your actual key from Step 3
4. Example:
   ```
   GROQ_API_KEY=gsk_abc123xyz789...
   ```
5. Save the file

### Step 5️⃣: Restart Your Server

Stop your running server (Ctrl+C) and restart:

```bash
cd /home/piyash/Desktop/Tasks/Samsung\ Phone\ Advisor
source venv/bin/activate
python main.py
```

### Step 6️⃣: Test It!

Run this command to test:

```bash
python -c "
import requests
import json

response = requests.get('http://localhost:8000/test/openai')
print(json.dumps(response.json(), indent=2))
"
```

**If you see `"status": "success"` - You're done!** ✅

---

## 🧪 Using the API

Now your endpoints work with FREE Groq:

### Ask about a phone
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Tell me about Galaxy S24 Ultra"}'
```

### Send any prompt
```bash
curl -X POST http://localhost:8000/llm \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Why is S24 good for photography?"}'
```

### Test without using quota
```bash
curl -X POST http://localhost:8000/llm/demo \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Tell me about Samsung"}'
```

---

## ⚠️ Troubleshooting

### Problem: "GROQ_API_KEY not set"

**Solution:**
1. Open `.env` file
2. Make sure you added your key to this line:
   ```
   GROQ_API_KEY=gsk_YOUR_KEY_HERE
   ```
3. Restart the server

### Problem: "Invalid Groq API Key"

**Solution:**
1. Go to: https://console.groq.com/keys
2. Check if your key is correct
3. Create a new key if the old one is broken
4. Update `.env` with the new key
5. Restart server

### Problem: Still not working?

1. Check `.env` file has correct format:
   ```
   GROQ_API_KEY=gsk_abc123...
   ```
   (NO spaces, NO quotes)

2. Make sure you restarted the server after adding the key

3. Try the diagnostic endpoint:
   ```bash
   curl http://localhost:8000/test/openai
   ```

4. Check internet connection is working

---

## 📚 More Information

- **Groq Official Docs**: https://console.groq.com/docs
- **Groq Models Available**: https://console.groq.com/docs/models
- **Free Tier Limits**: Unlimited requests (fair use policy)

---

## 💡 Why I Recommend Groq

✅ Completely FREE  
✅ No credit card required  
✅ Super fast (10x faster than OpenAI)  
✅ Great model quality (Mixtral 8x7B)  
✅ Easy setup  
✅ Perfect for development and testing  

---

**That's it! You now have a FREE AI-powered Samsung Phone Advisor!** 🚀

