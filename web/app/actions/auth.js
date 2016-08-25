import fetch from 'isomorphic-fetch'
import { parseJson, validate, m } from '../middlewares/fetch'
import urls from '../modules/urls'
import { toast } from '../modules/utils'
import { PLANS, LOGIN } from '../constants/routes'


// ===============
// Authentications
// ===============

export const AUTH_START = 'AUTH_START'
export function authStart() {
  return { type: AUTH_START }
}

export const AUTH_SUCCSESS = 'AUTH_SUCCSESS'
export function authSuccess(user) {
  return { type: AUTH_SUCCSESS, user }
}

export const AUTH_ERROR = 'AUTH_ERROR'
export function authError(reason = 'Something went wrong', email = null) {
  return { type: AUTH_ERROR, reason, email }
}

export function authenticate(email, password, router, next = PLANS.path) {
  return (dispatch) => {
    dispatch(authStart())

    fetch(urls.login(), m.postJson({ email, password }).value())
      .then(validate)
      .then(parseJson)
      .then(data => {
        const { user, reason, email: emailToResend } = data
        if (reason) {
          // we consider the user is unconfirmed if the server's response
          // contains user's email (implicating that the confirmation did not
          // passed yet).
          dispatch(authError(reason, emailToResend))
          return
        }
        dispatch(authSuccess(user))
        router.replace(next)
      }).catch(error => {
        dispatch(authError())
      })
  }
}

export const LOGOUT = 'LOGOUT'
export function logout(router, next = LOGIN.path) {
  return (dispatch) => {
    fetch(urls.logout(), m.postJson().authenticated().value()).then(() => {
      dispatch({ type: LOGOUT })
      router.replace(next)
    })
  }
}

export const RESEND_CONFIRMATION_MAIL = 'RESEND_CONFIRMATION_MAIL'
export function resendConfirmationMail(email) {
  return (dispatch) => {
    fetch(urls.resend(), m.postJson({ email }).value())
      .then(validate)
      .then(parseJson)
      .then(data => {
        dispatch({ type: RESEND_CONFIRMATION_MAIL, email })
        toast(`Confirmation mail has been sent to ${email}`, {
          duration: null,
        })
      })
  }
}


// =========================================================
// User information initialization (via token within cookie)
// =========================================================

export const USER_INIT_START = 'USER_INIT_START'
export function userInitStart() {
  return { type: USER_INIT_START }
}

export const USER_INIT_SUCCESS = 'USER_INIT_SUCCESS'
export function userInitSuccess(user) {
  return { type: USER_INIT_SUCCESS, user }
}

export const USER_INIT_ERROR = 'USER_INIT_ERROR'
export function userInitError(reason = 'Unknown reason') {
  return { type: USER_INIT_ERROR, reason }
}

export function initUser(replace, callback) {
  return (dispatch) => {
    dispatch(userInitStart())
    fetch(urls.userinfo(), m.authenticated().value())
      .then(validate)
      .then(parseJson)
      .then(json => {
        dispatch(userInitSuccess(response.body.user))
        callback()
      }).catch(error => {
          // There's 2 possible reason of failing user initialization.
          //
          // 1. Session key in local storage has been expired on server side.
          // 2. Internal server error
          //
          // We redirect to login page if failed due to session expiration and
          // redirect to error page otherwise.
          dispatch(userInitError())
          replace(LOGIN.path)
          callback()
      })
  }
}
