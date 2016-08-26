import React from 'react'
import { Router, Route, IndexRedirect } from 'react-router'

import { PLANS, TALKS, LOGIN, SIGNUP, PROFILE, } from './constants/routes'
import history from './modules/history'
import { authRequired } from './modules/routing'
import App from './containers/App'


export const router = (
  <Router history={history}>
    <Route path="/" component={App}>
      <IndexRedirect to={PLANS.path} />
      <Route path={PLANS.path} component={PLANS.component} onEnter={authRequired} />
      <Route path={TALKS.path} component={TALKS.component} onEnter={authRequired} />
      <Route path={LOGIN.path} component={LOGIN.component} />
      <Route path={SIGNUP.path} component={SIGNUP.component} />
      <Route path={PROFILE.path} component={PROFILE.component} onEnter={authRequired} />
    </Route>
  </Router>
)


export default router
