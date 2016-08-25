import fetch from 'isomorphic-fetch'
import { authenticated, parseJson, validate } from './fetch'
import { normalize, Schema, arrayOf } from 'normalizr'
import { camelizeKeys } from 'humps'
import urls from '../modules/urls'


const userSchema = new Schema('users')
const planSchema = new Schema('plans')

export const Schemas = {
  USER: userSchema,
  USERS: arrayOf(userSchema),
  PLAN: planSchema,
  PLANS: arrayOf(planSchema),
}

// Returns next url from a paginated response if found and returns null
// otherwise.
function getNextUrl(response) {
  return response.headers.get('link')
}

// Fetches an API response and normalizes the result JSON according to schema.
// This makes every API response have the same shape, regardless of how nested.
function callAPI(endpoint, schema) {
  return fetch(endpoint, authenticated())
      .then(validate)
      .then(response => response.json().then(json => ({ json, response })))
      .then(({ json, response }) => {
        const camelized = camelizeKeys(json)
        const normalized = normalize(camelized, schema)
        const link = getNextUrl(response)
        return Object.assign({}, normalized, {
          link: link ? `${urls.app()}${link}` : null
        })
      })
}

// Action key that carries API call information interpreted by this
export const CALL_API = 'CALL_API'

// A Redux middleware that interprets actions with CALL_API info specified.
// Performs the API call and promises when such actions are dispatched.
export default store => next => action => {
  if (typeof action[CALL_API] === 'undefined') {
    return next(action)
  }
  const api = action[CALL_API]
  const { schema, types } = api
  let { endpoint } = api

  if (typeof endpoint === 'function') {
    endpoint = endpoint(store.getState())
  }

  if (typeof endpoint !== 'string') {
    throw new Error('Specify a string endpoint URL')
  } else if (!schema) {
    throw new Error('Specify one of the exported schemas')
  } else if (!Array.isArray(types) || types.length !== 3) {
    throw new Error('Expected an array of three action types')
  } else if (!types.every(type => typeof type === 'string')) {
    throw new Error('Expected action types to be strings')
  }

  function actionWith(data) {
    const finalAction = Object.assign({}, action, data)
    delete finalAction[CALL_API]
    return finalAction
  }

  const [requestType, successType, failureType] = types
  next(actionWith({ type: requestType }))

  return callAPI(endpoint, schema).then(
    response => next(actionWith({ ...response, type: successType })),
    error => next(actionWith({
      type: failureType,
      error: error ? error.message : 'something bad happened'
    }))
  )
}
