import { combineReducers } from 'redux'
import undoable from 'redux-undo'

import base from './base'
import auth from './auth'
import signup from './signup'


export default combineReducers({
  base, auth, signup
})
