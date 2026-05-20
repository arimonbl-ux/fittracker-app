# CHANGELOG — FitTracker Pro

Convención: `vNN — fecha — qué cambió` · agrupado por commit en `main`.

---

## v25 — 2026-05-20 — dark-mode-first + gym-readable

**Diseño visual (Claude Design):**
- Paleta dark-mode-first como default — `bg #000`, surface `#1c1c1e`, accent iOS dark `#0a84ff`, semáforo iOS dark (`#30d158` ok, `#ff9f0a` warn, `#ff453a` bad, `#bf5af2` coach)
- Texto principal `#f2f2f7` (alto contraste sobre fondo negro)
- Tipografía SF Pro Display/Text system stack, antialiased + tabular-nums para números legibles
- Clase `.hero-num` para números que deben leerse desde 1 metro
- Indicador de set agrandado: `fontSize 19`, `fontWeight 800`, padding 6px, bordes sutiles con tinte del color RIR
- Tap targets ≥44px en inputs (cumple Apple HIG)
- Background con radial gradients sutiles (azul + morado dark) para profundidad sin saturar
- `prefers-color-scheme: light` reservado como opt-in body class (no auto-activa)
- Impreso conservado en light (papel) — `imprimir()` independiente

**Header:**
- "FITTRACKER" en SF Pro Display 17px (antes monospace 15px)
- Badge `v25` visible al lado del logotipo (monospace 11px, opacity 0.7)
- UserSelector logo agrandado a 28px con peso 800 + subtítulo monospace

**Constantes:**
- `const APP_VERSION = 'v25'` agregado en bloque de configuración global
- `G.ink` (white puro) agregado para usos específicos sobre fondos primarios

**Documentación:**
- `README.md` reescrito completo — arquitectura, tabs, infraestructura, filosofía de diseño, reglas duras, pendientes
- `CHANGELOG.md` creado con historia v1-v25
- `NEXT_PR.md` con propuesta detallada del próximo bloque 15D ondulante para HÉRCULES

**NO cambia:**
- Funcionalidad de tabs, lógica de programa semanal, ondulante 4 semanas, Supabase RLS, multi-usuario Ariel/Melissa, IA reactiva por set, Coach del Día, Suplementos, Logística, Recetario keto CR, autoguardado 1.2s, imprimir, historial

---

## v24 — 2026-05-19 16:08 CR — fallback PERIODIZACION_15D vencido

- Fix "Plan 15D vencido" — fallback que calcula sesión del día de la ondulante 4 semanas en vez de pantalla en blanco
- Aviso de warn en Coach del Día cuando el plan explícito (15-29 abr) ya venció
- Commit `d510182`

## v23 — Smart weight recommendations

- Recomendaciones de peso por set basadas en historial de entrenamiento del usuario
- Lectura de últimas 5 sesiones del mismo día de entreno (`getPrevSessions`)

## v22 — 2026-04-12 — Periodización 15D + Coach del Día + Recetario

- Periodización 15D explícita para Ariel + Melissa
- 15 recetas keto Costa Rica integradas en Logística
- Coach del Día embebido (protocolo post-binge)
- Tema Mac claro (light mode con macCard / macGlass) — antes de v25 era el default
- Hotfixes: G.mu top-level, React hooks violation en Recetario, placeholders pendientes, anti-extensión core, sin CrossFit sábado

## v21 — IA Reactiva + Logística

- IA reactiva por set (fatiga acumulada / progresión / regresión)
- Logística (compras + stock + recetario)
- L-Arginina agregada a suplementación
- Corte de ayuno automático

## v20 — Ayuno cross-day

- Contador de ayuno con persistencia entre días
- Lógica de detección de corte de ayuno (primera ingesta)

## v19 — Análisis de sueño gender-aware

- `sleepAnalysis` adaptado a Ariel (49 años, masculino) y Melissa (45 años, femenino)
- Nueva sección "Mejoras para la app" interna

## v18 — Sub-navegación Entreno

- Pestañas internas RUTINA / SUPLEMENTOS dentro del tab ENTRENO
- Antes Suplementos era tab top-level

## v17 — Suplementos del Día sincronizados

- Sección Suplementos del Día en área Entreno
- Sincronización bidireccional con Nutrición

## v16 — Fixes Ultima ingesta

- Display correcto de `coachRecs` en Decisión del Coach
- Cálculo de horas desde última ingesta

## v15 — Fixes Unicode + warmup

- 7 bugs Unicode resueltos (energía/técnica/precaución)
- Toggle técnica warmup corregido
- Nueva área "Última ingesta" con cálculo automático de ayuno

## v14 — Notas usuario + auto-coach

- Unificación de notas del usuario
- Auto-coach analiza keywords en notas
- Fix de placeholders Unicode

## v13 — Warmup mejorado

- Warmup con colores diferenciados por bloque
- Timer dedicado de warmup

## v12 — Animal M-Stak

- Animal M-Stak agregado a suplementación
- User notes integradas
- Honey pre-workout opcional

## v11d — Ratings semánticos

- Ratings con gradiente rojo→amarillo→verde semántico

## v10 → v1 — Historia previa

Ver `git log --all` para detalle. Itinerario:
- v1-v5: prototipo inicial, tabs base, Supabase setup
- v6-v9: nutrición, ayuno, semáforo RIR
- v10: deploy estabilizado en Vercel, después migrado a GitHub Pages

---

## Convenciones

- **Bump version** cuando hay cambio user-facing (no hotfix invisible)
- **Sufijos** `hN` para hotfixes dentro de la misma versión mayor (v22h6 etc)
- **Commits en español** con formato `vNN: descripción corta`
- **CHANGELOG actualizado** en el mismo commit del cambio

---

_Mantenido por Claude Code en sesiones Code disparadas desde Dispatch de Ariel._
