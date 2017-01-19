import React, { PropTypes } from 'react'
import { Card, CardActions, CardHeader, CardMedia, CardTitle, CardText } from 'material-ui/Card'


export default class PostItem extends React.Component {
  render() {
    return (
      <Card>
        <CardHeader title={this.props.title} subtitle={this.props.content}/>
      </Card>
    )
  }
}
