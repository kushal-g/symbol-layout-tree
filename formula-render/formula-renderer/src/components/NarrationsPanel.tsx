import { Box, Button, Stack, Typography } from '@mui/material'
import AddIcon from '@mui/icons-material/Add'
import type { Narration } from '../types/narration'
import { NarrationRow } from './NarrationRow'

interface NarrationsPanelProps {
  narrations: Narration[]
  onAdd: () => void
  onChange: (id: string, patch: Partial<Narration>) => void
  onRemove: (id: string) => void
}

export function NarrationsPanel({
  narrations,
  onAdd,
  onChange,
  onRemove,
}: NarrationsPanelProps) {
  return (
    <Box>
      <Stack
        direction="row"
        sx={{ alignItems: 'center', justifyContent: 'space-between', mb: 1 }}
      >
        <Typography variant="subtitle2">Narrations</Typography>
        <Button size="small" startIcon={<AddIcon />} onClick={onAdd}>
          Add Narration
        </Button>
      </Stack>
      <Stack spacing={2}>
        {narrations.map((narration) => (
          <NarrationRow
            key={narration.id}
            narration={narration}
            onChange={onChange}
            onRemove={onRemove}
          />
        ))}
      </Stack>
    </Box>
  )
}
