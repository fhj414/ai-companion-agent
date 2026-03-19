<template>
  <div class="page">
    <div class="container">
      <h1>AI Companion Agent</h1>

      <div class="chat-box">
        <div
          v-for="(item, index) in messages"
          :key="index"
          :class="['msg', item.role]"
        >
          <div class="role">{{ item.role === 'user' ? '我' : 'AI' }}</div>
          <div class="content">{{ item.content }}</div>
        </div>

        <div v-if="loading" class="msg assistant">
          <div class="role">AI</div>
          <div class="content">思考中...</div>
        </div>
      </div>

      <div class="input-area">
        <textarea
          v-model="inputValue"
          placeholder="输入你想说的话"
          @keydown.enter.exact.prevent="sendMessage"
        />
        <button :disabled="loading || !inputValue.trim()" @click="sendMessage">
          发送
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'

const inputValue = ref('')
const loading = ref(false)

const messages = ref([
  {
    role: 'system',
    content: '你是一个温柔、聪明、会长期陪伴用户的AI伙伴。',
  },
  {
    role: 'assistant',
    content: '你好，我已经准备好了。你今天想聊什么？',
  },
])

const sendMessage = async () => {
  const text = inputValue.value.trim()
  if (!text || loading.value) return

  messages.value.push({
    role: 'user',
    content: text,
  })
  inputValue.value = ''
  loading.value = true

  try {
    const res = await axios.post('http://127.0.0.1:8000/api/chat', {
      messages: messages.value,
    })

    messages.value.push({
      role: 'assistant',
      content: res.data.reply,
    })
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: '请求失败，请检查后端或API Key配置。',
    })
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f5f7fb;
  padding: 24px;
  box-sizing: border-box;
}
.container {
  width: 900px;
  margin: 0 auto;
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-sizing: border-box;
}
h1 {
  margin: 0 0 20px;
}
.chat-box {
  height: 520px;
  overflow-y: auto;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  background: #fafafa;
}
.msg {
  margin-bottom: 16px;
}
.msg.system {
  display: none;
}
.role {
  font-size: 12px;
  color: #666;
  margin-bottom: 6px;
}
.content {
  display: inline-block;
  max-width: 75%;
  line-height: 1.7;
  padding: 12px 14px;
  border-radius: 12px;
  word-break: break-word;
}
.user .content {
  background: #dbeafe;
}
.assistant .content {
  background: #f3f4f6;
}
.input-area {
  margin-top: 16px;
  display: flex;
  gap: 12px;
}
textarea {
  flex: 1;
  min-height: 100px;
  resize: vertical;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 12px;
  font-size: 14px;
  outline: none;
}
button {
  width: 100px;
  border: none;
  border-radius: 12px;
  background: #111827;
  color: #fff;
  cursor: pointer;
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>