import CodeMirror from '@uiw/react-codemirror'
import { Box, Typography } from '@mui/material'
import { stexLanguage } from '../lib/stexLanguage'

interface LatexEditorProps {
  label?: string
  value: string
  onChange: (value: string) => void
  height?: string
  compact?: boolean
}

export function LatexEditor({
  label = 'Latex',
  value,
  onChange,
  height,
  compact = false,
}: LatexEditorProps) {
  return (
    <Box>
      <Typography variant="subtitle2" sx={{ mb: 1 }}>
        {label}
      </Typography>
      <CodeMirror
        value={value}
        height={height}
        basicSetup={
          compact
            ? { lineNumbers: false, foldGutter: false, highlightActiveLine: false }
            : undefined
        }
        extensions={[stexLanguage]}
        onChange={onChange}
        style={{border:"1px solid rgba(0, 0, 0, 0.23)", borderRadius: "4px"}}
      />
    </Box>
  )
}
