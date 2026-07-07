import { useState } from 'react'
import { Alert, Box, Button, CircularProgress, Stack, Typography } from '@mui/material'
import type { NarrationTerm } from '../types/narration'

interface PreviewPanelProps {
  latex: string
  narrations: NarrationTerm[]
}

export function PreviewPanel({ latex, narrations }: PreviewPanelProps) {
  const [html, setHtml] = useState<string | undefined>(undefined)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleRender = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('/render', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          latex,
          narrations: narrations.filter((n) => n.term.trim() !== ''),
        }),
      })

      const body = await response.text()
      console.log(body)
      if (!response.ok) {
        const parsed = JSON.parse(body) as { error?: string }
        throw new Error(parsed.error || `Request failed with status ${response.status}`)
      }

      setHtml(body)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to render preview')
      setHtml(undefined)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', gap: 2 }}>
      <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="subtitle2">Preview</Typography>
        <Button size="small" variant="contained" onClick={handleRender} disabled={loading || !latex.trim()}>
          {loading ? <CircularProgress size={16} sx={{ color: 'inherit' }} /> : 'Render Preview'}
        </Button>
      </Stack>

      {error && <Alert severity="error">{error}</Alert>}

  
        <Box sx={{ flex: 1, border: '1px solid', borderColor: 'divider', borderRadius: 1, overflow: 'hidden' }}>
          <iframe
            title="Equation preview"
            srcDoc={html}
            sandbox="allow-scripts"
            style={{ width: '100%', height: '100%', border: 'none' }}
          />
        </Box>
      
    </Box>
  )
}
