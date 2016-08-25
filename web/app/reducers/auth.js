import Immutable from 'immutable'

import {
  AUTH_START,
  AUTH_SUCCSESS,
  AUTH_ERROR,
  LOGOUT,
  USER_INIT_SUCCESS,
  USER_INIT_ERROR,
} from '../actions/auth'


export const initialState = new Immutable.Map({
  // user, auth
  user: null,
  isAuthenticating: false,
  didAuthFail: false,
  didUserInitFail: false,
  errorMessage: null,
  // confirmation
  emailToResend: null,
  didNotConfirmed: false,
})

export default (state = initialState, action) => {
  switch (action.type) {
    case AUTH_START:
      return state.set('isAuthenticating', true)

    case AUTH_SUCCSESS:
      return state.merge({
        // set user and clear auth errors
        user: action.user,
        isAuthenticating: false,
        didAuthFail: false,
        didUserInitFail: false,
        errorMessage: null,
        // clear confirmation errors
        emailToResend: null,
        didNotConfirmed: false
      })

    case AUTH_ERROR:
      return state.merge({
        isAuthenticating: false,
        didAuthFail: true,
        errorMessage: action.reason,
        emailToResend: action.email,
        didNotConfirmed: !!action.email
      })

    case LOGOUT:
      return initialState

    case USER_INIT_SUCCESS:
      return state.merge({
        user: new Immutable.Map(action.user),
        didUserInitFail: false
      })

    case USER_INIT_ERROR:
      return state.merge({
        didUserInitFail: true
      })

    default:
      return state
  }
}
