// Simple global toast system using custom events
export function toast(message, type = 'info', duration = 3200) {
  window.dispatchEvent(new CustomEvent('app-toast', { detail: { message, type, duration } }))
}
export const toastOk = m => toast(m, 'success')
export const toastErr = m => toast(m, 'danger', 4800)
export const toastWarn = m => toast(m, 'warn')
