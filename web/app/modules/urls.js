// ===============
// Component Bases
// ===============

export const app = () => {
  return process.env.NODE_ENV === 'development' ?
    'http://localhost:5000' :
    'http://localhost:5000'

}
export const api = () => 'api'


// ==========
// Resources
// ==========

export const login = () => `${app()}/${api()}/login`
export const logout = () => `${app()}/${api()}/logout`
export const signup = () => `${app()}/${api()}/signup`
export const csrf = () => `${app()}/${api()}/csrf`
export const userinfo = () => `${app()}/${api()}/userinfo`
export const resend = () => `${app()}/${api()}/resend`

export const users = id => id ?
  `${app()}/${api()}/users/${id}` :
  `${app()}/${api()}/users`


export default {
  app, login, logout, signup, csrf, userinfo, resend,
  users,
}
