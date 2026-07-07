import { useEffect, useRef, useState } from 'react'
import CodeMirror from '@uiw/react-codemirror'
import { json } from '@codemirror/lang-json'
import { Box, Typography } from '@mui/material'
import type { NarrationTerm } from '../types/narration'

interface FormData {
  latex: string
  narrations: NarrationTerm[]
}

interface JsonPanelProps {
  latex: string
  narrations: NarrationTerm[]
  onApply: (data: FormData) => void
}

function formatJson(latex: string, narrations: NarrationTerm[]) {
  return JSON.stringify({ latex, narrations }, null, 2)
}

function parseFormData(text: string): FormData {
  const parsed = JSON.parse(text)
  if (
    typeof parsed !== 'object' ||
    parsed === null ||
    typeof parsed.latex !== 'string' ||
    !Array.isArray(parsed.narrations)
  ) {
    throw new Error('Expected an object shaped like { latex: string, narrations: [] }')
  }

  const narrations: NarrationTerm[] = parsed.narrations.map((n: unknown) => {
    const entry = (n ?? {}) as Partial<NarrationTerm>
    return {
      term: typeof entry.term === 'string' ? entry.term : '',
      narration: typeof entry.narration === 'string' ? entry.narration : '',
      pos: typeof entry.pos === 'number' ? entry.pos : 1,
    }
  })

  return { latex: parsed.latex, narrations }
}

export function JsonPanel({ latex, narrations, onApply }: JsonPanelProps) {
  const [text, setText] = useState(() => formatJson(latex, narrations))
  const [error, setError] = useState<string | null>(null)
  const skipNextSync = useRef(false)

  useEffect(() => {
    if (skipNextSync.current) {
      skipNextSync.current = false
      return
    }
    setText(formatJson(latex, narrations))
    setError(null)
  }, [latex, narrations])

  const handleChange = (value: string) => {
    setText(value)
    try {
      const data = parseFormData(value)
      setError(null)
      skipNextSync.current = true
      onApply(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Invalid JSON')
    }
  }

  return (
    <Box>
      <Typography variant="subtitle2" sx={{ mb: 1 }}>
        JSON
      </Typography>
      <CodeMirror value={text} height="500px" extensions={[json()]} onChange={handleChange} />
      {error && (
        <Typography variant="caption" color="error" sx={{ display: 'block', mt: 1 }}>
          {error}
        </Typography>
      )}
    </Box>
  )
}
