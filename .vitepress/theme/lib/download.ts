/**
 * Trigger a client-side file download of in-memory text via a Blob + anchor.
 * Navigations (anchor downloads) are not governed by the CSP connect-src, so
 * this works under the project's locked policy.
 */
export function downloadTextFile(filename: string, content: string, mime: string): void {
  const blob = new Blob([content], { type: mime })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}
