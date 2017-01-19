import React from 'react'
import { Router, Route, IndexRedirect } from 'react-router'

import { 
  POSTS, 
  POST,
  WRITE, 
  PROFILE, 
  SIGNUP, 
  LOGIN, 
} from './constants/routes'
import history from './modules/history'
import { authRequired } from './modules/routing'
import App from './containers/App'


export const router = (
  <Router history={history}>
    <Route path="/" component={App}>
      <IndexRedirect to={POSTS.path} />
      <Route path={POSTS.path} component={POSTS.component} />
      <Route path={POST.path} component={POST.component} />
      <Route path={WRITE.path} component={WRITE.component} onEnter={authRequired} />
      <Route path={LOGIN.path} component={LOGIN.component} />
      <Route path={SIGNUP.path} component={SIGNUP.component} />
      <Route path={PROFILE.path} component={PROFILE.component} onEnter={authRequired} />
    </Route>
  </Router>
)


export default router
