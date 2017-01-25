import React, { PropTypes } from 'react'
import InfiniteList from '../base/InfiniteList'
import PostItem from './PostItem'


export default class PostList extends React.Component {
  static STYLE = {
    paddingTop: 20,
    paddingBottom: 10,
  };

  render() {
    const { STYLE } = this.constructor
    const { posts, postsById, ...rest } = this.props
    const postItems = posts.map(id => (<PostItem id={id} {...postsById.get(id)}/>))
    return (
      <div>
        <InfiniteList
          {...rest}
          useWindowAsScrollContainer
          containerHeight={400}
          elementHeight={150}
          style={STYLE}
        >
          {postItems}
        </InfiniteList>
      </div>
    )
  }
}
