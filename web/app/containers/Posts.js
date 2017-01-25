import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import PostList from '../components/posts/PostList'
import RaisedButton from 'material-ui/RaisedButton'
import Chip from 'material-ui/Chip'
import { PRIMARY, SECONDARY } from '../constants/colors'


class Posts extends React.Component {
  static CHIP_STYLE = {
    margin: 5,
    color: 'white',
  };

  render() {
    const { CHIP_STYLE } = this.constructor
    const { posts, postsById } = this.props
    return (
      <div className="flex-container-v">
        <div className="col-md-4 col-md-offset-2">
          <div className="row">
            <Chip style={CHIP_STYLE} backgroundColor={PRIMARY}>tag 1</Chip>
            <Chip style={CHIP_STYLE}>tag 2</Chip>
            <Chip style={CHIP_STYLE}>tag 3</Chip>
            <Chip style={CHIP_STYLE}>tag 4</Chip>
          </div>
          <PostList className="flex-content" posts={posts} postsById={postsById}/>
          <RaisedButton 
            secondary 
            label="포스트 작성하기" 
            fullWidth={true} 
            icon={<i className="fa fa-pencil" style={{color: 'white'}}></i>}
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
