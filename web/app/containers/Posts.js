import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import PostList from '../components/posts/PostList'


class Posts extends React.Component {
  render() {
    const { posts, postsById } = this.props
    return (
      <div className="row full-height">
        <div className="col-md-4 col-md-offset-2">

          <PostList
            posts={posts}
            postsById={postsById}
          />

        </div>
      </div>
    )
  }
}


export default connect(app => ({
  posts: app.posts.get('posts'),
    postsById: app.posts.get('postsById'),
}))(Posts)
