<script setup lang="ts">
/**
 * EditorSettingsPopover — the gear ⚙ entry point for editor settings.
 *
 * Self-contained: owns its open/close state and binds the two v1 toggles
 * (autocomplete, bracket auto-close) directly to the shared `useEditorSettings`
 * ref, so changes persist and apply live. Closes on outside click and Escape.
 *
 * The gear lives in ChallengeView's bottom action bar, which is inside an
 * `overflow-hidden`, height-clamped flex column. An in-flow popover would be
 * clipped by that ancestor (z-index cannot escape overflow clipping), so the
 * panel is teleported to <body> and positioned `fixed`, anchored to the gear's
 * on-screen rect. Swapping the settings surface later means replacing only this
 * component.
 */
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useEditorSettings, DEFAULT_EDITOR_SETTINGS } from '../../composables/useEditorSettings'

const settings = useEditorSettings()
const isOpen = ref(false)
const gearRef = ref<HTMLElement | null>(null)
const panelRef = ref<HTMLElement | null>(null)
const panelStyle = ref<Record<string, string>>({})

function positionPanel() {
  const gear = gearRef.value
  if (!gear) return
  const rect = gear.getBoundingClientRect()
  // Open upward from the gear: pin the panel's bottom just above the gear and
  // align its right edge with the gear's right edge.
  panelStyle.value = {
    position: 'fixed',
    bottom: `${Math.max(8, window.innerHeight - rect.top + 8)}px`,
    right: `${Math.max(8, window.innerWidth - rect.right)}px`,
  }
}

async function openPanel() {
  positionPanel()
  isOpen.value = true
  await nextTick()
  positionPanel()
}
function close() {
  isOpen.value = false
}
function toggleOpen() {
  if (isOpen.value) close()
  else void openPanel()
}
function reset() {
  settings.value = { ...DEFAULT_EDITOR_SETTINGS }
}

// Dismiss on `mousedown` (not `click`): the gear sits atop ChallengeView's
// drag-resizable bottom panel, so grabbing the resize handle must close the
// popover BEFORE the drag shifts the gear's position — otherwise the fixed
// panel would detach from the (now-moved) gear for the duration of the drag.
function onDocumentPointerDown(e: MouseEvent) {
  if (!isOpen.value) return
  const target = e.target as Node
  if (gearRef.value?.contains(target) || panelRef.value?.contains(target)) return
  close()
}
function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') close()
}
function onReposition() {
  if (isOpen.value) positionPanel()
}

onMounted(() => {
  document.addEventListener('mousedown', onDocumentPointerDown)
  document.addEventListener('keydown', onKeydown)
  window.addEventListener('resize', onReposition)
})
onUnmounted(() => {
  document.removeEventListener('mousedown', onDocumentPointerDown)
  document.removeEventListener('keydown', onKeydown)
  window.removeEventListener('resize', onReposition)
})
</script>

<template>
  <div class="inline-block">
    <!-- Gear button -->
    <button
      ref="gearRef"
      type="button"
      data-testid="editor-settings-gear"
      class="p-1.5 rounded text-slate-500 hover:text-slate-800 hover:bg-slate-200 dark:text-gray-400 dark:hover:text-gray-100 dark:hover:bg-gray-800 transition-colors cursor-pointer flex items-center"
      :aria-expanded="isOpen"
      aria-label="編輯器設定"
      title="編輯器設定"
      @click="toggleOpen"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="3" />
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
      </svg>
    </button>

    <!-- Panel teleported to <body> so the overflow-hidden action bar cannot clip it -->
    <Teleport to="body">
      <div
        v-if="isOpen"
        ref="panelRef"
        :style="panelStyle"
        data-testid="editor-settings-panel"
        class="w-72 rounded-lg border border-slate-200 dark:border-gray-700 bg-white dark:bg-gray-900 shadow-xl p-4 z-50"
        role="dialog"
        aria-label="編輯器設定"
      >
        <h3 class="text-sm font-bold text-slate-800 dark:text-gray-100 mb-1">編輯器設定</h3>

        <label class="flex items-center justify-between gap-3 py-2.5 cursor-pointer border-b border-slate-100 dark:border-gray-800">
          <span class="text-sm text-slate-700 dark:text-gray-200">
            自動完成
            <small class="block text-xs text-slate-400 dark:text-gray-500 mt-0.5">輸入時自動彈出候選字與型別提示</small>
          </span>
          <input
            v-model="settings.autocomplete"
            data-testid="toggle-autocomplete"
            type="checkbox"
            class="w-4 h-4 shrink-0 accent-emerald-600 cursor-pointer"
          />
        </label>

        <label class="flex items-center justify-between gap-3 py-2.5 cursor-pointer">
          <span class="text-sm text-slate-700 dark:text-gray-200">
            括號自動閉合
            <small class="block text-xs text-slate-400 dark:text-gray-500 mt-0.5">輸入 ( [ &#123; 時自動補上對應右括號</small>
          </span>
          <input
            v-model="settings.closeBrackets"
            data-testid="toggle-close-brackets"
            type="checkbox"
            class="w-4 h-4 shrink-0 accent-emerald-600 cursor-pointer"
          />
        </label>

        <div class="pt-3 mt-1 border-t border-slate-100 dark:border-gray-800 flex justify-end">
          <button
            type="button"
            data-testid="editor-settings-reset"
            class="text-xs text-sky-600 dark:text-sky-400 hover:underline cursor-pointer"
            @click="reset"
          >
            重設為預設值
          </button>
        </div>
      </div>
    </Teleport>
  </div>
</template>
