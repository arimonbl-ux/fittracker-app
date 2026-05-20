# FitTracker Pro

App personal de Ariel Montero para gestión integral de entreno + nutrición + progreso físico. SPA HTML pura con React 18 (CDN) + Babel Standalone + Supabase JS — **sin build step**, archivo único `index.html`.

**Live:** https://arimonbl-ux.github.io/fittracker-app/
**Repo:** [`arimonbl-ux/fittracker-app`](https://github.com/arimonbl-ux/fittracker-app)
**Versión actual:** v25 (20-may-2026) — dark-mode-first, gym-readable
**Hosting:** GitHub Pages (deploy automático en push a `main`)

---

## Para cualquier agente del ecosistema GBS

Cuando Ariel diga "actualizar app del gym", "FitTracker", "la app de gimnasio" o cualquier variante, ese agente debe:

1. **Leer este README primero.**
2. **Leer la memoria canónica** del proyecto en Cowork: `project_fittracker_app.md` — tiene perfil del usuario, programa semanal, infraestructura, pendientes.
3. **Verificar deploy vivo:** `curl -I https://arimonbl-ux.github.io/fittracker-app/` (esperar HTTP 200).
4. **Revisar commits recientes:** `git log --oneline -20` en este repo.
5. **NO romper Supabase RLS:** las tablas `sesiones_entreno`, `nutricion`, `mediciones` tienen RLS activo.
6. **NO hardcodear secretos:** Vercel token / Supabase Service Key / Cloudflare token viven en Keychain de Ariel.

---

## Arquitectura

```
index.html (~420KB)
  ├─ React 18 UMD (CDN unpkg)
  ├─ Babel Standalone (transformación JSX en cliente)
  ├─ Supabase JS v2 (UMD CDN jsdelivr)
  └─ <script type="text/babel"> con toda la app (≈5900 líneas)
       ├─ Const G = paleta dark (línea ~1370)
       ├─ Const APP_VERSION = string visible en header
       ├─ PROG[] = programa semanal por día (Ariel + Melissa)
       ├─ PERIODO[] = ondulante 4 semanas (acumulación → intensificación → sobrecarga → descarga)
       ├─ PERIODIZACION_15D (con fallback v24 si vencido)
       ├─ Componentes UI (Inp, Sec, NavSemana, Rating, RestTimer, …)
       ├─ Tabs (TabEntreno, TabNutricion, TabBalance, TabLogistica, TabProgreso)
       ├─ UserSelector (Ariel + Melissa)
       └─ App root
```

**Multi-usuario:** Ariel + Melissa, IDs hardcoded UUID estables. Auto-auth anónimo Supabase. No hay login real (público intencional, Anon Key + RLS por user_id).

**Sin build step:** todo se sirve estático desde GitHub Pages. Babel transpila JSX en el browser. Tradeoff: archivo grande (~420KB) y primer paint ~600ms en 4G. Aceptado por simplicidad de mantenimiento.

---

## Tabs

| Tab | Función |
|---|---|
| ENTRENO | 7 días, semáforo RIR, técnica por ejercicio, sets/reps/peso/RIR/RPE/cadencia, métricas PRE/POST, Coach del Día, sub-pestaña Suplementos |
| NUTRICION | Timer ayuno automático, registro alimentos por momento, macros, nivel hambre, análisis holístico SNC/sueño/ansiedad |
| BALANCE | Balance global del día (sueño, energía, alimentación, fatiga) |
| LOGISTICA | Compras + stock + recetario keto CR |
| PROGRESO | Peso + cintura con fecha, tendencia histórica |

Header sticky con backdrop blur. Selector usuario (Ariel/Melissa) con perfil persistido.

---

## Infraestructura

- **Hosting:** GitHub Pages — deploy automático push a `main`
- **Backend:** Supabase `byrgpddpmpoffgfegmjk` (Anon Key embebida en HTML, RLS activo)
- **Tablas:** `sesiones_entreno`, `nutricion`, `mediciones`
- **Credenciales sensibles:** Keychain de macOS del Director (`security find-generic-password -s <servicio>`)

---

## Filosofía de diseño (v25)

- **Dark mode por default** — gym suele tener luz fría, mejor contraste en bajada de luz, menos fatiga ocular post-entreno
- **Paleta limitada:** 4 funcionales — `bg #000`, surface `#1c1c1e`, accent `#0a84ff`, semáforo verde/naranja/rojo iOS dark
- **Tipografía:** SF Pro Display/Text system stack, `font-variant-numeric: tabular-nums` para números legibles
- **Tap targets 44px+** en inputs (cumple Apple HIG)
- **Número del set actual** legible desde 1 metro (clase `.hero-num`, fontSize 19, fontWeight 800)
- **Animaciones discretas** — transiciones 180ms, scale 0.97 al press, prPulse para PR
- **NO inspiración** de apps fitness saturadas. SÍ inspiración: Apple Health, WHOOP, Strava, Hevy, MacroFactor
- **Modo impreso conservado en light** (papel) — `imprimir()` abre nueva pestaña con CSS independiente

---

## Cómo deployar un cambio

```bash
cd /Users/gbslaw/Documents/Claude/Projects/fittracker-app
# editar index.html
git add index.html
git commit -m "vNN: descripción"
git push origin main
# GitHub Pages re-publica en 1-3 minutos
curl -I https://arimonbl-ux.github.io/fittracker-app/
```

**No hace falta:** webpack, vite, npm install, node, build step alguno.

---

## Reglas duras

- ❌ No tocar `.git`, `.env`, force push, borrar main, desactivar Actions
- ❌ No hardcodear tokens / passwords en HTML
- ❌ No romper RLS de Supabase — queries siempre con `user_id` filter
- ❌ No introducir build step (rompe filosofía "edita y push")
- ✅ Comentarios y textos UI en español de Costa Rica
- ✅ Commits descriptivos en español: `vNN: <qué cambió>`
- ✅ Bump version en `APP_VERSION` cuando hay cambio user-facing
- ✅ Actualizar `CHANGELOG.md` con el cambio

---

## Pendientes ([CHANGELOG.md](CHANGELOG.md) tiene más detalle)

**Inmediato:**
- HÉRCULES diseña próximo bloque 15D que reemplaza el fallback ondulante (ver `NEXT_PR.md`)
- Validar app en iPhone / iPad / iMac / MacBook Pro en condiciones reales

**Mediano:**
- Gráficas tendencia peso+cintura (Recharts o canvas simple)
- Imprimible PRE/INTRA/POST con suplementos personalizados
- PWA offline con service worker (cache shell)

**Largo:**
- Integración Apple Health (peso, HR, sueño)
- Tracker de suplementos (recordatorios Omega-3, K2 MK-7)
- Coach IA que valide científicamente el plan del coach humano

---

## Contacto

App personal — **no hay soporte público**. Para temas técnicos del ecosistema GBS, contactar `contacto@gbs.law`.

---

_Última actualización del README: 2026-05-20 por Claude Code (sesión Code de Dispatch)_
