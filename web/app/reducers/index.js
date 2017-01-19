import { combineReducers } from 'redux'
import undoable from 'redux-undo'

import base from './base'
import auth from './auth'
import signup from './signup'
import posts from './posts'


export default combineReducers({
  base, auth, signup, posts
})
