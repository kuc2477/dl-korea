import React from 'react'
import { Router, Route, IndexRedirect } from 'react-router'

import { PLANS, LOGIN, SIGNUP } from './constants/routes'
import history from './modules/history'
import { authRequired } from './modules/routing'
import App from './containers/App'


export const router = (
  <Router history={history}>
    <Route path="/" component={App}>
      <IndexRedirect to={PLANS.path} />
      <Route path={PLANS.path} component={PLANS.component} onEnter={authRequired}/>
      <Route path={LOGIN.path} component={LOGIN.component} />
      <Route path={SIGNUP.path} component={SIGNUP.component} />
    </Route>
  </Router>
)


export default router
