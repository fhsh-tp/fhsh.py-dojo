import { useFetch, useWebSocket } from '@vueuse/core'
import type { UseFetchOptions, UseFetchReturn, UseWebSocketOptions, UseWebSocketReturn } from '@vueuse/core'

export function useApi<T = unknown>(
  url: string,
  options?: UseFetchOptions,
): UseFetchReturn<T> & PromiseLike<UseFetchReturn<T>> {
  return useFetch<T>(url, options ?? {})
}

export function useWsApi(url: string, options?: UseWebSocketOptions): UseWebSocketReturn {
  return useWebSocket(url, options)
}
