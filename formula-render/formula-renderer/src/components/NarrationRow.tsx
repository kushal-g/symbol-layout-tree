import { IconButton, Paper, Stack, TextField } from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'
import type { Narration } from '../types/narration'
import { LatexEditor } from './LatexEditor'

interface NarrationRowProps {
  narration: Narration
  onChange: (id: string, patch: Partial<Narration>) => void
  onRemove: (id: string) => void
}

export function NarrationRow({ narration, onChange, onRemove }: NarrationRowProps) {
  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Stack direction="row" spacing={2} sx={{ alignItems: 'flex-start' }}>
        <Stack spacing={2} sx={{ flex: 1 }}>
          <LatexEditor
            label="Latex term"
            compact
            value={narration.term}
            onChange={(term) => onChange(narration.id, { term })}
          />
          <TextField
            label="Narration text"
            size="small"
            fullWidth
            multiline
            minRows={2}
            value={narration.narration}
            onChange={(e) => onChange(narration.id, { narration: e.target.value })}
          />
          <TextField
            label="Occurrence"
            size="small"
            type="number"
            slotProps={{ htmlInput: { min: 1 } }}
            value={narration.pos}
            onChange={(e) =>
              onChange(narration.id, { pos: Number(e.target.value) })
            }
          />
        </Stack>
        <IconButton
          aria-label="Remove narration"
          onClick={() => onRemove(narration.id)}
        >
          <DeleteIcon />
        </IconButton>
      </Stack>
    </Paper>
  )
}
