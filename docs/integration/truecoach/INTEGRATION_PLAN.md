# Integración TrueCoach → FitTracker

**Generado:** 5-jun-2026 por ATLAS + Claude Code (autónomo)
**Aprobado para PR:** Director Ariel Montero (vía "dale" en chat)
**Pendiente:** push a Supabase + activación del tab Historial (VB Director, §15.8 CAMINO B)

---

## Qué es esto

Paquete completo para integrar **5 años de coaching de Howard** (TrueCoach `howiecoach.truecoach.co`) al stack de FitTracker, **sin tocar la lógica del motor adaptativo v25** (regla D3 v1 intocable).

## Estado del paquete

| Componente | Estado | Ubicación |
|---|---|---|
| Data raw bajada (1,093 workouts · 6,978 items · 5.7MB) | ✅ | `_OUT_ATLAS/_TRUECOACH_EXPORT/02_workouts_complete.json` (OneDrive, no en repo por tamaño) |
| Data parseada lista para Supabase (6.7MB) | ✅ | `_OUT_ATLAS/_TRUECOACH_EXPORT/MAPPED_FITTRACKER_READY.json` |
| Schema SQL Supabase (tablas separadas, RLS estricta) | ✅ | [`MIGRATION_001_truecoach_imports.sql`](./MIGRATION_001_truecoach_imports.sql) |
| Script de carga con `--dry-run` | ✅ | [`load_to_supabase.py`](./load_to_supabase.py) |
| Auditoría científica Tier 1-2 | ✅ | [`AUDITORIA_CIENTIFICA_HOWARD.md`](./AUDITORIA_CIENTIFICA_HOWARD.md) |
| Tab Historial en index.html | ✅ feature flag OFF | `index.html` (este PR) |
| Carga real a Supabase staging | ⏸️ pendiente VB Director | — |
| Activación tab Historial (feature flag ON) | ⏸️ pendiente carga Supabase | — |

---

## Decisiones de diseño tomadas

1. **Tablas separadas** (`truecoach_imports_workouts` + `truecoach_imports_items`) en vez de append a `sesiones_entreno` →
   - Cero riesgo a v1 producción
   - Permite borrar todo el import sin afectar el motor adaptativo
   - El auditor cruza ambos tablas explícitamente

2. **RLS estricta** vía `auth.uid()` → solo el dueño ve sus imports. Coaches Pro futuros (Fase 6) requerirán policy adicional.

3. **`raw_workout` JSONB** preservado → permite re-parsing futuro si cambia el algoritmo de extracción de sets/reps/RIR.

4. **Feature flag** `ENABLE_TRUECOACH_HISTORY` en `index.html` → off por defecto. Se activa SOLO cuando las tablas existan en Supabase.

5. **NO inserción al motor adaptativo R1-R7** → la data importada queda separada como referencia histórica + insumo del auditor. El motor adaptativo sigue operando solo con `sesiones_entreno` nativa.

---

## Próximos pasos (cuando Director apruebe)

### Paso 1: Aplicar migration SQL en Supabase
1. Director abre Supabase Studio → SQL Editor
2. Copia y pega contenido de `MIGRATION_001_truecoach_imports.sql`
3. Click "Run" — crea las 2 tablas + vista + RLS

### Paso 2: Cargar data (con --dry-run primero)
```bash
export SUPABASE_URL='https://byrgpddpmpoffgfegmjk.supabase.co'
export SUPABASE_SERVICE_KEY='eyJ...'   # Service Role Key (no Anon!)
export ARIEL_USER_UUID='<UUID del Director en auth.users>'

# Validar (no escribe nada)
python3 docs/integration/truecoach/load_to_supabase.py --dry-run

# Validar con 10 workouts solamente
python3 docs/integration/truecoach/load_to_supabase.py --limit 10

# Si todo OK, cargar todo
python3 docs/integration/truecoach/load_to_supabase.py
```

### Paso 3: Activar feature flag en index.html
Cambiar:
```js
const ENABLE_TRUECOACH_HISTORY = false;
```
a:
```js
const ENABLE_TRUECOACH_HISTORY = true;
```
Commit + push → deploy automático GitHub Pages.

### Paso 4: Usar el auditor (Fase futura)
El motor adaptativo R1-R7 puede leer de `truecoach_imports_*` y producir feedback sobre el plan externo. Esto va en un PR separado.

---

## Referencias

- **Auditoría científica:** [`AUDITORIA_CIENTIFICA_HOWARD.md`](./AUDITORIA_CIENTIFICA_HOWARD.md) — 6 hallazgos con citas Schoenfeld / Helms / Israetel / Issurin / Bompa / ACSM / NSCA
- **Plan ejecutivo ATLAS** (no en repo, en OneDrive): `_OUT_ATLAS/2026-06-05_upgrade_truecoach_killer/PLAN_EJECUTIVO_v01.md`
- **Filosofía operativa** (no en repo, en memoria persistente): `_CLAUDE_MEMORY/memory/feedback_fittracker_filosofia_frio_riguroso_2026-06-05.md`
- **CLAUDE.md §15.8** (CAMINO B para tocar producción): aplicado para Supabase push

---

## ⚠️ NO hacer

- ❌ NO compartir `AUDITORIA_CIENTIFICA_HOWARD.md` con el coach (IP del Director).
- ❌ NO insertar la data importada en `sesiones_entreno` directamente (mezcla data + motor adaptativo).
- ❌ NO activar `ENABLE_TRUECOACH_HISTORY = true` sin tener las tablas creadas (rompe queries en runtime).
- ❌ NO descalificar a coaches en lenguaje público del producto (regla D9 narrativa "elevar estándar").
