import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import {
  DEADLINE_MS,
  INTERRUPT_SIGNAL,
  SLOT_SIGNAL,
  SLOT_GENERATION,
  GENERATION_IDLE,
  createInterruptChannel,
  DeadlineWatchdog,
  resetDegradationNotice,
} from '../workers/deadline'

describe('deadline module', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    vi.clearAllMocks()
    // The degraded-path notice is a per-page one-shot; each test needs it fresh.
    resetDegradationNotice()
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.unstubAllGlobals()
  })

  describe('constants', () => {
    it('exposes a positive per-testcase deadline', () => {
      expect(DEADLINE_MS).toBeGreaterThan(0)
    })

    it('uses the Pyodide interrupt signal value for SIGINT', () => {
      // Pyodide raises KeyboardInterrupt when the buffer's signal slot holds 2.
      expect(INTERRUPT_SIGNAL).toBe(2)
    })

    it('keeps the signal and generation slots distinct', () => {
      expect(SLOT_SIGNAL).not.toBe(SLOT_GENERATION)
    })
  })

  describe('createInterruptChannel()', () => {
    it('reports supported and returns a shared buffer when SharedArrayBuffer exists', () => {
      const channel = createInterruptChannel()
      expect(channel.supported).toBe(true)
      expect(channel.buffer).not.toBeNull()
      expect(channel.view).not.toBeNull()
      expect(channel.view!.length).toBeGreaterThanOrEqual(2)
    })

    it('degrades to unsupported without throwing when SharedArrayBuffer is absent', () => {
      vi.stubGlobal('SharedArrayBuffer', undefined)
      const channel = createInterruptChannel()
      expect(channel.supported).toBe(false)
      expect(channel.buffer).toBeNull()
      expect(channel.view).toBeNull()
    })

    it('warns exactly once about the degraded path across repeated creation', () => {
      vi.stubGlobal('SharedArrayBuffer', undefined)
      const warn = vi.spyOn(console, 'warn').mockImplementation(() => {})
      createInterruptChannel()
      createInterruptChannel()
      createInterruptChannel()
      expect(warn).toHaveBeenCalledTimes(1)
      warn.mockRestore()
    })
  })

  describe('DeadlineWatchdog', () => {
    it('raises the interrupt signal once the deadline elapses', () => {
      const channel = createInterruptChannel()
      const wd = new DeadlineWatchdog(channel)

      wd.arm(1)
      expect(channel.view![SLOT_SIGNAL]).toBe(0)

      vi.advanceTimersByTime(DEADLINE_MS)
      expect(channel.view![SLOT_SIGNAL]).toBe(INTERRUPT_SIGNAL)
    })

    it('does not raise the signal before the deadline elapses', () => {
      const channel = createInterruptChannel()
      const wd = new DeadlineWatchdog(channel)

      wd.arm(1)
      vi.advanceTimersByTime(DEADLINE_MS - 1)
      expect(channel.view![SLOT_SIGNAL]).toBe(0)
    })

    it('disarm prevents a pending expiry from raising the signal', () => {
      const channel = createInterruptChannel()
      const wd = new DeadlineWatchdog(channel)

      wd.arm(1)
      wd.disarm()
      vi.advanceTimersByTime(DEADLINE_MS * 3)
      expect(channel.view![SLOT_SIGNAL]).toBe(0)
    })

    it('a stale expiry from an earlier testcase cannot interrupt a later one', () => {
      const channel = createInterruptChannel()
      const wd = new DeadlineWatchdog(channel)

      // Testcase 1 is armed, then finishes quickly and is disarmed.
      wd.arm(1)
      wd.disarm()
      // Testcase 2 starts and is still well within its own budget when the
      // timer scheduled for testcase 1 would have fired.
      wd.arm(2)
      vi.advanceTimersByTime(DEADLINE_MS - 1)
      expect(channel.view![SLOT_SIGNAL]).toBe(0)
    })

    it('arm clears a signal left over from the previous testcase', () => {
      const channel = createInterruptChannel()
      const wd = new DeadlineWatchdog(channel)

      wd.arm(1)
      vi.advanceTimersByTime(DEADLINE_MS)
      expect(channel.view![SLOT_SIGNAL]).toBe(INTERRUPT_SIGNAL)

      wd.arm(2)
      expect(channel.view![SLOT_SIGNAL]).toBe(0)
    })

    it('publishes a live generation into the shared buffer on arm', () => {
      const channel = createInterruptChannel()
      const wd = new DeadlineWatchdog(channel)

      wd.arm(7)
      expect(channel.view![SLOT_GENERATION]).toBe(8)
    })

    it('never arms with the idle sentinel, whatever the counter value', () => {
      // GENERATION_IDLE means "the Worker has disarmed"; an armed testcase
      // taking that value would let a stale expiry match a disarmed slot.
      const channel = createInterruptChannel()
      const wd = new DeadlineWatchdog(channel)

      for (const g of [0, 1, 254, 255, 256, 509, 510, 1000]) {
        wd.arm(g)
        expect(channel.view![SLOT_GENERATION]).not.toBe(GENERATION_IDLE)
        expect(channel.view![SLOT_GENERATION]).toBeLessThanOrEqual(255)
      }
    })

    it('wraps the generation so it always fits the shared byte slot', () => {
      const channel = createInterruptChannel()
      const wd = new DeadlineWatchdog(channel)

      wd.arm(256)
      expect(channel.view![SLOT_GENERATION]).toBe(2)
      vi.advanceTimersByTime(DEADLINE_MS)
      expect(channel.view![SLOT_SIGNAL]).toBe(INTERRUPT_SIGNAL)
    })

    it('disarm parks the slot at the idle sentinel so a stale expiry cannot match', () => {
      const channel = createInterruptChannel()
      const wd = new DeadlineWatchdog(channel)

      wd.arm(1)
      wd.disarm()
      expect(channel.view![SLOT_GENERATION]).toBe(GENERATION_IDLE)
    })

    it('is inert but safe when the channel is unsupported', () => {
      vi.stubGlobal('SharedArrayBuffer', undefined)
      const channel = createInterruptChannel()
      const wd = new DeadlineWatchdog(channel)

      expect(() => {
        wd.arm(1)
        vi.advanceTimersByTime(DEADLINE_MS * 2)
        wd.disarm()
        wd.dispose()
      }).not.toThrow()
    })

    it('dispose cancels any pending expiry', () => {
      const channel = createInterruptChannel()
      const wd = new DeadlineWatchdog(channel)

      wd.arm(1)
      wd.dispose()
      vi.advanceTimersByTime(DEADLINE_MS * 3)
      expect(channel.view![SLOT_SIGNAL]).toBe(0)
    })
  })

  describe('exceededDeadline()', () => {
    it('adjudicates on measured elapsed time regardless of the interrupt path', async () => {
      const { exceededDeadline } = await import('../workers/deadline')
      expect(exceededDeadline(DEADLINE_MS + 1)).toBe(true)
      expect(exceededDeadline(DEADLINE_MS)).toBe(false)
      expect(exceededDeadline(0)).toBe(false)
    })
  })
})
