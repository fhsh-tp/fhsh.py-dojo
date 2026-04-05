import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('@vueuse/core', () => ({
  useFetch: vi.fn((url: string, options?: object) => ({
    data: { value: null },
    error: { value: null },
    isFetching: { value: false },
    execute: vi.fn(),
    _url: url,
    _options: options,
  })),
  useWebSocket: vi.fn((url: string, options?: object) => ({
    data: { value: null },
    status: { value: 'CLOSED' },
    send: vi.fn(),
    close: vi.fn(),
    _url: url,
    _options: options,
  })),
}))

import { useApi, useWsApi } from '../composables/useApi'

describe('useApi', () => {
  it('returns UseFetchReturn shape', () => {
    const result = useApi('https://example.com/api')
    expect(result).toHaveProperty('data')
    expect(result).toHaveProperty('error')
    expect(result).toHaveProperty('isFetching')
    expect(result).toHaveProperty('execute')
  })

  it('forwards url to useFetch', () => {
    const url = 'https://example.com/api/test'
    const result = useApi(url) as any
    expect(result._url).toBe(url)
  })

  it('forwards options to useFetch', () => {
    const options = { method: 'POST' as const }
    const result = useApi('https://example.com/api', options) as any
    expect(result._options).toEqual(options)
  })
})

describe('useWsApi', () => {
  it('returns UseWebSocketReturn shape', () => {
    const result = useWsApi('wss://example.com/ws')
    expect(result).toHaveProperty('data')
    expect(result).toHaveProperty('status')
    expect(result).toHaveProperty('send')
    expect(result).toHaveProperty('close')
  })

  it('forwards url to useWebSocket', () => {
    const url = 'wss://example.com/ws/test'
    const result = useWsApi(url) as any
    expect(result._url).toBe(url)
  })

  it('forwards options to useWebSocket', () => {
    const options = { autoReconnect: true }
    const result = useWsApi('wss://example.com/ws', options) as any
    expect(result._options).toEqual(options)
  })
})
