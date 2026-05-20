# NEXT_PR — Propuesta próximo bloque 15D ondulante (para HÉRCULES)

**Estado actual (v25):** el fallback `PERIODIZACION_15D` calcula la sesión del día desde la ondulante de 4 semanas porque el plan explícito (15-29 abr 2026) venció. La app NO está rota, pero el "Plan del día" muestra un aviso `warn` en Coach del Día indicando que el bloque explícito caducó.

**Próximo paso natural:** definir un nuevo bloque 15D con sesiones explícitas reemplazando el fallback genérico. Esto lo debe diseñar HÉRCULES (agente especializado en periodización). Esta propuesta sirve de base.

---

## Propuesta estructural — Bloque "2026-05 hipertrofia + definición"

**Fechas sugeridas:** 20-may-2026 → 03-jun-2026 (15 días).

**Objetivo macro:** mantener 9% grasa + ganar volumen muscular + definir abdomen (centro + oblicuos). Sin sacrificar SNC ni cortisol — historial de Ariel = ansioso, post-doble-jornada CrossFit, temblor esencial.

**Estructura ondulante 4 microciclos** (la ondulante actual ya implementada en `PERIODO[]` calza con esto):

| Microciclo | Semana | RIR objetivo | Volumen relativo | Carga relativa |
|---|---|---|---|---|
| ACUMULACIÓN | Sem 1 (días 1-5) | 3-4 | 100% (base) | 75% 1RM |
| INTENSIFICACIÓN | Sem 2 (días 6-10) | 2-3 | 90% | 80% 1RM |
| SOBRECARGA | Sem 3 (días 11-13) | 1-2 | 80% (-1 set por ejercicio) | 85% 1RM |
| DESCARGA | Sem 4 (días 14-15) | 4-5 | 60% (-2 sets) | 65% 1RM |

---

## Programa semanal aplicado por día

Replicar estructura `PROG[]` vigente con ajustes por microciclo.

### Lunes — Pecho + Espalda (Alta, carbos 30-40g peri-entreno)

Base por sesión:
- **Bloque A — Empuje horizontal**
  - Press banca plano (4×6-8 RIR según micro)
  - Apertura inclinada con mancuernas (3×10-12)
- **Bloque B — Tirón horizontal**
  - Remo Pendlay o T-bar (4×6-8)
  - Remo en máquina con polea baja (3×10-12)
- **Bloque C — Empuje vertical**
  - Press inclinado declinado mancuernas (3×8-10)
- **Bloque D — Tirón vertical**
  - Dominadas asistidas o jalón al pecho (3×8-10)
- **Core anti-extensión:** plancha dura 3×45s (rectus abdominis + transverso)

### Martes — Pierna Principal (Alta, carbos 30-40g)

- Sentadilla trasera barra (4×5-8 RIR según micro)
- Hip thrust con barra (4×8-10) — clave para abdomen centro+oblicuo en transferencia
- Press de pierna 45° (3×10-12)
- Curl femoral acostado (3×10-12)
- Gemelo en multipower (4×12-15) — temblor esencial: evitar saltos
- Core anti-rotación: pallof press 3×10/lado

### Miércoles — Hombro + Brazos (Media, carbos 25-35g post)

- Press militar barra o mancuernas (4×6-8)
- Elevaciones laterales con cable (4×12-15) — el deltoide lateral en cable mantiene tensión cte
- Pájaros / face pull (3×12-15) — deltoide posterior, suele faltar en exnadadores
- Curl bíceps barra Z (3×8-10)
- Tríceps polea cuerda (3×10-12)
- Tríceps press francés (3×10-12)

### Jueves — Pierna Complementaria (Media, carbos 20-30g post)

- Peso muerto rumano con barra (4×6-8) — cadena posterior, isquios
- Sentadilla búlgara (3×8-10/pierna) — unilateral, mejora asimetría
- Extensión cuádriceps (3×12-15) — finishing
- Curl femoral sentado (3×12-15)
- Abductor + aductor máquina (3×15)
- Core anti-flexión lateral: side plank 3×30s/lado

### Viernes — Hombro + Espalda (optimizado) (Media, carbos 15-30g post)

- Press hombro Arnold (4×8-10)
- Elevaciones laterales mancuerna (4×12-15)
- Dominada con peso (3×6-8) — si fatiga: jalón con agarre supino
- Remo unilateral mancuerna (3×8-10/lado)
- Encogimiento de hombros barra (3×12-15) — trapecio
- Abdomen oblicuo: russian twist con disco 3×15/lado

### Sábado — Recuperación activa / CrossFit ocasional (Baja, 0-15g)

**Default v25:** descanso activo (caminata + movilidad + sauna)
**CrossFit opcional según fatiga:** si energía ≥7 y fatiga ≤4, AMRAP 15min con burpees + KB swing + box jump. Si NO, descanso.

### Domingo — Descanso + pump dominical opcional (Baja, 15-20g post)

- Pump opcional 30min: bíceps + tríceps + hombro lateral solo (alto rep, bajo peso)
- Foco en recuperación cognitiva + paseo + lectura

---

## Personalización para Ariel (memoria de perfil)

- **Falta Omega-3 EPA+DHA 2-3g + K2 MK-7 100mcg** — incluir aviso en Coach del Día cada sesión hasta que se confirme adquisición
- **Temblor esencial en manos** — evitar ejercicios con barra pesada al fallo cercano (RIR <1) en press banca y sentadilla. Preferir mancuernas o máquina cuando RIR<1.
- **Ansiedad / impulsividad** — Coach del Día debe recordar: "respira 4-7-8 entre sets si RPE>8"
- **Historial nadador + judoca + triatleta** — alto VO2max + tolerancia al volumen. NO subir volumen abrupto pero soporta densidad alta.
- **49 años + 9% grasa + meta abdomen** — déficit calórico debe ser MODERADO (200-300 kcal), no agresivo. Anti-rotación + anti-extensión en core 3×/semana.

---

## Personalización para Melissa (si HÉRCULES diseña paralelo)

- 45 años, gym en casa + yoga, keto fase 2
- Equipamiento limitado: mancuernas + bandas + barra olímpica casa
- Sustituir Pendlay/T-bar por remo en banda
- Sustituir hip thrust en barra por hip thrust en banco con mancuerna
- Yoga 2-3×/sem (lunes + jueves + sábado) — flexibilidad de la app debe permitir log de yoga como sesión

---

## Implementación técnica en el HTML

**Dónde editar:** `index.html` → constante `PERIODIZACION_15D` (línea ~XXX por buscar)

**Estructura JS esperada (siguiendo patrón actual):**

```js
const PERIODIZACION_15D = {
  ariel: {
    fechaInicio: '2026-05-20',
    fechaFin: '2026-06-03',
    bloques: {
      '2026-05-20': { /* sesión lunes acumulación */ },
      '2026-05-21': { /* sesión martes acumulación */ },
      // ... 15 días
    }
  },
  melissa: { /* paralelo */ }
};
```

**Validar:**
1. Que el `getDia()` y `getSemPeriodo()` siguen calzando con el nuevo bloque
2. Que el fallback v24 sigue funcionando cuando el bloque venza (3-jun)
3. Que Coach del Día deja de mostrar `warn` de plan vencido

**Rollout:**
1. HÉRCULES diseña 15 sesiones (lunes-domingo × 2 semanas + 1 día extra)
2. PR a `main` con bump v26
3. Validar en producción 1-2 días
4. Si bien: continuar
5. Si mal: revertir commit, fallback v24 sigue funcionando

---

## Decisiones que requieren VB del Director

1. **Fechas exactas del bloque** — 20-may → 03-jun, o otro rango?
2. **Equipamiento gimnasio actual de Ariel** — confirmar que Pendlay row está disponible
3. **CrossFit sábado** — mantener opcional o cortarlo del todo
4. **Bloque de Melissa** — ¿se diseña paralelo o se deja fallback?

---

## Riesgos identificados

- **Lesión por sobrecarga** si Ariel empuja semana 3 sin descanso bueno semana 2 → mitigación: prescribir que RPE>9 dispara `bad` en Coach del Día (ya implementado en v23 IA reactiva)
- **Burnout SNC** post-doble-jornada → mitigación: el sábado debe quedar como recuperación por default, CrossFit solo opcional
- **Sub-recuperación oblicuos** si todos los días tienen core → mitigación: core 3×/sem máx (lun/mar/jue)

---

_Última edición: 2026-05-20. Propuesta inicial por Claude Code. HÉRCULES (cuando esté disponible) refina y emite versión final con sesiones explícitas día por día._
