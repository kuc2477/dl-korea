import _ from 'lodash'


// ==================
// Request Middleware
// ==================

class RequestMiddleware {
  constructor(options) {
    this.options = options || {}
  }

  authenticated() {
    const updated = Object.assign({}, this.options, {
      credentials: 'include',
    })
    return new RequestMiddleware(updated)
  }

  postJson(data) {
    const updated = Object.assign({}, this.options, {
      method: 'POST',
      headers: {
        'Acccept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    })
    return new RequestMiddleware(updated)
  }

  value() {
    return this.options
  }
}

export const m = new RequestMiddleware()


// ====================
// Response Middlewares
// ====================

export function parseJson(response) {
  return response.json()
}

export function validate(response) {
  if (response.status < 200 && response.status >= 300) {
    let error = new Error(response.statusText)
    error.response = response
    throw error
  } 
  return response
}
