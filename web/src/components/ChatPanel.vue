<template>
  <main class="main">
    <div class="main-header">
      <h1>AI Companion Agent</h1>
      <ExportActions @export="emit('export', $event)" />
    </div>

    <div class="prompt-panel">
      <div class="prompt-panel-header">
        <div class="prompt-panel-title">Prompt Playground</div>
        <div class="prompt-panel-actions">
          <button class="prompt-btn secondary" @click="emit('reset-prompt')">恢复默认</button>
          <button class="prompt-btn" @click="emit('save-prompt')">保存 Prompt</button>
        </div>
      </div>

      <textarea
        :value="promptDraft"
        class="prompt-textarea"
        placeholder="编辑当前会话的 system prompt"
        @input="emit('update:promptDraft', $event.target.value)"
      />

      <div class="prompt-template-list">
        <span
          class="prompt-template-tag"
          @click="emit('use-prompt-template', '你是一个专业、友好、清晰的 AI 助手，回答准确，表达简洁。')"
        >
          通用助手
        </span>
        <span
          class="prompt-template-tag"
          @click="
            emit(
              'use-prompt-template',
              '你是一个资深技术顾问，回答时要结构化、专业、可执行，优先给出步骤、代码和避坑建议。'
            )
          "
        >
          技术顾问模板
        </span>
        <span
          class="prompt-template-tag"
          @click="
            emit(
              'use-prompt-template',
              '你是一个资深面试教练，请从面试官视角给出高质量回答，突出考点、答题框架和表达建议。'
            )
          "
        >
          面试教练模板
        </span>
        <span
          class="prompt-template-tag"
          @click="emit('use-prompt-template', '你是一个温柔、稳定、善于倾听和鼓励的陪伴型 AI，回答自然、真诚、有情绪价值。')"
        >
          陪伴模板
        </span>
      </div>
    </div>

    <div class="params-panel">
      <div class="params-panel-header">
        <div class="params-panel-title">聊天参数</div>
        <button class="prompt-btn" @click="emit('save-params')">保存参数</button>
      </div>

      <div class="params-grid">
        <div class="param-item">
          <label class="param-label">temperature</label>
          <input
            :value="temperatureDraft"
            class="param-input"
            type="number"
            min="0"
            max="2"
            step="0.1"
            @input="emit('update:temperatureDraft', $event.target.value)"
          />
          <div class="param-tip">越高越发散，越低越稳定</div>
        </div>

        <div class="param-item">
          <label class="param-label">top_p</label>
          <input
            :value="topPDraft"
            class="param-input"
            type="number"
            min="0"
            max="1"
            step="0.1"
            @input="emit('update:topPDraft', $event.target.value)"
          />
          <div class="param-tip">控制采样范围</div>
        </div>

        <div class="param-item">
          <label class="param-label">max_tokens</label>
          <input
            :value="maxTokensDraft"
            class="param-input"
            type="number"
            min="100"
            max="4000"
            step="100"
            @input="emit('update:maxTokensDraft', $event.target.value)"
          />
          <div class="param-tip">限制单次最大输出长度</div>
        </div>
      </div>
    </div>

    <MessageList
      :current-messages="currentMessages"
      :loading="loading"
      :on-copy-message="onCopyMessage"
      :on-delete-message="onDeleteMessage"
      :on-regenerate="onRegenerate"
    />
    <MessageInput
      :loading="loading"
      :input-value="inputValue"
      @update:input-value="emit('update:inputValue', $event)"
      @send="emit('send')"
      @abort="emit('abort')"
    />
  </main>
</template>

<script setup>
import ExportActions from './ExportActions.vue'
import MessageInput from './MessageInput.vue'
import MessageList from './MessageList.vue'

const props = defineProps({
  currentMessages: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    required: true,
  },
  inputValue: {
    type: String,
    required: true,
  },
  promptDraft: {
    type: String,
    required: true,
  },
  temperatureDraft: {
    type: [Number, String],
    required: true,
  },
  topPDraft: {
    type: [Number, String],
    required: true,
  },
  maxTokensDraft: {
    type: [Number, String],
    required: true,
  },
  onCopyMessage: {
    type: Function,
    required: true,
  },
  onDeleteMessage: {
    type: Function,
    required: true,
  },
  onRegenerate: {
    type: Function,
    required: true,
  },
})

const emit = defineEmits([
  'update:inputValue',
  'send',
  'abort',
  'export',
  'update:promptDraft',
  'save-prompt',
  'reset-prompt',
  'use-prompt-template',
  'update:temperatureDraft',
  'update:topPDraft',
  'update:maxTokensDraft',
  'save-params',
])
</script>

<style scoped>
.main {
  flex: 1;
  min-width: 0;
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-sizing: border-box;
  height: calc(100vh - 48px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.main-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.main-header h1 {
  margin: 0;
  font-size: 40px;
  line-height: 1.2;
  color: #111827;
  font-weight: 700;
}

.prompt-panel {
  margin-bottom: 16px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #fafafa;
}

.prompt-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.prompt-panel-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.prompt-panel-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.prompt-btn {
  border: none;
  border-radius: 10px;
  background: #111827;
  color: #fff;
  padding: 8px 12px;
  font-size: 12px;
  cursor: pointer;
}

.prompt-btn.secondary {
  background: #6b7280;
}

.prompt-textarea {
  width: 100%;
  min-height: 96px;
  resize: vertical;
  box-sizing: border-box;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  padding: 12px;
  font-size: 14px;
  line-height: 1.6;
  outline: none;
  background: #fff;
  margin-bottom: 12px;
}

.prompt-template-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.prompt-template-tag {
  display: inline-flex;
  align-items: center;
  padding: 6px 10px;
  border-radius: 999px;
  background: #eef2ff;
  color: #4338ca;
  font-size: 12px;
  cursor: pointer;
}

.prompt-template-tag:hover {
  background: #e0e7ff;
}

.params-panel {
  margin-bottom: 16px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #fafafa;
}

.params-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.params-panel-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.params-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.param-item {
  padding: 12px;
  border-radius: 10px;
  background: #fff;
  border: 1px solid #e5e7eb;
}

.param-label {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #111827;
}

.param-input {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 8px 10px;
  font-size: 14px;
  outline: none;
  background: #fff;
}

.param-tip {
  margin-top: 8px;
  font-size: 12px;
  color: #6b7280;
}
</style>
