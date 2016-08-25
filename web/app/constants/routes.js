import Plans from '../containers/Plans'
import Login from '../containers/Login'
import Signup from '../containers/Signup'
import urls from '../modules/urls'


export const PLANS = {
  component: Plans,
  path: 'plans',
  label: 'PLANS',
  loginRequired: true,
  onlyVisibleToAuthenticated: true
}

export const LOGIN = {
  component: Login,
  path: 'login',
  label: 'LOGIN',
  loginRequired: false,
  onlyVisibleToAnonymous: true,
}

export const LOGOUT = {
  link: urls.logout(),
  label: 'LOGOUT',
  onlyVisibleToAuthenticated: true
}

export const SIGNUP = {
  component: Signup,
  path: 'signup',
  label: 'SIGNUP',
  loginRequired: false
}


export default { PLANS, LOGIN, LOGOUT, SIGNUP }
