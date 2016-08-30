import Plans from '../containers/Plans'
import PlanCreation from '../containers/PlanCreation'
import Profile from '../containers/Profile'
import Login from '../containers/Login'
import Signup from '../containers/Signup'
import urls from '../modules/urls'


export const PLANS = {
  component: Plans,
  path: 'plans',
  label: 'PLANS',
  loginRequired: true,
  onlyVisibleToAuthenticated: true,
}

export const PLAN_CREATION = {
  component: PlanCreation,
  path: `${PLANS.path}/creation`,
  label: 'CREATE NEW PLAN',
  loginRequired: true,
  onlyVisibleToAuthenticated: true,
}

export const PROFILE = {
  component: Profile,
  path: 'profile',
  label: 'PROFILE',
  loginRequired: true,
  onlyVisibleToAuthenticated: true,
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


export default { 
  PLANS, 
  PLAN_CREATION,
  PROFILE,
  LOGIN, 
  LOGOUT, 
  SIGNUP 
}
