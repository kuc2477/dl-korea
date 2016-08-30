// ====
// Meta
// ====

export const APP_PREFIX = 'ANCHOR'


// =============
// Electron IPC
// =============

export const MAIN = 'MAIN'
export const MAIN_RENDERER = 'MAIN_RENDERER'
export const MENUBAR = 'MENUBAR'


// ========
// Crossbar
// ========

export const ROUTER_REALM =
  process.env.NODE_ENV === 'production' ? 'anchor' : 'realm1'

export const COVER_START = 'COVER_START'
export const COVER_SUCCESS = 'COVER_SUCCESS'
export const COVER_ERROR = 'COVER_ERROR'


// =============
// Celery states
// =============

export const PENDING = 'PENDING'
export const RECEIVED = 'RECEIVED'
export const STARTED = 'STARTED'
export const SUCCESS = 'SUCCESS'
export const FAILURE = 'FAILURE'
export const REVOKED = 'REVOKED'
export const RETRY = 'RETRY'


// =====
// Types
// =====

export const URL = 'url'
export const RSS = 'rss'
export const ATOM = 'atom'


// ====
// Auth
// ====

export const CSRF_TOKEN_HEADER = 'X-CSRFToken'
export const LOCAL_STORAGE_SESSION_KEY = `${APP_PREFIX}_SESSION_KEY`
export const LOCAL_STORAGE_CSRF_KEY = `${APP_PREFIX}_CSRF`


// ======
// Stages
// ======

export const SIGNUP_STEP_USER = 'SIGNUP_STEP_USER'
export const SIGNUP_STEP_PASSWORD = 'SIGNUP_STEP_PASSWORD'


export default {
  // application meta
  APP_PREFIX,
  // electron ipc
  MAIN,
  MAIN_RENDERER,
  MENUBAR,
  // crossbar
  ROUTER_REALM,
  COVER_START,
  COVER_SUCCESS,
  COVER_ERROR,
  // celery states
  PENDING,
  RECEIVED,
  STARTED,
  SUCCESS,
  FAILURE,
  REVOKED,
  RETRY,
  // schedule types
  URL,
  RSS,
  ATOM,
  // authentication
  CSRF_TOKEN_HEADER,
  LOCAL_STORAGE_SESSION_KEY,
  LOCAL_STORAGE_CSRF_KEY,
  // stages
  SIGNUP_STEP_USER,
  SIGNUP_STEP_PASSWORD,
}
