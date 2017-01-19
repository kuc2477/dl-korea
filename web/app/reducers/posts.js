import Immutable from 'immutable'


export const initialState = new Immutable.Map({
  posts: new Immutable.List(['1']),
  postsById: new Immutable.Map({1: {title: 'title', content: 'content'}}),
})

export default(state = initialState, action) => {
  switch(action.type) {
    default:
      return state
  }
}
