import Posts from '../containers/Posts'
import Post from '../containers/Post'
import Write from '../containers/Write'
import Profile from '../containers/Profile'
import Login from '../containers/Login'
import Signup from '../containers/Signup'
import urls from '../modules/urls'


export const POSTS = {
  component: Posts,
  path: 'posts',
  label: '포스트',
  loginRequired: false,
  onlyVisibleToAuthenticated: false,
}

export const POST = {
  component: Post,
  path: 'posts/:id',
  label: '포스트',
  loginRequired: false,
  onlyVisibleToAuthenticated: false,
}

export const WRITE = {
  component: Write,
  path: `${POSTS.path}/write`,
  label: '포스트 작성',
  loginRequired: true,
  onlyVisibleToAuthenticated: true,
}

export const PROFILE = {
  component: Profile,
  path: 'profile',
  label: '프로필',
  loginRequired: true,
  onlyVisibleToAuthenticated: true,
}

export const LOGIN = {
  component: Login,
  path: 'login',
  label: '로그인',
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
  label: '회원가입',
  loginRequired: false
}


export default { 
  POSTS,
  POST,
  WRITE,
  PROFILE,
  LOGIN, 
  LOGOUT, 
  SIGNUP 
}
