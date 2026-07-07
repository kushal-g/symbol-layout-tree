import { useState } from 'react'
import { Box, FormControl, InputLabel, MenuItem, Select, Tab, Tabs } from '@mui/material'
import type { SelectChangeEvent } from '@mui/material'
import { LatexEditor } from './components/LatexEditor'
import { NarrationsPanel } from './components/NarrationsPanel'
import { JsonPanel } from './components/JsonPanel'
import { PreviewPanel } from './components/PreviewPanel'
import { EXAMPLES } from './examples'
import type { Narration, NarrationTerm } from './types/narration'

type LeftTab = 'form' | 'json'

function App() {
  const [latex, setLatex] = useState('')
  const [narrations, setNarrations] = useState<Narration[]>([])
  const [tab, setTab] = useState<LeftTab>('form')

  const addNarration = () =>
    setNarrations((prev) => [
      ...prev,
      { id: crypto.randomUUID(), term: '', narration: '', pos: 1 },
    ])

  const updateNarration = (id: string, patch: Partial<Narration>) =>
    setNarrations((prev) =>
      prev.map((n) => (n.id === id ? { ...n, ...patch } : n)),
    )

  const removeNarration = (id: string) =>
    setNarrations((prev) => prev.filter((n) => n.id !== id))

  const applyFromJson = (data: { latex: string; narrations: NarrationTerm[] }) => {
    setLatex(data.latex)
    setNarrations(data.narrations.map((n) => ({ ...n, id: crypto.randomUUID() })))
  }

  const narrationTerms: NarrationTerm[] = narrations.map(({ term, narration, pos }) => ({ term, narration, pos }))

  const loadExample = (event: SelectChangeEvent) => {
    const example = EXAMPLES.find((e) => e.name === event.target.value)
    if (!example) return
    setLatex(example.latex)
    setNarrations(example.narrations.map((n) => ({ ...n, id: crypto.randomUUID() })))
  }

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Box
        sx={{
          width: { xs: '100%', md: '45%' },
          p: 3,
          borderRight: '1px solid',
          borderColor: 'divider',
          display: 'flex',
          flexDirection: 'column',
          gap: 3,
        }}
      >
        <FormControl size="small" fullWidth>
          <InputLabel id="example-select-label">Load Example</InputLabel>
          <Select labelId="example-select-label" label="Load Example" value="" onChange={loadExample}>
            {EXAMPLES.map((example) => (
              <MenuItem key={example.name} value={example.name}>
                {example.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Tabs value={tab} onChange={(_, value: LeftTab) => setTab(value)}>
          <Tab label="Form" value="form" />
          <Tab label="JSON (DSL)" value="json" />
        </Tabs>
        {tab === 'form' ? (
          <>
            <LatexEditor value={latex} onChange={setLatex} height="200px" />
            <NarrationsPanel
              narrations={narrations}
              onAdd={addNarration}
              onChange={updateNarration}
              onRemove={removeNarration}
            />
          </>
        ) : (
          <JsonPanel latex={latex} narrations={narrationTerms} onApply={applyFromJson} />
        )}
      </Box>
      <Box sx={{ flex: 1, p: 3 }}>
        <PreviewPanel latex={latex} narrations={narrationTerms} />
      </Box>
    </Box>
  )
}

export default App
